from flask import Flask
# import routes
app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

from telebot import routes