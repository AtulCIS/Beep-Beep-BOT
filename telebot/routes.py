from flask import request
import telegram
from telebot.credentials import (
    bot_token,
    URL,
    api_key_for_weather,
    api_key_for_news,
)
import requests
import json
from telebot.service import (
    send_message,
    is_name,
    is_location,
    removing_extra_from_name,
    is_location_correct,
    get_state_and_countryname,
    append_in_json,
    write_in_json,
    read_in_json,
)
from telebot import app

global bot
global TOKEN
global user_name
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)


@app.route("/{}".format(TOKEN), methods=["POST"])
def chatbot():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode("utf-8").decode()

    # for starting the conversation by /start command
    if text == "/start":
        bot_welcome = """
        Welcome to ChatBot, This chatbot can provide you the weather and top3 news as per your location.I am BeepBeepbot, what is your name (Please enter your name in @name format)?"""
        # send the welcoming message
        send_message(bot_welcome, chat_id, msg_id)

    # for performing actions when name will be given in a format
    elif is_name(text):
        user_name = removing_extra_from_name(text)
        user_intro = (
            "Hello " + user_name + ". Please enter your location(like indore,india)."
        )
        # send the Introductory message
        send_message(user_intro, chat_id, msg_id)

    # for replying as per the greeting of the user
    elif text.upper() == "HELLO" or text.upper() == "HEY" or text.upper() == "HI":
        bot_intro = "Hello I am ChatBot. What is your first name (Please enter your name in (@name) format)?"
        # send the welcoming message
        send_message(bot_intro, chat_id, msg_id)

    # for taking the location and replying as per the location.
    elif is_location(text):
        user_id_in_location = update.message.from_user.id
        if is_location_correct(text):
            write_in_json(user_id_in_location, text)
            actions = (
                "Please enter commands for choosing the action.\n1./Weather\n2./News"
            )
            send_message(actions, chat_id, msg_id)

            contents = read_in_json()
            if contents:
                location_obj = contents['location_user']
                for i, dicts in enumerate(location_obj) :
                    if str(user_id_in_location) == str(dicts['user_id']):
                        dicts['location'] = text

                        location_obj[i] = dicts

                        my_dict = {"location_user": location_obj}

                        with open('holdlocation.json', 'w') as f:
                            json.dump(my_dict,f)
                        break
                    else:
                        append_in_json(read_in_json() ,user_id_in_location, text)
            else:
                write_in_json(user_id_in_location, text)
        else:
            send_message("Please enter correct location", chat_id, msg_id)
    # for giving the weather information as per the location
    elif text == "/Weather":
        contents = read_in_json()
        user_id_in_weather = update.message.from_user.id
        if contents:
            for location_dict in contents['location_user']:
                if str(location_dict['user_id']) == str(user_id_in_weather):
                    location = location_dict['location']
                    if str(location) != "":
                        url = (
                            "https://api.weatherbit.io/v2.0/current?city="
                            + location
                            + ",NC&key="
                            + api_key_for_weather
                            + ""
                        )
                        city_country = location.split(",")
                        try:
                            weather_response = requests.get(url=url)
                            weather_results = json.loads(weather_response.text)
                            weather = (
                                "The Weather for "
                                + city_country[0]
                                + "("
                                + city_country[-1]
                                + ")"
                                + "is:"
                                + "\n\n-Weather:"
                                + str(weather_results["data"][0]["weather"]["description"])
                                + "\n\n-Wind speed:"
                                + str(weather_results["data"][0]["wind_spd"])
                                + "\n\n-Clouds:"
                                + str(weather_results["data"][0]["clouds"])
                                + "\n\n-Temperature:"
                                + str(weather_results["data"][0]["temp"])
                                + "°C"
                                + "\n\n-vis:"
                                + str(weather_results["data"][0]["vis"])
                                + "\n\n-aqi:"
                                + str(weather_results["data"][0]["aqi"])
                            )
                            send_message(weather, chat_id, msg_id)
                        except Exception as e:
                            error_msg = "Please enter location like (city,country)"
                            send_message(error_msg, chat_id, msg_id)
                else:
                    send_message("Please enter a location!", chat_id, msg_id)

    # for giving the Top 3 news as per the country
    elif text == "/News":
        contents = read_in_json()
        user_id_in_weather = update.message.from_user.id
        if contents:
            for location_dict in contents['location_user']:
                if str(location_dict['user_id']) == str(user_id_in_weather):
                    location = location_dict['location']
                    if str(location) != "":
                        getting_state_country = get_state_and_countryname(location)
                        city_country = location.split(",")
                        if len(getting_state_country["code"]) != 0:
                            country = getting_state_country["code"]
                            url = (
                                "https://newsapi.org/v2/top-headlines?country="
                                + country
                                + "&category=business&apiKey="
                                + api_key_for_news
                                + ""
                            )
                            try:
                                value_response = requests.get(url=url)
                                value_results = json.loads(value_response.text)
                                all_articles = value_results["articles"]
                                news1 = all_articles[0]["description"]
                                news2 = all_articles[1]["description"]
                                news3 = all_articles[3]["description"]
                                news = (
                                    "The News for "
                                    + city_country[-1]
                                    + " is:\n\n*"
                                    + news1
                                    + "\n\n*"
                                    + news2
                                    + "\n\n*"
                                    + news3
                                )
                                send_message(news, chat_id, msg_id)
                            except:
                                error_msg = "Please enter location like (city,country)"
                                send_message(error_msg, chat_id, msg_id)
                        else:
                            location_error_msg = "Please enter location like (city,country)"
                            send_message(location_error_msg, chat_id, msg_id)
                else:
                    send_message("Please enter a location!", chat_id, msg_id)
    # setting the default response as a starting command
    else:
        starting_command = "Start your chat with BeepBeepbot. Please click /start"
        send_message(starting_command, chat_id, msg_id)
    return "ok"


# for getting the updates at every request
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    s = bot.setWebhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

# to check the server is running or not
@app.route("/")
def index():
    return "it is working"

