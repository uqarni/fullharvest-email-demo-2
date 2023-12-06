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
    # Create a title for the chat interface
    st.title("Full Harvest Bot (named Harvey)")
    st.write("To test, first select some fields then click the button below.")
   
    
    name_of_buyer = st.text_input('Name of buyer', value = 'Buyer-Test')
    email_of_buyer = st.text_input('Email of buyer', value = 'uzairanjum@hellogepeto.com')
    phone_number_of_buyer = st.text_input('Phone number of buyer',value = '+16469802405')
    supplier_name = st.text_input('Supplier name',value = 'Supplier-Test')
    supplier_address = st.text_input(' Supplier address',value = '')
    ple_delivered = st.text_input('Priority Listing Email Delivered',value = '')
    ple_open_count = st.text_input('Priority Listing Email Opened Count',value = '')
    ple_clicked_count = st.text_input('Priority Listing Email Clicked Count',value = '')
    ple_produced_type = st.text_input('Produce type in the PLE',value = '')
    ple_supplier_available_date = st.text_input('Produce available date from the supplier in the PLE',value = '')
    ple_supplier_growing_method = st.text_input('Produce growing method from the supplier in the PLE',value = '')
    ple_supplier_product_price = st.text_input('Produce price from the supplier in the PLE',value = '')
    ple_supplier_packing_type = st.text_input('Produce packing type from the supplier in the PLE',value = '')
    ple_supplier_product_volume = st.text_input('Produce volume from the supplier in the PLE',value = '')
    produce_priority_listing_link= st.text_input('Produce priority listing link for purchase',value = '')
    full_harvest_account = st.text_input('Full Harvest Account executive email tied to the buyer',value = '')
    priority_lisitng_purchase = st.text_input('Priority Listing Purchase Status',value = '')


    lead_dict_info = {
        'name_of_buyer' : name_of_buyer,
        'email_of_buyer' : email_of_buyer,
        'phone_number_of_buyer' : phone_number_of_buyer, 
        'supplier_name' : supplier_name,
        'supplier_address' : supplier_address,
        'ple_delivered' : ple_delivered,
        'ple_open_count' : ple_open_count,
        'ple_clicked_count' : ple_clicked_count,
        'ple_produced_type' : ple_produced_type,
        'ple_supplier_available_date' : ple_supplier_available_date,
        'ple_supplier_growing_method' : ple_supplier_growing_method,
        'ple_supplier_product_price' : ple_supplier_product_price,
        'ple_supplier_packing_type' : ple_supplier_packing_type,
        'ple_supplier_product_volume' : ple_supplier_product_volume,
        'produce_priority_listing_link': produce_priority_listing_link,
        'full_harvest_account' : full_harvest_account,
        'priority_lisitng_purchase' : priority_lisitng_purchase
 
    }
    name = 'persistent_harvey'
    if st.button('Click to Start or Restart'):
        data, count = supabase.table("bots_dev").select("*").eq("id", 'persistent_harvey').execute()   
        bot_info = data[1][0]
        
        system_prompt = bot_info['system_prompt']        
        initial_text = "Hey, this is {name} from Full Harvest. Just saw you signed up on our platform. Am I speaking with {name_of_buyer}?"

        system_prompt = system_prompt.format(
                                            name=name, 
                                            name_of_buyer = name_of_buyer,
                                            email_of_buyer = email_of_buyer,
                                            phone_number_of_buyer = phone_number_of_buyer,
                                            supplier_name = supplier_name,
                                            supplier_address = supplier_address,
                                            ple_delivered = ple_delivered,
                                            ple_open_count = ple_open_count,
                                            ple_clicked_count = ple_clicked_count,
                                            ple_produced_type = ple_produced_type,
                                            ple_supplier_available_date = ple_supplier_available_date,
                                            ple_supplier_growing_method = ple_supplier_growing_method,
                                            ple_supplier_product_price = ple_supplier_product_price,
                                            ple_supplier_packing_type = ple_supplier_packing_type,
                                            ple_supplier_product_volume = ple_supplier_product_volume,
                                            produce_priority_listing_link= produce_priority_listing_link,
                                            full_harvest_account = full_harvest_account,
                                            priority_lisitng_purchase = priority_lisitng_purchase,
                                            booking_link = 'booking_link_data',
                                            selected_commodities = "",
                                            bid_request_link= ""
        )
        initial_text = initial_text.format(name_of_buyer = name_of_buyer, name=name)

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
