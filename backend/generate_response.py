import pymongo
import pandas as pd
from pandas import DataFrame
from tabulate import tabulate
from dotenv import load_dotenv
import json
import sys
import os

sys.path.append(os.path.dirname(__file__))

load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")



CONNECTION_STRING = "mongodb+srv://"+username+":"+password+"@cluster0.1zo8noj.mongodb.net/test"
client = pymongo.MongoClient(CONNECTION_STRING)

db = client["TF"]
uk_dining_retail = db["UK_dining_retail"]
item_details = uk_dining_retail.find()
df_uk_dining_retail = DataFrame(item_details).drop('_id', axis=1)

uk_dining_trade = db["UK_dining_trade"]
item_details = uk_dining_trade.find()
df_uk_dining_trade = DataFrame(item_details).drop('_id', axis=1)


def process(email):
    if email=="":
        return ""
    try:
        data=json.loads(email)
        new_df=None
        if data['tradeRetail']=='retail':
            new_df = df_uk_dining_retail[(df_uk_dining_retail['model'].str.contains(pat=data['model'])) & (df_uk_dining_retail['shape']==data['shape']) & (df_uk_dining_retail['size']==data['size'])]
        elif data['tradeRetail']=='trade':
            new_df = df_uk_dining_trade[(df_uk_dining_trade['model'].str.contains(pat=data['model'])) & (df_uk_dining_trade['shape']==data['shape']) & (df_uk_dining_trade['size']==data['size'])]
        return tabulate(new_df, showindex=False, headers=new_df.columns, maxcolwidths=[None, None, None, None, None, 30, 50, None])
    except Exception as e:
        print(e)
        return "Please enter valid format"

