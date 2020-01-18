import requests
import json
import time
from telebot.credentials import (
    bot_token,
)
import telegram

global bot
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)


# send_message() is using to sending the message on the bot
def send_message(msg, chat_id, msg_id):
    bot.sendChatAction(chat_id=chat_id, action="typing")
    time.sleep(1.5)
    bot.sendMessage(chat_id=chat_id, text=msg, reply_to_message_id=msg_id)


# is_name() is taking a text and checking whether it is containing @ or not
def is_name(text):
    if text.__contains__("@"):
        return True
    else:
        return False


# is it used for appending the data of the new user into the file
def append_in_json(data, user_id, location):
    data['location_user'].append(
        {
          'user_id': user_id,
          'location': location,
        }
        )
    with open('holdlocation.json', 'a') as f:
        json.dump(data, f)

    read_in_json()


# writing data into the file
def write_in_json(user_id,location):
    data = {'location_user': []}
    data['location_user'].append(
        {
          'user_id': user_id,
          'location': location,
        }
        )
    with open('holdlocation.json', 'w') as f:
        json.dump(data, f)


# for read into the file and return it as an object
def read_in_json():
    with open('holdlocation.json') as f:
        file_obj = f.read()
        if file_obj != '{}':
            f.seek(0)  # it may be redundant but it does not hurt
            json_obj = json.loads(file_obj)
            return json_obj
        else:
            return False


# is_location() is taking a text and checking whether it is containing location: or not
def is_location(text):
    count_of_commas = 0
    for c in text:
        if c == ",":
            count_of_commas = count_of_commas + 1
    if count_of_commas > 1:
        return False
    elif count_of_commas == 1:
        return True


# removing_extra_from_name() is taking a text removing a particular character
def removing_extra_from_name(text):
    if text.__contains__("@"):
        return text.replace("@", "")


# get_state_and_countryname() is taking location and returning the location in the particular format
def get_state_and_countryname(geolocation):
    if geolocation != "":
        url_for_geolocation = "https://geocode.xyz/" + geolocation + "?json=1"
        geolocation_response = requests.get(url=url_for_geolocation)
        geolocation_results = json.loads(geolocation_response.text)
        if len(geolocation_results["standard"]["city"]) == 0:
            geolocation = {"code": {}}
            return geolocation
        else:
            geolocation = {"code": geolocation_results["standard"]["prov"]}
            return geolocation

# for checking the location is right or not
def is_location_correct(geolocation):
    if geolocation != "":
        url_for_geolocation = "https://geocode.xyz/" + geolocation + "?json=1"
        geolocation_response = requests.get(url=url_for_geolocation)
        geolocation_results = json.loads(geolocation_response.text)
        if len(geolocation_results["standard"]["city"]) == 0:
            return False
        else:
            return True
    else:
        return False
