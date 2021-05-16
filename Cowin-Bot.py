from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
from datetime import date , timedelta
from time import sleep
import requests
import json

#Insert your Telegram Bot token here
TOKEN = ""

# Insert pincode here
PINCODE = ""

# Insert search term/keyword here
SEARCH_WORD = ""

# User-Agent to bypass bot detection mechanism of Cowin
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0" ,
    "Accept-Language": "hi_IN"
}

# Asynchronous function which once started queries the Cowin API for slots available for next 5 days every 5 mins
@run_async
def check_slots(update , context):
    update.message.reply_text("[+]Bot started!")
    while True:
        for day in range(0,5):
            DATE = (date.today() + timedelta(days = day)).strftime("%d-%m-%Y")
            API_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
            try:
                res = requests.get(url = API_URL , headers = headers)
            except Exception as e:
                print(e)

            if res.status_code == 200:
                json_data = json.loads(res.text)
                if len(json_data["sessions"]):
                    for session in json_data["sessions"]:
                        if SEARCH_WORD in session["name"].lower() and session["available_capacity"] > 0: # and session["min_age_limit"] <= 18:
                            slot_available_msg = f"{session['vaccine']} vaccination slot available for {session['available_capacity']} people on {session['date']} at {session['name']}\n"
                            update.message.reply_text(slot_available_msg)
            sleep(30)
        sleep(5 * 60)


# Asynchronous function to manually check for slots at any point of time. This won't block the check_slots function
@run_async
def check(update , context):
    found = False
    DATE = date.today().strftime("%d-%m-%Y")
    if len(update.message.text.strip()) > 5:
        SEARCH_WORD = update.message.text.strip().split()[1]
        API_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
        try:
            res = requests.get(url = API_URL , headers = headers)
        except Exception as e:
            print(e)

        if res.status_code == 200:
            json_data = json.loads(res.text)
            if len(json_data["sessions"]):
                for session in json_data["sessions"]:
                    if SEARCH_WORD in session["name"].lower() and session["available_capacity"] > 0: # and session["min_age_limit"] <= 18:
                        slot_available_msg = f"{session['vaccine']} vaccination slot available for {session['available_capacity']} people on {session['date']} at {session['name']}\n"
                        update.message.reply_text(slot_available_msg)
                        found = True
                if not found:
                    update.message.reply_text(f"No slot found for the term {SEARCH_WORD} in Pin:{PINCODE}")
            else:
                update.message.reply_text(f"No sessions found for  Pin:{PINCODE}")
            
        else:
            update.message.reply_text("[+]Request was not successful!")

# Function to display help menu
@run_async
def help(update , context):
    help_msg = '''This is a telegram bot created by @xscorp for automating vaccination slot alert. It utilizes Cowin API and Telegram API to do this.\n
It queries the Cowin API for 5 days starting from the current date with a break of 5 minutes after every set of HTTP requests.\n
Please note that it only checks slots for these conditions-\n
Age >= 18\n
Pin = 248140\n

There are 3 vaccination centers for the Pin 248140-\n
1. CHC Doiwala\n
2. Ganpati Wedding P.Bhaniyawala\n
3. Dudhli\n

This bot searches for "ganpati" keyword. And hence, whenever there are any vaccination slots available ub "Ganpati Wedding P.Bhaniyawala", it pings you on telegram.\n
To update this keyword for a single request, type:\n
"/check <keyword>"\n
Example: "/check doiwala"\n
'''
    update.message.reply_text(help_msg)


def main():
    updater = Updater(token = TOKEN , use_context = True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("check_slots" , check_slots))
    dp.add_handler(CommandHandler("check" , check))
    dp.add_handler(CommandHandler("help" , help))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
