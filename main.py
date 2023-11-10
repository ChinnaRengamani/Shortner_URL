import random
import string
from pymongo import MongoClient
import os
import qrcode
import base64
db_url = os.environ.get("DATABASE_URL", "")
character = string.digits + string.ascii_letters

from os import getenv
from dotenv import load_dotenv

load_dotenv('config.env', override=True)
Domain = getenv('Domain', '')

m_client = MongoClient(db_url)
db = m_client['Shortner']
collection = db['Urls']
users=db['Users']
keywords=['login','signup','dashboard']
#url= input("Please enter the url: ")
code =''
for _ in range(0,6):
    code += "".join(random.choices(character))
def insert(url):
    code =''
    for _ in range(0,6):
        code += "".join(random.choices(character))
    document = {'code':code,'url':url}
    if collection.find_one({'code':code}):
        return "already in db"
    collection.insert_one(document)
    return f'{Domain}/{code}'


def retrive(code):
    if str(code) in keywords: 
        return code
    elif code[-1] == "+":
        code= code.replace('+','')
    r = collection.find_one({'code':code})
    try:
        return r['url']
    except: 
        return False;
    

def add_user(user1,password):
    if users.find_one({"username":user1}):
        return False
    document = {"username":user1,'Password':password}
    users.insert_one(document)
def check_user(user1,password):
    p = users.find_one({"username":user1})
    if p:
        if p['username'] != user1 or p['Password'] != password:
            return False
        elif p['username'] == user1 and p['Password'] == password:
            return True
    else:
        return "signup"

def user_data(user):
    return users.find_one({'username':user})
    

def user_insert(user,url,code):
    p = users.find_one({'username':user})
    update_data = {
            "$set": {
                code: url
            }
        }
    users.update_one({'username':user},update_data)


def qrcode1(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('r.png')
    binary_fc = open('r.png', 'rb').read()
    base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')
    dataurl = f'data:image/png;base64,{base64_utf8_str}'
    return dataurl

