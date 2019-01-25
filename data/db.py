#!/Users/gb6366/anaconda/bin/python2.7

# 1) Download file to tmp
# 2) Parse files
# 3) Update the dadabase
# pip install requests

import matplotlib
matplotlib.use('Agg')

from datetime import date, timedelta
import urllib2
import csv, StringIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os
import re
import pymysql




tags = {
          "CONSUMPTION": "all",
          "AIRCON": "air-conditioning",
          "FAN": "fan",
          "HEATER": "heater",
          "ENTERTAINMENT": "entertainement",
          "AUDIO_EQPT": "audio-equipment",
          "GAMES_CONSOLE": "games-console",
          "SET_TOP_BOX": "set-top-box",
          "TV": "tv",
          "TV_2": "tv-2",
          "DVD": "dvd-player",
          "BLURAY": "bluray-player",
          "CHARGER": "charger",
          "ALARM_CLOCK": "alarm-clock",
          "TELEPHONE": "telephone",
          "KITCHEN_EQPT": "kitchen-equipment",
          "COFFEE_MACHINE": "coffe-machine",
          "KETTLE": "kettle",
          "TOASTER": "toaster",
          "MICROWAVE": "microwave",
          "HOB": "hob",
          "OVEN": "oven",
          "IRON": "iron",
          "APPLIANCE": "appliance",
          "FREEZER": "freezer",
          "FRIDGE": "fridge",
          "WASHING_MACHINE": "washing-machine",
          "DISHWASHER": "dishwasher",
          "CLOTHES_DRIER": "tumble-dryer",
          "GARDEN_EQPT": "gardern-equipment",
          "POWER_TOOLS": "power-tool",
          "LAWN_MOWER": "lawn-mower",
          "COMPUTING_EQPT": "computing-equipment",
          "PC": "computer",
          "PC_2": "computer-2",
          "PRINTER": "printer",
          "SCANNER": "scanner",
          "LIGHTING": "lighting",
          "LAMP": "lamp",
          "LAMP_2": "lamp-2",
          "LAMP_3": "lamp-3",
          "HEALTH_BEAUTY": "health-beauty",
          "HAIR_DRIER": "hair-dryer",
          "HAIR_STRAIGHTENER": "hair-straightener",
          "AQUATICS_EQPT": "aquatic-equpment",
          "UNLABELLED_PLUG": "unlabelled"
        }

tagsIds = {
          0: "CONSUMPTION",
          1: "AIRCON",
          2: "FAN",
          3: "HEATER",
          21: "ENTERTAINMENT",
          22: "AUDIO_EQPT",
          23: "GAMES_CONSOLE",
          24: "SET_TOP_BOX",
          25: "TV",
          26: "TV_2",
          227: "DVD",
          28: "BLURAY",
          29: "CHARGER",
          30: "ALARM_CLOCK",
          31: "TELEPHONE",
          41: "KITCHEN_EQPT",
          42: "COFFE_MACHINE",
          43: "KETTLE",
          44: "TOASTER",
          45: "MICROWAVE",
          46: "HOB",
          47: "OVEN",
          48: "IRON",
          51: "APPLIANCE",
          52: "FREEZER",
          53: "FRIDGE",
          54: "WASHING_MACHINE",
          55: "DISHWASHER",
          56: "CLOTHES_DRIER",
          61: "GARDEN_EQPT",
          62: "POWER_TOOLS",
          63: "LAWN_MOWER",
          71: "COMPUTING_EQPT",
          72: "PC",
          73: "PC_2",
          74: "PRINTER",
          75: "SCANNER",
          81: "LIGHTING",
          82: "LAMP",
          83: "LAMP_2",
          84: "LAMP_3",
          91: "HEALTH_BEAUTY",
          92: "HAIR_DRYER",
          93: "HAIR_STRIGHTENER",
          96: "AQUATICS_EQPT",
          99: "UNLABELLED_PLUG"
}


def insertCSV(dat, username, password, host, port, dbname):
        connection = pymysql.connect(host=host, user=username, password=password, db=dbname, cursorclass=pymysql.cursors.DictCursor)

        for row_index, row in dat.iterrows():
                concept =  tags.get(tagsIds.get(row.Type,"UNLABELLED_PLUG"),"unlabelled")
                try:
                        with connection.cursor() as cursor:
                                sql = "INSERT INTO eusers_energyconsumption (email, timestamp, concept, consumption) VALUES (%s, %s, %s, %s)"
                                cursor.execute(sql, ( row.UserID,  row.EpochID,  concept, row.DeltaConsumption))
                                connection.commit()
                except Exception as e:
                        print "Error inserting: " + str(( row.UserID,  row.EpochID,  concept, row.DeltaConsumption))
                        pass

        connection.close()

def insertURL(url, username, password, host, port, dbname):
        response = urllib2.urlopen(url)
        data = response.read()
        dat = pd.read_csv(StringIO.StringIO(data))
        insertCSV(dat, username, password, host, port, dbname)

def insertDir(dir, username, password, host, port, dbname):
        files = glob.glob(dir + "Epoch*.csv")
        for f in files:
                print "Processing: " + f
                dat = pd.read_csv(f)
                insertCSV(dat, username, password, host, port, dbname)

