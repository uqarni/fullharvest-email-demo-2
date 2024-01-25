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
          model="gpt-4",
          messages= messages,
          max_tokens = 500,
          temperature = 0
        )
        response = result["choices"][0]["message"]["content"]
        newline = "  \n"
        response = response.replace("Best, Harvey", "")
        response = response.replace("Best,\nHarvey", "")
        response = response.replace("Cheers,\nHarvey", "")
        response = response.replace("Cheers,  \nHarvey", "")
        response = response.replace("Cheers,\n\nHarvey", "")
        response = response.replace("Cheers, Harvey", "")
        response = response.replace("\n", newline)
        response = response + newline + newline + 'Best,' + newline + 'Harvey'
        print('response:')
        print(response)
        print('\n\n')
        break
      except Exception as e: 
        error_message = f"Attempt {i + 1} failed: {e}"
        #print(error_message)
        if i < 4:  # we don't want to wait after the last try
          time.sleep(5)  # wait for 5 seconds before the next attempt
  
    def split_sms(message):
        #not splitting it for now so just return it as a list
        import re
        message = [message]
        for m in message:
           print('###')
           print(m)
           print('###')
        return message

    response = format_links(response)
    #split_response = split_sms(response)
    #count = len(split_response)
    section = {
           "role": "assistant", 
           "content": response
           }
    messages.append(section)
    
    return messages, 1
  

def add_space_after_url(s):
    words = s.split()
    for i, word in enumerate(words):
        if word.startswith('http://') or word.startswith('https://'):
            if word[-1] in '.,!?;:':
                words[i] = word[:-1] + ' ' + word[-1] + ' '
            else:
                words[i] = word + ' '
    return ' '.join(words)


def create_produce_link_url(buyer_or_supplier, inputs):
  to_append = ''
  for input in inputs:
    to_append += f'&commodity{inputs}'

  base = 'https://app.fullharvest.com/listings?anonymous=true'
  search_produce_link = base + to_append

  return search_produce_link


   

   
