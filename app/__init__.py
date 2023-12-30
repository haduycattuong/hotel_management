from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = "cattuong" 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hotel?charset=utf8mb4" % quote('kuuhaku611')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

#config cloudinary to upload images
cloudinary.config( 
  cloud_name = "dzvzu6udg", 
  api_key = "699726166611635", 
  api_secret = "hadfJzbdPf8F1qHbU8ZHX6Iv7RY" 
)

db = SQLAlchemy(app=app)
login = LoginManager(app=app)