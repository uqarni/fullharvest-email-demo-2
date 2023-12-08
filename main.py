import streamlit as st
from functions import ideator, create_produce_link_url
import json
import os
from datetime import datetime
from supabase import create_client, Client

#connect to supabase database
urL: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(urL, key)




def main():
    message = """
            The following bot is how Harvey is going to correspond with buyers who receive and click on the Priority Listings. The objective is to find out what the buyers need if they need anything different than what’s on the listing, and then schedule a call with their account executive to see if Full Harvest can help them.

            We need your help in identifying how Harvey can correspond better. To do that, we need example conversations.

            Here’s a video on how to give feedback to Harvey.
            [Harvey Feedback Instructions Video](https://www.loom.com/share/5577b742cecd4d82939697e17bc7c617)

            Here’s the google doc you can leave your feedback in:
            [Feedback Google Doc](https://docs.google.com/document/d/147Bzbi1zbcdN4kmuv2enOF6RcROeLpCI5v12fx2oJ_w/edit)
            """


    # Create a title for the chat interface
    st.title("Harvey Outbound")
    st.write(message)
   
    
    name = 'Harvey'
    buyer_first_name = st.text_input('Buyer first name', value = 'John')
    buyer_company_name = st.text_input('Buyer company name:', value = ' Fresh Vegetables Buyers, Inc.')
    booking_link = st.text_input('Meeting Booking Link',value = 'fullharvestbookinglink.com')
    email_buyer = st.text_input('Email of buyer',value = 'john@freshveggies.com')
    supplier_name = st.text_input('Supplier name',value = 'Appleseed Farms')
    supplier_address = st.text_input('Supplier address',value = '555 Springfield Road, Boston, MA')
    selected_commodities = st.text_input('Produce type',value = 'Spaghetti Squash')
    growing_method = st.text_input('Growing Method',value = 'Organic')
    available_date = st.text_input('Available Date',value = 'December 1st, 2023')
    price = st.text_input('Price per lb',value = '$1')
    packing_type = st.text_input('Packing type',value = 'Bin')
    volume = st.text_input('Available volume',value = '575 lbs')
    priority_listing_link= st.text_input('Priority Listing Direct Link:',value = 'fullharvestplelink.com')



    lead_dict_info = {
        "name" : 'Harvey',
        "buyer_first_name" :buyer_first_name,
        "buyer_company_name" :buyer_company_name,
        "booking_link" :booking_link,
        "email_buyer" :email_buyer,
        "supplier_name" :supplier_name,
        "supplier_address" :supplier_address,
        "selected_commodities" :selected_commodities,
        "growing_method" :growing_method,
        "available_date" :available_date,
        "price" :price,
        "packing_type" :packing_type,
        "volume" :volume,
        "priority_listing_link":priority_listing_link,
 
    }
    if st.button('Click to Start or Restart'):
        data, count = supabase.table("bots_dev").select("*").eq("id", 'outbound_harvey').execute() 

        bot_info = data[1][0]
        system_prompt = bot_info['system_prompt']  
        initial_text = bot_info['initial_text'] 
        initial_text =initial_text.format(name=name, selected_commodities =selected_commodities)
        system_prompt = system_prompt.format(**lead_dict_info)

        st.write(initial_text)


        #clear database to only first two lines
        with open('database.jsonl', 'w') as f:
        # Override database with initial json files
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": initial_text}            
            ]
            f.write(json.dumps(messages[0])+'\n')
            f.write(json.dumps(messages[1])+'\n')


    # Create a text input for the user to enter their message and append it to messages
    userresponse = st.text_input("Enter your message")
    

    # Create a button to submit the user's message
    if st.button("Send"):
        #prep the json
        newline = {"role": "user", "content": userresponse}

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(newline) + '\n')

        #extract messages out to list
        messages = []

        with open('database.jsonl', 'r') as f:
            for line in f:
                json_obj = json.loads(line)
                messages.append(json_obj)

        #generate OpenAI response
        messages, count = ideator(messages, lead_dict_info)

        #append to database
        with open('database.jsonl', 'a') as f:
                for i in range(count):
                    f.write(json.dumps(messages[-count + i]) + '\n')



        # Display the response in the chat interface
        string = ""

        for message in messages[1:]:
            if 'This is a secret internal thought' not in str(message):
                string = string + message["role"] + ": " + message["content"] + "\n\n"
        st.write(string)
        

if __name__ == '__main__':
    main()
