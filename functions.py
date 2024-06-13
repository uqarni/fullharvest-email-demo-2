import openai as op
import os
import re
import random
from datetime import datetime, timedelta
import random
import time

#examples puller
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_sms(message):
    # Use regular expressions to split the string at ., !, or ? followed by a space or newline
    sentences = re.split('(?<=[.!?]) (?=\\S)|(?<=[.!?])\n', message.strip())
    # Strip leading and trailing whitespace from each sentence
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # Compute the total length of all sentences
    total_length = sum(len(sentence) for sentence in sentences)

    # Split the sentences into two parts such that the difference in their total lengths is minimized
    part1 = []
    part2 = []
    part1_length = 0
    i = 0
    while i < len(sentences) and part1_length + len(sentences[i]) <= total_length / 2:
        part1.append(sentences[i])
        part1_length += len(sentences[i])
        i += 1

    part2 = sentences[i:]

    # Join the sentences in each part back into strings
    #if part1 is empty, just return part2
    if len(part1) == 0:
        strings = [" ".join(part2)]
    else:
        #half the time, include both parts in two strings
        if random.random() < 0.5:
            strings = [" ".join(part1), " ".join(part2)]
        else:
            #add both part1 and part2 into one string
            strings = [" ".join(part1 + part2)]

    return strings

def add_space_after_url(s):
    words = s.split()
    for i, word in enumerate(words):
        if word.startswith('http://') or word.startswith('https://'):
            if word[-1] in '.,!?;:':
                words[i] = word[:-1] + ' ' + word[-1] + ' '
            else:
                words[i] = word + ' '
    return ' '.join(words)

def find_txt_examples(query, k=8):
    loader = TextLoader("sops.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50, length_function = len, is_separator_regex = False)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
       print(len(str(doc)))
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    docs = db.similarity_search(query, k=k)

    examples = ""
    i = 1
    for doc in docs:
       examples += f'\n\nSNIPPET {i}' + doc.page_content
       i+=1
    return examples

def format_links(text):
    # Regular expression to identify URLs
    # Matches URLs starting with http://, https://, or www., and simple .com URLs
    url_regex = r'(https?://\S+|www\.\S+|\b\S+\.com\b)'
    
    # Function to replace each URL with Markdown link format
    def replace_with_link(match):
        url = match.group(0)
        # Add http:// if the URL starts with www. or ends with .com and does not start with http:// or https://
        if url.startswith('www.') or (url.endswith('.com') and not (url.startswith('http://') or url.startswith('https://'))):
            url = 'http://' + url
        return f"[Link]({url})"

    # Replace all found URLs in the text
    return re.sub(url_regex, replace_with_link, text)

#generate openai response; returns messages with openai response
def ideator(messages, lead_dict_info):
#
    prompt = messages[0]['content']
    messages = messages[1:]
    new_message = messages[-1]['content']

    #perform similarity search
    examples = find_txt_examples(new_message, k=5)
    prompt = prompt + examples
    prompt = prompt.format(**lead_dict_info)
    #print('inbound message: ' + str(messages[-1]))
    #print('prompt' + prompt)
    #print('\n\n')
    prompt = {'role': 'system', 'content': prompt}
    messages.insert(0,prompt)
    
    for message in messages:
       print(message)
    for i in range(5):
      try:
        key = os.environ.get("OPENAI_API_KEY")
        op.api_key = key
    
        result = op.ChatCompletion.create(
          model="gpt-4o",
          messages= messages,
          max_tokens = 500,
          temperature = 0
        )
        response = result["choices"][0]["message"]["content"]
        # newline = "  \n"
        # response = response.replace("Best, Harvey", "")
        # response = response.replace("Best,\nHarvey", "")
        # response = response.replace("Best,\n\nHarvey", "")
        # response = response.replace("Best,  \nHarvey", "")
        # response = response.replace("Cheers,\nHarvey", "")
        # response = response.replace("Cheers,  \nHarvey", "")
        # response = response.replace("Cheers,\n\nHarvey", "")
        # response = response.replace("Cheers, Harvey", "")
        # response = response.replace("\n", newline)
        # response = response + newline + newline + 'Best,' + newline + 'Harvey'
        print('response:')
        print(response)
        print('\n\n')
        break
      except Exception as e: 
        error_message = f"Attempt {i + 1} failed: {e}"
        #print(error_message)
        if i < 4:  # we don't want to wait after the last try
          time.sleep(5)  # wait for 5 seconds before the next attempt

    response = add_space_after_url(response)
    split_response = split_sms(response)
    count = len(split_response)
    section = {
           "role": "assistant", 
           "content": response
           }
    messages.append(section)
    
    return messages, 1

def create_produce_link_url(buyer_or_supplier, inputs):
  to_append = ''
  for input in inputs:
    to_append += f'&commodity{inputs}'

  base = 'https://app.fullharvest.com/listings?anonymous=true'
  search_produce_link = base + to_append

  return search_produce_link


   

   
