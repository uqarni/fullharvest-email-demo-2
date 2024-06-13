# fullharvest-demo

python -m streamlit run main.py


# other stuff

<h1 align="center" id="title">FULL HARVEST HARVEY</h1>

# STEP 1 ensure python3.9 is installed
(these are instructions for mac, assuming homebrew is already installed)
brew install python@3.9
brew link python@3.9

# STEP 2 create virtual environment
python3.9 -m venv .venv

# STEP 3 activate environment for MacOs
source ./.venv/bin/activate (macos)

# activate environment for Windows
source ./.venv/Scripts/activate (window)

# STEP 4 install dependencies
pip install -r requirements.txt

# STEP 5 Setup Redis and Supabase
```
brew install redis
```

Create a new Supabase project in your own personal account (free)

Restore database schema in your personal Supabase instance
```
psql -h <supabase host> -p 5432 -d postgres -U <supabase user> < supabase_dev.dump
```

# STEP 6 setup .env file
copy .env_dev to .env

Copy over Supabase URL and Key from your project settings into the .env file

Add required ENV variables from DigitalOcean prod

# STEP 7 run unit tests
python3 -m pytest

# STEP 8 run application
uvicorn main:app --port=3000

# STEP 9 delete  yourself in supabase
go to supabase and make sure your phone number and test contact email dont exist in the messages table and the contacts table

# STEP 10 create a new inbound form fill contact
(change # and email to yours)
(this endpoint is in Zapier)
curl --location 'http://127.0.0.1:3000/v1/fh_new_contact' \
--header 'Content-Type: application/json' \
--data-raw '{
    "contactid":"test",
    "firstname":"John",
    "lastname":"Sangha",
    "companyname":"testcompany",
    "status":"Open",
    "leadtype":"Buyer",
    "phone":"+17372740771",
    "email":"uzair+apr27test@gp.com",
    "commodities":"apple",
    "initial_text":"Hey, this is Harvey from Full Harvest. Just saw your request come in regarding seasonal deliveries of apple. Am I speaking with John?",
    "growing_method":"organic",
    "need_availability":"seasonal"
}'

# STEP 11 send incoming SMS message
(change From # to yours)
(this endpoint is in Twilio)

curl --location 'http://127.0.0.1:3000/v1/fh_webhook' \
--form 'From="+17372740771"' \
--form 'To="+16509556151"' \
--form 'Body="can you share a booking link"'

# STEP 12 book a meeting with Justin
(change email to the same one as in #1)
(this endpoint is in Zapier)

curl --location 'http://127.0.0.1:3000/v1/fh_booking' \
--header 'Content-Type: application/json' \
--data-raw '{
    "contact_email" : "uzair+apr27test@gp.com",
    "start_time": "2024-01-12T13:14:15Z",
    "lead_timezone": "America/Los_Angeles",
    "reschedule_link": "https://go.oncehub.com/Elite&Params=IPLa6BkbZ-Q3D*rtWdSXOB-D6RvdTShkLvaH-7mTZO4!",
    "cancel_link": "https://",
    "description":"testing"
}'

# STEP 13 delete yourself in supabae
from messages from the messages table, contact from the contacts table in supabase
using your phone number

<h6 align="center" id="title">Powered By Gepeto</h6>
