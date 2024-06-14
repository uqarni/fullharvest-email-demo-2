import streamlit as st
from functions import ideator, create_produce_link_url
import json
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv() 

#connect to supabase database
urL: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(urL, key)




def main():
    message = """
            This is a testing site for Outbound Harvey email. Please share all feedback with screenshots and suggested changes directly with Mert.
            Reminder: one person using the site at a time. 
            """


    # Create a title for the chat interface
    st.title("Harvey Outbound")
    st.write(message)
   
    
    name = 'Harvey'
    name_of_buyer = st.text_input('Name of buyer', value = 'John')
    email_of_buyer = st.text_input('Email of buyer', value = 'john@freshveggies.com')
    # buyer_company_name = st.text_input('Buyer company name', value = ' Fresh Vegetables Buyers, Inc.')
    priority_listing_email_delivered = st.text_input('Priority Listing Email Delivered ',value = '10')
    priority_listing_email_opened_count = st.text_input('Priority Listing Email Opened Count',value = '4')
    priority_listing_email_clicked_count = st.text_input('Priority Listing Email Clicked Count ',value = '6')
    produce_commodity_in_the_ple = st.text_input('Produce commodity in the PLE',value = 'Apple')
    produce_variety_in_the_ple = st.text_input('Produce variety in the PLE',value = 'fuji')
    produce_pack_type_from_the_supplier_in_the_ple = st.text_input('Produce pack type from the supplier in the PLE',value = 'carton')
    produce_cost_per_pack_in_the_ple = st.text_input('Produce cost per pack in the PLE',value = '12')
    price_per_carton = st.text_input('Price per carton',value = '48')
    produce_total_available_volume_from_the_supplier_in_the_ple = st.text_input('Produce total available volume from the supplier in the PLE',value = '4800')
    produce_available_date_from_the_supplier_in_the_ple = st.text_input('Produce available date from the supplier in the PLE',value = 'December 1st, 2023')
    produce_growing_method_from_the_supplier_in_the_ple= st.text_input('Produce growing method from the supplier in the PLE',value = 'Organic')
    produce_price_from_the_supplier_in_the_ple = st.text_input('Produce price from the supplier in the PLE' , value= '10')
    produce_priority_listing_link_for_purchase = st.text_input('Produce priority listing link for purchase',value = 'fullharvestplelink.com')
    full_harvest_account_executive_email_tied_to_the_buyer = st.text_input('Full Harvest Account executive email tied to the buyer',value = 'accountexecutive@fullharvest.com')
    priority_listing_purchase_status = st.text_input('Priority Listing Purchase Status',value = 'not purchased')
    priority_listing_has_pictures = st.text_input('Supplier city where the produce is shipping from',value = 'no')
    produce_grade_from_the_supplier_in_the_ple = st.text_input('Produce grade from the supplier in the PLE',value = 'A+')
    produce_pack_amount_per_pack_type_from_the_supplier_in_the_ple = st.text_input('Produce pack amount per pack type from the supplier',value = 4)
    produce_description = st.text_input('Produce description',value = "Best Apple in the world")
    supplier_city_where_the_produce_is_shipping_from = st.text_input('Supplier city where the produce is shipping from',value = "Denver, CO")

    api_data= {
            "name" : name,
            "name_of_buyer": name_of_buyer,
            "email_of_buyer": email_of_buyer,
            "phone_number_of_buyer":  "+13372219750",
            "booking_link" : "accountexecutive_bookinglink.com",
            "priority_listing_email_delivered": priority_listing_email_delivered,
            "priority_listing_email_opened_count": priority_listing_email_opened_count,
            "priority_listing_email_clicked_count": priority_listing_email_clicked_count,
            "produce_commodity_in_the_ple": produce_commodity_in_the_ple,
            "produce_variety_in_the_ple": produce_variety_in_the_ple,
            "produce_pack_type_from_the_supplier_in_the_ple": produce_pack_type_from_the_supplier_in_the_ple,
            "produce_cost_per_pack_in_the_ple": produce_cost_per_pack_in_the_ple,
            "price_per_carton": price_per_carton,
            "produce_total_available_volume_from_the_supplier_in_the_ple": produce_total_available_volume_from_the_supplier_in_the_ple,
            "produce_available_date_from_the_supplier_in_the_ple": produce_available_date_from_the_supplier_in_the_ple,
            "produce_growing_method_from_the_supplier_in_the_ple": produce_growing_method_from_the_supplier_in_the_ple,
            "produce_price_from_the_supplier_in_the_ple": produce_price_from_the_supplier_in_the_ple,
            "produce_priority_listing_link_for_purchase": produce_priority_listing_link_for_purchase,
            "full_harvest_account_executive_email_tied_to_the_buyer": full_harvest_account_executive_email_tied_to_the_buyer,
            "priority_listing_purchase_status": priority_listing_purchase_status,
            "priority_listing_has_pictures": priority_listing_has_pictures,
            "produce_grade_from_the_supplier_in_the_ple":produce_grade_from_the_supplier_in_the_ple,
            "produce_pack_amount_per_pack_type_from_the_supplier_in_the_ple": produce_pack_amount_per_pack_type_from_the_supplier_in_the_ple,
            "produce_description": produce_description,
            "supplier_city_where_the_produce_is_shipping_from" :supplier_city_where_the_produce_is_shipping_from
  
        }

    if st.button('Click to Start or Restart'):
        data, count = supabase.table("bots_dev").select("*").eq("id", 'outbound_harvey_email').execute() 
        bot_info = data[1][0]
        system_prompt = bot_info['system_prompt']  
        initial_text = bot_info['initial_text'] 
        initial_text =initial_text.format(name_of_buyer = api_data['name_of_buyer'], grade=api_data['produce_grade_from_the_supplier_in_the_ple'], produce_growing_method_from_the_supplier_in_the_ple =api_data['produce_growing_method_from_the_supplier_in_the_ple'], produce_variety_in_the_ple=api_data['produce_variety_in_the_ple'], produce_commodity_in_the_ple=api_data['produce_commodity_in_the_ple'], produce_cost_per_pack_in_the_ple=api_data['produce_cost_per_pack_in_the_ple'], pack_size=api_data['produce_pack_type_from_the_supplier_in_the_ple'],location_variable =api_data['supplier_city_where_the_produce_is_shipping_from'], produce_price_from_the_supplier_in_the_ple = api_data['produce_price_from_the_supplier_in_the_ple'])

        system_prompt = system_prompt.format(**api_data)

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
    userresponse = st.text_area("Enter your message", height = 300)
    

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
        messages, count = ideator(messages, api_data)

        #append to database
        with open('database.jsonl', 'a') as f:
                for i in range(count):
                    f.write(json.dumps(messages[-count + i]) + '\n')



        # Display the response in the chat interface
        string = ""

        for message in messages[1:]:
            if 'This is a secret internal thought' not in str(message):
                string = string + message["role"] + ": " + message["content"] + "\n\n"
        st.markdown(string)
        

if __name__ == '__main__':
    main()
