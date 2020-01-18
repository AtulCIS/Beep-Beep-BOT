# Beep Beep Bot Bot

This is a telegram chatbot. It addresses the user by user name and asks about the location of the user and gives weather information and Top 3 News of the country of that location.


## Installation

This is a bot so this application needs to be on a live server. I am assuming that the live server is Heroku and you have the Heroku account. 

* Firstly you need to have [Telegram](https://web.telegram.org/#/login) and [Heroku](https://id.heroku.com/login) accounts and you have to create the bot on telegram.
* To create a bot on telegram, search BotFather and follow the instructions to create the bot.
* Once you created your Bot with BotFather. It will give you a token. This token will be required later.
* Clone this repository.
* **We have used some API's to get location, weather, and news.**
  * For Location: https://geocode.xyz
  * For Weather: https://www.weatherbit.io/
  * For News: https://newsapi.org
* You have to create the account on these and add credentials in credentials.py with your bot token.
* Now Heroku login to Heroku account use Heroku CLI. Run Heroku login.
```
heroku login
```

* Once you logged in to the system, create an app in Heroku.
```
heroku create APPNAME --buildpack heroku/python
```
* This will give a url in which the app will run.
* Add this to credentials.py.
* and push this code to your Git Repository.
* After this push it on Heroku.
```
git push heroku master
```
* Once the build is successful. Your Bot will start its work.
* **requirement file and Procfile is required to run the app on the server.**

* **Our app is running here on the server** :
[https://telegramdeep2.herokuapp.com/](https://telegramdeep2.herokuapp.com/)
* **Bot Name** : BeepBeepbot

![BeepBeepbot](https://i.imgur.com/YWvH0nO.jpg)
