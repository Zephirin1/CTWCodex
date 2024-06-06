from app import app, db
from flask import render_template, redirect, url_for
from app.forms import SearchForm, CompareForm
from app.models import Player
import grequests
import requests
import json
import math
import sqlalchemy as sa
from pprint import pprint

def getInfo(call):
    r = requests.get(call)
    return r.json()

# get the json response for player information from the Hypixel API
def autoGetInfo(API_KEY, name):
    call = f"https://api.hypixel.net/player?key={API_KEY}&name={name}"
    r = requests.get(call)
    return r.json()

# check if data exists in a dataset, if it does then return it, if it doesn't then return 0
def checkDataExists(dataPoint, data):
    if dataPoint in data:
        return data[dataPoint]
    else:
        return 0
    
# returns the API key
def getAPIKey():
    API_KEY = "b446d0d4-c982-4f49-942a-cf8acdd70ff0"
    return API_KEY
    
# return a dictionary of relevant CTW stats from a section of the API response
def getCTWData(data):
    dataDict = {
        "winrateInt": 0, 
        "winPercent": 0, 
        "winRatio": 0, 
        "wins": 0, 
        "losses": 0, 

        "caps": 0, 
        "capDeathRatio": 0, 
        "woolsStolen": 0, 
        "capSuccessRate": 0, 
        "capsPerGame": 0, 

        "kdr": 0, 
        "kills": 0, 
        "deaths": 0, 
        "assists": 0, 
        "killsPerGame": 0, 

        "huntingKDR": 0, 
        "huntingKills": 0, 
        "huntingDeaths": 0, 
        "huntingKillsPerGame": 0, 

        "woolholderKDR": 0, 
        "woolholderKills": 0, 
        "woolholderDeaths": 0, 

        "capPR": 0, 
        "draws": 0, 
        "winPR": 0, 

        "hotbarImageList": ['images/Stone_Sword.png', 'images/Iron_Pickaxe_JE3_BE2.png', 'images/Bow_JE2_BE1.png', 'images/Iron_Axe_JE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Golden_Apple_JE1_BE1.png', 'images/Arrow.png'], 
        "hotbarAltTextList": ["Sword", "Pickaxe", "Bow", "Axe", "Planks", "Planks", "Planks", "Golden Apple", "Arrows", "Empty"]
    }

    #win/loss data
    if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
        dataDict["winrateInt"] = checkDataExists("woolhunt_participated_wins", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data))
    dataDict["winPercent"] = round(dataDict["winrateInt"] * 100, 2)
    if checkDataExists("woolhunt_participated_losses", data) != 0:
        dataDict["winRatio"] = round(checkDataExists("woolhunt_participated_wins", data) / checkDataExists("woolhunt_participated_losses", data), 2)
    else:
        dataDict["winRatio"] = checkDataExists("woolhunt_participated_wins", data)
    dataDict["wins"] = checkDataExists("woolhunt_participated_wins", data)
    dataDict["losses"] = checkDataExists("woolhunt_participated_losses", data)

    #cap data
    dataDict["caps"] = checkDataExists("woolhunt_wools_captured", data)
    if checkDataExists("woolhunt_deaths", data) != 0:
        dataDict["capDeathRatio"] = round(checkDataExists("woolhunt_wools_captured", data) / checkDataExists("woolhunt_deaths", data), 2)
    else:
        dataDict["capDeathRatio"] = checkDataExists("woolhunt_wools_captured", data)
    dataDict["woolsStolen"] = checkDataExists("woolhunt_wools_stolen", data)
    if checkDataExists("woolhunt_wools_stolen", data) != 0:
        dataDict["capSuccessRate"] = round((checkDataExists("woolhunt_wools_captured", data) / checkDataExists("woolhunt_wools_stolen", data)) * 100, 2)
    if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
        dataDict["capsPerGame"] = round(checkDataExists("woolhunt_wools_captured", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data)), 2)
    else:
        dataDict["capsPerGame"] = checkDataExists("woolhunt_wools_captured", data)

    #general kill/death data
    if checkDataExists("woolhunt_deaths", data) != 0:
        dataDict["kdr"] = round(checkDataExists("woolhunt_kills", data) / checkDataExists("woolhunt_deaths", data), 2)
    else:
        dataDict["kdr"] = checkDataExists("woolhunt_kills", data)
    dataDict["kills"] = checkDataExists("woolhunt_kills", data)
    dataDict["deaths"] = checkDataExists("woolhunt_deaths", data)
    dataDict["assists"] = checkDataExists("woolhunt_assists", data)
    if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
        dataDict["killsPerGame"] = round(checkDataExists("woolhunt_kills", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data)), 2)
    else:
        dataDict["killsPerGame"] = checkDataExists("woolhunt_kills", data)

    #kill/death data against woolholder
    if checkDataExists("woolhunt_deaths_to_woolholder", data) != 0:
        dataDict["huntingKDR"] = round(checkDataExists("woolhunt_kills_on_woolholder", data) / checkDataExists("woolhunt_deaths_to_woolholder", data), 2)
    else:
        dataDict["huntingKDR"] = checkDataExists("woolhunt_kills_on_woolholder", data)
    dataDict["huntingKills"] = checkDataExists("woolhunt_kills_on_woolholder", data)
    dataDict["huntingDeaths"] = checkDataExists("woolhunt_deaths_to_woolholder", data)
    if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
        dataDict["huntingKillsPerGame"] = round(checkDataExists("woolhunt_kills_on_woolholder", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data)), 2)
    else:
        dataDict["huntingKillsPerGame"] = checkDataExists("woolhunt_kills_on_woolholder", data)

    #kill/death data as woolholder
    if checkDataExists("woolhunt_deaths_with_wool", data) != 0:
        dataDict["woolholderKDR"] = round(checkDataExists("woolhunt_kills_with_wool", data) / checkDataExists("woolhunt_deaths_with_wool", data), 2)
    else:
        dataDict["woolholderKDR"] = checkDataExists("woolhunt_kills_with_wool", data)
    dataDict["woolholderKills"] = checkDataExists("woolhunt_kills_with_wool", data)
    dataDict["woolholderDeaths"] = checkDataExists("woolhunt_deaths_with_wool", data)

    #miscellaneous data
    dataDict["capPR"] = checkDataExists("woolhunt_fastest_wool_capture", data)
    dataDict["draws"] = checkDataExists("woolhunt_participated_draws", data)
    dataDict["winPR"] = checkDataExists("woolhunt_fastest_win", data)

    #inventory layout data
    layoutData = checkDataExists("woolhunt_inventorylayout", data)
    if layoutData != 0:
        layoutDataKeys = list(layoutData.keys())
        layoutDataValues = list(layoutData.values())
    else:
        layoutDataKeys = 0
        layoutDataValues = 0
    inventoryList = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    imageList = ['images/Stone_Sword.png', 'images/Iron_Pickaxe_JE3_BE2.png', 'images/Bow_JE2_BE1.png', 'images/Iron_Axe_JE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Golden_Apple_JE1_BE1.png', 'images/Arrow.png', 'images/Empty.png']
    altTextList = ["Sword", "Pickaxe", "Bow", "Axe", "Planks", "Planks", "Planks", "Golden Apple", "Arrows", "Empty"]

    if layoutDataKeys != 0:
        count = 0
        for key in layoutDataKeys:
            inventoryList[int(key)] = layoutDataValues[count]
            count = count + 1


    if layoutData != 0:
        dataDict["hotbarImageList"] = []
        dataDict["hotbarAltTextList"] = []
        i = 0
        while i < 9:
            dataDict["hotbarImageList"].append(imageList[inventoryList[i]])
            dataDict["hotbarAltTextList"].append(altTextList[inventoryList[i]])
            i = i + 1
    
    return dataDict


# return a dictionary of relevant CTW stats from the specified player object in the database
def getCTWDataFromDatabase(name):
    dataDict = {
        "displayName": "",

        "winPercent": 0, 
        "winRatio": 0, 
        "wins": 0, 
        "losses": 0, 

        "caps": 0, 
        "capDeathRatio": 0, 
        "woolsStolen": 0, 
        "capSuccessRate": 0, 
        "capsPerGame": 0, 

        "kdr": 0, 
        "kills": 0, 
        "deaths": 0, 
        "assists": 0, 
        "killsPerGame": 0, 

        "huntingKDR": 0, 
        "huntingKills": 0, 
        "huntingDeaths": 0, 
        "huntingKillsPerGame": 0, 

        "woolholderKDR": 0, 
        "woolholderKills": 0, 
        "woolholderDeaths": 0, 

        "capPR": 0, 
        "draws": 0, 
        "winPR": 0, 

        "hotbarImageList": ['images/Stone_Sword.png', 'images/Iron_Pickaxe_JE3_BE2.png', 'images/Bow_JE2_BE1.png', 'images/Iron_Axe_JE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Golden_Apple_JE1_BE1.png', 'images/Arrow.png'], 
        "hotbarAltTextList": ["Sword", "Pickaxe", "Bow", "Axe", "Planks", "Planks", "Planks", "Golden Apple", "Arrows", "Empty"]
    }
    
    player = db.session.scalar(sa.select(Player).where(Player.playerName == name.lower()))

    dataDict["displayName"] = player.displayName

    dataDict["winPercent"] = player.winPercent
    dataDict["winRatio"] = player.winRatio
    dataDict["wins"] = player.wins
    dataDict["losses"] = player.losses

    dataDict["caps"] = player.caps
    dataDict["capDeathRatio"] = player.capDeathRatio
    dataDict["woolsStolen"] = player.woolsStolen
    dataDict["capSuccessRate"] = player.capSuccessRate
    dataDict["capsPerGame"] = player.capsPerGame

    dataDict["kdr"] = player.kdr
    dataDict["kills"] = player.kills
    dataDict["deaths"] = player.deaths
    dataDict["assists"] = player.assists
    dataDict["killsPerGame"] = player.killsPerGame

    dataDict["huntingKDR"] = player.huntingKDR
    dataDict["huntingKills"] = player.huntingKills
    dataDict["huntingDeaths"] = player.huntingDeaths
    dataDict["huntingKillsPerGame"] = player.huntingKillsPerGame

    dataDict["woolholderKDR"] = player.woolholderKDR
    dataDict["woolholderKills"] = player.woolholderKills
    dataDict["woolholderDeaths"] = player.woolholderDeaths

    dataDict["capPR"] = player.capPR
    dataDict["draws"] = player.draws
    dataDict["winPR"] = player.winPR

    dataDict["hotbarImageList"] = [player.hotbarImage1, player.hotbarImage2, player.hotbarImage3, player.hotbarImage4, player.hotbarImage5, player.hotbarImage6, player.hotbarImage7, player.hotbarImage8, player.hotbarImage9]
    dataDict["hotbarAltTextList"] = [player.hotbarAlt1, player.hotbarAlt2, player.hotbarAlt3, player.hotbarAlt4, player.hotbarAlt5, player.hotbarAlt6, player.hotbarAlt7, player.hotbarAlt8, player.hotbarAlt9]
    
    return dataDict





# Stores player data in the appropriate database object based on provided uuid, name data variables, and data dictionary
def storeData(uuid, name, displayName, dataDict):
    player = db.session.scalar(sa.select(Player).where(Player.uuid == uuid))
    if player is not None:
        player.playerName = name.lower()
        player.displayName = displayName
        player.pageTitle = displayName
        player.winPercent = str(dataDict["winPercent"])
        player.winRatio = str(dataDict["winRatio"])
        player.wins = str(dataDict["wins"])
        player.losses = str(dataDict["losses"])

        player.capDeathRatio = str(dataDict["capDeathRatio"])
        player.caps = str(dataDict["caps"])
        player.woolsStolen = str(dataDict["woolsStolen"])
        player.capSuccessRate = str(dataDict["capSuccessRate"])
        player.capsPerGame = str(dataDict["capsPerGame"])

        player.kdr = str(dataDict["kdr"])
        player.kills = str(dataDict["kills"])
        player.deaths = str(dataDict["deaths"])
        player.assists = str(dataDict["assists"])
        player.killsPerGame = str(dataDict["killsPerGame"])

        player.huntingKDR = str(dataDict["huntingKDR"])
        player.huntingKills = str(dataDict["huntingKills"])
        player.huntingDeaths = str(dataDict["huntingDeaths"])
        player.huntingKillsPerGame = str(dataDict["huntingKillsPerGame"])

        player.woolholderKDR = str(dataDict["woolholderKDR"])
        player.woolholderKills = str(dataDict["woolholderKills"])
        player.woolholderDeaths = str(dataDict["woolholderDeaths"])

        player.capPR = str(dataDict["capPR"])
        player.winPR = str(dataDict["winPR"])
        player.draws = str(dataDict["draws"])


        
        player.hotbarImage1 = str(dataDict["hotbarImageList"][0])
        player.hotbarImage2 = str(dataDict["hotbarImageList"][1])
        player.hotbarImage3 = str(dataDict["hotbarImageList"][2])
        player.hotbarImage4 = str(dataDict["hotbarImageList"][3])
        player.hotbarImage5 = str(dataDict["hotbarImageList"][4])
        player.hotbarImage6 = str(dataDict["hotbarImageList"][5])
        player.hotbarImage7 = str(dataDict["hotbarImageList"][6])
        player.hotbarImage8 = str(dataDict["hotbarImageList"][7])
        player.hotbarImage9 = str(dataDict["hotbarImageList"][8])

        player.hotbarAlt1 = str(dataDict["hotbarAltTextList"][0])
        player.hotbarAlt2 = str(dataDict["hotbarAltTextList"][1])
        player.hotbarAlt3 = str(dataDict["hotbarAltTextList"][2])
        player.hotbarAlt4 = str(dataDict["hotbarAltTextList"][3])
        player.hotbarAlt5 = str(dataDict["hotbarAltTextList"][4])
        player.hotbarAlt6 = str(dataDict["hotbarAltTextList"][5])
        player.hotbarAlt7 = str(dataDict["hotbarAltTextList"][6])
        player.hotbarAlt8 = str(dataDict["hotbarAltTextList"][7])
        player.hotbarAlt9 = str(dataDict["hotbarAltTextList"][8])

        db.session.commit()
    else:
        newPlayer = Player(playerName=name, uuid=uuid, displayName=displayName, pageTitle=displayName, winPercent=str(dataDict["winPercent"]), winRatio=str(dataDict["winRatio"]), wins=str(dataDict["wins"]), losses=str(dataDict["losses"]), 
                        capDeathRatio=str(dataDict["capDeathRatio"]), caps=str(dataDict["caps"]), woolsStolen=str(dataDict["woolsStolen"]), capSuccessRate=str(dataDict["capSuccessRate"]), capsPerGame=str(dataDict["capsPerGame"]), 
                        kdr=str(dataDict["kdr"]), kills=str(dataDict["kills"]), deaths=str(dataDict["deaths"]), assists=str(dataDict["assists"]), killsPerGame=str(dataDict["killsPerGame"]), 
                        huntingKDR=str(dataDict["huntingKDR"]), huntingKills=str(dataDict["huntingKills"]), huntingDeaths=str(dataDict["huntingDeaths"]), huntingKillsPerGame=str(dataDict["huntingKillsPerGame"]), 
                        woolholderKDR=str(dataDict["woolholderKDR"]), woolholderKills=str(dataDict["woolholderKills"]), woolholderDeaths=str(dataDict["woolholderDeaths"]), capPR=str(dataDict["capPR"]), winPR=str(dataDict["winPR"]), draws=str(dataDict["draws"]), 
                        hotbarImage1=str(dataDict["hotbarImageList"][0]), hotbarImage2=str(dataDict["hotbarImageList"][1]), hotbarImage3=str(dataDict["hotbarImageList"][2]), hotbarImage4=str(dataDict["hotbarImageList"][3]), hotbarImage5=str(dataDict["hotbarImageList"][4]), hotbarImage6=str(dataDict["hotbarImageList"][5]), hotbarImage7=str(dataDict["hotbarImageList"][6]), hotbarImage8=str(dataDict["hotbarImageList"][7]), hotbarImage9=str(dataDict["hotbarImageList"][8]), 
                        hotbarAlt1=str(dataDict["hotbarAltTextList"][0]), hotbarAlt2=str(dataDict["hotbarAltTextList"][1]), hotbarAlt3=str(dataDict["hotbarAltTextList"][2]), hotbarAlt4=str(dataDict["hotbarAltTextList"][3]), hotbarAlt5=str(dataDict["hotbarAltTextList"][4]), hotbarAlt6=str(dataDict["hotbarAltTextList"][5]), hotbarAlt7=str(dataDict["hotbarAltTextList"][6]), hotbarAlt8=str(dataDict["hotbarAltTextList"][7]), hotbarAlt9=str(dataDict["hotbarAltTextList"][8]))
        
        db.session.add(newPlayer)
        db.session.commit()

# generates data to be used for the player performance radar chart
def makeChartData(dataDict):
    winIndex = int(dataDict["wins"]) / (int((dataDict["wins"])) + int(dataDict["losses"]) + 1)
    killIndex = int(dataDict["kills"]) / (int(dataDict["kills"]) + int(dataDict["deaths"]) + 1)
    capIndex = (int(dataDict["caps"]) / (int(dataDict["woolsStolen"]) + 1)) * 1.6
    huntingIndex = int(dataDict["huntingKills"]) / (int(dataDict["huntingKills"]) + int(dataDict["huntingDeaths"]) + 1)

    return [winIndex, capIndex, huntingIndex, killIndex]



# form page to search for a specific player's data
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('player', playerName = form.playerName.data))
    return render_template('playerSearch.html', form=form)


# form page for player comparison (similar to /home page)
@app.route('/compare', methods=['GET', 'POST'])
def compareSearch():
    form = CompareForm()
    if form.validate_on_submit():
        return redirect(url_for('compare', playerName1 = form.playerName1.data, playerName2 = form.playerName2.data))
    return render_template('compareSearch.html', form=form)



@app.route('/player/<playerName>')
def player(playerName):
    try:
        try:
            API_KEY = getAPIKey()
            name = playerName

            name_link = f"https://api.hypixel.net/player?key={API_KEY}&name={name}"

            x = getInfo(name_link)

            uuid = str(x["player"]["uuid"]) 
            displayName = str(x["player"]["displayname"])
            data = x["player"]["stats"]["Arcade"]

            #skywarsWins = str(data["player"]["stats"]["SkyWars"]["wins"])  <-- example to get specific data from json

            #win/loss data
            if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
                winRateInt = checkDataExists("woolhunt_participated_wins", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data))
            else:
                 winRateInt = 0
            winPercent = str(round(winRateInt * 100, 2))
            if checkDataExists("woolhunt_participated_losses", data) != 0:
                winRatio = str(round(checkDataExists("woolhunt_participated_wins", data) / checkDataExists("woolhunt_participated_losses", data), 2))
            else:
                 winRatio = str(checkDataExists("woolhunt_participated_wins", data))
            wins = str(checkDataExists("woolhunt_participated_wins", data))
            losses = str(checkDataExists("woolhunt_participated_losses", data))

            #cap data
            caps = str(checkDataExists("woolhunt_wools_captured", data))
            if checkDataExists("woolhunt_deaths", data) != 0:
                capDeathRatio = str(round(checkDataExists("woolhunt_wools_captured", data) / checkDataExists("woolhunt_deaths", data), 2))
            else:
                 capDeathRatio = str(checkDataExists("woolhunt_wools_captured", data))
            woolsStolen = str(checkDataExists("woolhunt_wools_stolen", data))
            if checkDataExists("woolhunt_wools_stolen", data) != 0:
                capSuccessRate = str(round((checkDataExists("woolhunt_wools_captured", data) / checkDataExists("woolhunt_wools_stolen", data)) * 100, 2))
            else:
                capSuccessRate = "0"
            if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
                capsPerGame = str(round(checkDataExists("woolhunt_wools_captured", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data)), 2))
            else:
                 capsPerGame = str(checkDataExists("woolhunt_wools_captured", data))

            #general kill/death data
            if checkDataExists("woolhunt_deaths", data) != 0:
                kdr = str(round(checkDataExists("woolhunt_kills", data) / checkDataExists("woolhunt_deaths", data), 2))
            else:
                kdr = str(checkDataExists("woolhunt_kills", data))
            kills = str(checkDataExists("woolhunt_kills", data))
            deaths = str(checkDataExists("woolhunt_deaths", data))
            assists = str(checkDataExists("woolhunt_assists", data))
            if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
                killsPerGame = str(round(checkDataExists("woolhunt_kills", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data)), 2))
            else:
                killsPerGame = str(checkDataExists("woolhunt_kills", data))

            #kill/death data against woolholder
            if checkDataExists("woolhunt_deaths_to_woolholder", data) != 0:
                huntingKDR = str(round(checkDataExists("woolhunt_kills_on_woolholder", data) / checkDataExists("woolhunt_deaths_to_woolholder", data), 2))
            else:
                huntingKDR = str(checkDataExists("woolhunt_kills_on_woolholder", data))
            huntingKills = str(checkDataExists("woolhunt_kills_on_woolholder", data))
            huntingDeaths = str(checkDataExists("woolhunt_deaths_to_woolholder", data))
            if checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data) != 0:
                huntingKillsPerGame = str(round(checkDataExists("woolhunt_kills_on_woolholder", data) / (checkDataExists("woolhunt_participated_wins", data) + checkDataExists("woolhunt_participated_losses", data)), 2))
            else:
                huntingKillsPerGame = str(checkDataExists("woolhunt_kills_on_woolholder", data))

            #kill/death data as woolholder
            if checkDataExists("woolhunt_deaths_with_wool", data) != 0:
                woolholderKDR = str(round(checkDataExists("woolhunt_kills_with_wool", data) / checkDataExists("woolhunt_deaths_with_wool", data), 2))
            else:
                woolholderKDR = str(checkDataExists("woolhunt_kills_with_wool", data))
            woolholderKills = str(checkDataExists("woolhunt_kills_with_wool", data))
            woolholderDeaths = str(checkDataExists("woolhunt_deaths_with_wool", data))

            #miscellaneous data
            capPR = str(checkDataExists("woolhunt_fastest_wool_capture", data))
            draws = str(checkDataExists("woolhunt_participated_draws", data))
            winPR = str(checkDataExists("woolhunt_fastest_win", data))

            #inventory layout data
            layoutData = checkDataExists("woolhunt_inventorylayout", data)
            if layoutData != 0:
                layoutDataKeys = list(layoutData.keys())
                layoutDataValues = list(layoutData.values())
            else:
                layoutDataKeys = 0
                layoutDataValues = 0
            inventoryList = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
            imageList = ['images/Stone_Sword.png', 'images/Iron_Pickaxe_JE3_BE2.png', 'images/Bow_JE2_BE1.png', 'images/Iron_Axe_JE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Golden_Apple_JE1_BE1.png', 'images/Arrow.png', 'images/Empty.png']
            altTextList = ["Sword", "Pickaxe", "Bow", "Axe", "Planks", "Planks", "Planks", "Golden Apple", "Arrows", "Empty"]

            if layoutDataKeys != 0:
                count = 0
                for key in layoutDataKeys:
                    inventoryList[int(key)] = layoutDataValues[count]
                    count = count + 1


            if layoutData != 0:
                hotbarImageList = []
                hotbarAltTextList = []
                i = 0
                while i < 9:
                    hotbarImageList.append(imageList[inventoryList[i]])
                    hotbarAltTextList.append(altTextList[inventoryList[i]])
                    i = i + 1
            else:
                hotbarImageList = ['images/Stone_Sword.png', 'images/Iron_Pickaxe_JE3_BE2.png', 'images/Bow_JE2_BE1.png', 'images/Iron_Axe_JE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Golden_Apple_JE1_BE1.png', 'images/Arrow.png']
                hotbarAltTextList = ["Sword", "Pickaxe", "Bow", "Axe", "Planks", "Planks", "Planks", "Golden Apple", "Arrows"]

            #Making values to be used in player radar chart
            playerWinIndex = winRateInt
            playerKillIndex = int(kills) / (int(kills) + int(deaths) + 1)
            playerHuntingIndex = int(huntingKills) / (int(huntingKills) + int(huntingDeaths) + 1)
            playerCapIndex = (int(caps) / (int(woolsStolen) + 1)) * 1.6

            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            radarValues = [playerWinIndex, playerCapIndex, playerHuntingIndex, playerKillIndex]


            #deal with entering all this information into the database
            player = db.session.scalar(sa.select(Player).where(Player.uuid == uuid))
            if player is not None:
                player.playerName = name.lower()
                player.displayName = displayName
                player.pageTitle = displayName
                player.winPercent = winPercent
                player.winRatio = winRatio
                player.wins = wins
                player.losses = losses

                player.capDeathRatio = capDeathRatio
                player.caps = caps
                player.woolsStolen = woolsStolen
                player.capSuccessRate = capSuccessRate
                player.capsPerGame = capsPerGame

                player.kdr = kdr
                player.kills = kills
                player.deaths = deaths
                player.assists = assists
                player.killsPerGame = killsPerGame

                player.huntingKDR = huntingKDR
                player.huntingKills = huntingKills
                player.huntingDeaths = huntingDeaths
                player.huntingKillsPerGame = huntingKillsPerGame

                player.woolholderKDR = woolholderKDR
                player.woolholderKills = woolholderKills
                player.woolholderDeaths = woolholderDeaths

                player.capPR = capPR
                player.winPR = winPR
                player.draws = draws

                player.hotbarImage1 = hotbarImageList[0]
                player.hotbarImage2 = hotbarImageList[1]
                player.hotbarImage3 = hotbarImageList[2]
                player.hotbarImage4 = hotbarImageList[3]
                player.hotbarImage5 = hotbarImageList[4]
                player.hotbarImage6 = hotbarImageList[5]
                player.hotbarImage7 = hotbarImageList[6]
                player.hotbarImage8 = hotbarImageList[7]
                player.hotbarImage9 = hotbarImageList[8]

                player.hotbarAlt1 = hotbarAltTextList[0]
                player.hotbarAlt2 = hotbarAltTextList[1]
                player.hotbarAlt3 = hotbarAltTextList[2]
                player.hotbarAlt4 = hotbarAltTextList[3]
                player.hotbarAlt5 = hotbarAltTextList[4]
                player.hotbarAlt6 = hotbarAltTextList[5]
                player.hotbarAlt7 = hotbarAltTextList[6]
                player.hotbarAlt8 = hotbarAltTextList[7]
                player.hotbarAlt9 = hotbarAltTextList[8]

                db.session.commit()
            else:
                newPlayer = Player(playerName=name, uuid=uuid, displayName=displayName, pageTitle=displayName, winPercent=winPercent, winRatio=winRatio, wins=wins, losses=losses, 
                                capDeathRatio=capDeathRatio, caps=caps, woolsStolen=woolsStolen, capSuccessRate=capSuccessRate, capsPerGame=capsPerGame, 
                                kdr=kdr, kills=kills, deaths=deaths, assists=assists, killsPerGame=killsPerGame, 
                                huntingKDR=huntingKDR, huntingKills=huntingKills, huntingDeaths=huntingDeaths, huntingKillsPerGame=huntingKillsPerGame, 
                                woolholderKDR=woolholderKDR, woolholderKills=woolholderKills, woolholderDeaths=woolholderDeaths, capPR=capPR, winPR=winPR, draws=draws, 
                                hotbarImage1=hotbarImageList[0], hotbarImage2=hotbarImageList[1], hotbarImage3=hotbarImageList[2], hotbarImage4=hotbarImageList[3], hotbarImage5=hotbarImageList[4], hotbarImage6=hotbarImageList[5], hotbarImage7=hotbarImageList[6], hotbarImage8=hotbarImageList[7], hotbarImage9=hotbarImageList[8], 
                                hotbarAlt1=hotbarAltTextList[0], hotbarAlt2=hotbarAltTextList[1], hotbarAlt3=hotbarAltTextList[2], hotbarAlt4=hotbarAltTextList[3], hotbarAlt5=hotbarAltTextList[4], hotbarAlt6=hotbarAltTextList[5], hotbarAlt7=hotbarAltTextList[6], hotbarAlt8=hotbarAltTextList[7], hotbarAlt9=hotbarAltTextList[8])
                
                db.session.add(newPlayer)
                db.session.commit()

            return render_template('player.html', displayName=displayName, uuid=uuid, title=displayName, winPercent=winPercent, winRatio=winRatio, wins=wins, losses=losses, 
                                capDeathRatio=capDeathRatio, caps=caps, woolsStolen=woolsStolen, capSuccessRate=capSuccessRate, capsPerGame=capsPerGame, 
                                kdr=kdr, kills=kills, deaths=deaths, assists=assists, killsPerGame=killsPerGame, 
                                huntingKDR=huntingKDR, huntingKills=huntingKills, huntingDeaths=huntingDeaths, huntingKillsPerGame=huntingKillsPerGame, 
                                woolholderKDR=woolholderKDR, woolholderKills=woolholderKills, woolholderDeaths=woolholderDeaths,
                                capPR=capPR, winPR=winPR, draws=draws,
                                hotbarImageList=hotbarImageList, hotbarAltTextList=hotbarAltTextList,
                                labels=radarLabels, values=radarValues)
            
        except:
            player = db.session.scalar(sa.select(Player).where(Player.playerName == name.lower()))
            
            displayName = player.displayName
            uuid = player.uuid

            winPercent = player.winPercent
            winRatio = player.winRatio
            wins = player.wins
            losses = player.losses

            capDeathRatio = player.capDeathRatio
            caps = player.caps
            woolsStolen = player.woolsStolen
            capSuccessRate = player.capSuccessRate
            capsPerGame = player.capsPerGame

            kdr = player.kdr
            kills = player.kills
            deaths = player.deaths
            assists = player.assists
            killsPerGame = player.killsPerGame

            huntingKDR = player.huntingKDR
            huntingKills = player.huntingKills
            huntingDeaths = player.huntingDeaths
            huntingKillsPerGame = player.huntingKillsPerGame

            woolholderKDR = player.woolholderKDR
            woolholderKills = player.woolholderKills
            woolholderDeaths = player.woolholderDeaths

            capPR = player.capPR
            winPR = player.winPR
            draws = player.draws

            hotbarImageList = [player.hotbarImage1, player.hotbarImage2, player.hotbarImage3, player.hotbarImage4, player.hotbarImage5, player.hotbarImage6, player.hotbarImage7, player.hotbarImage8, player.hotbarImage9]
            hotbarAltTextList = [player.hotbarAlt1, player.hotbarAlt2, player.hotbarAlt3, player.hotbarAlt4, player.hotbarAlt5, player.hotbarAlt6, player.hotbarAlt7, player.hotbarAlt8, player.hotbarAlt9]
            
            # radar chart data
            playerWinIndex = int(wins) / (int(wins) + int(losses) + 1)
            playerKillIndex = int(kills) / (int(kills) + int(deaths) + 1)
            playerHuntingIndex = int(huntingKills) / (int(huntingKills) + int(huntingDeaths) + 1)
            playerCapIndex = (int(caps) / (int(woolsStolen) + 1)) * 1.6

            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            radarValues = [playerWinIndex, playerCapIndex, playerHuntingIndex, playerKillIndex]
            
            
            return render_template('player.html', displayName=displayName, uuid=uuid, title=displayName, winPercent=winPercent, winRatio=winRatio, wins=wins, losses=losses, 
                                capDeathRatio=capDeathRatio, caps=caps, woolsStolen=woolsStolen, capSuccessRate=capSuccessRate, capsPerGame=capsPerGame, 
                                kdr=kdr, kills=kills, deaths=deaths, assists=assists, killsPerGame=killsPerGame, 
                                huntingKDR=huntingKDR, huntingKills=huntingKills, huntingDeaths=huntingDeaths, huntingKillsPerGame=huntingKillsPerGame, 
                                woolholderKDR=woolholderKDR, woolholderKills=woolholderKills, woolholderDeaths=woolholderDeaths,
                                capPR=capPR, winPR=winPR, draws=draws,
                                hotbarImageList=hotbarImageList, hotbarAltTextList=hotbarAltTextList, 
                                labels=radarLabels, values=radarValues)
    except:
        return render_template('retrieveError.html')
    


# player comparison page
@app.route('/compare/<playerName1>-<playerName2>')
def compare(playerName1, playerName2):
    try:
        try:
            API_KEY = getAPIKey()
            name1 = playerName1
            name2 = playerName2

            x = autoGetInfo(API_KEY, name1)
            y = autoGetInfo(API_KEY, name2)

            uuid1 = str(x["player"]["uuid"])
            displayName1 = str(x["player"]["displayname"])
            xData = x["player"]["stats"]["Arcade"]
            
            uuid2 = str(y["player"]["uuid"])
            displayName2 = str(y["player"]["displayname"])
            yData = y["player"]["stats"]["Arcade"]

            # CTW data for both players in dictionary form
            xDataDict = getCTWData(xData)
            yDataDict = getCTWData(yData)

            # Deal with putting this information into the database
            storeData(uuid1, name1, displayName1, xDataDict)
            storeData(uuid2, name2, displayName2, yDataDict)

            # Make lists of data to be used in radar chart
            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            p1RadarData = makeChartData(xDataDict)
            p2RadarData = makeChartData(yDataDict)

            return render_template('compare.html', title="Compare", displayName1=displayName1, displayName2=displayName2, xDataDict=xDataDict, yDataDict=yDataDict, 
                                   labels=radarLabels, p1Values=p1RadarData, p2Values=p2RadarData, p1Label=displayName1, p2Label=displayName2)
        except:
            
            name1 = playerName1
            name2 = playerName2


            #get CTW data form both players in dictionary form FROM THE DATABASE
            xDataDict = getCTWDataFromDatabase(name1)
            yDataDict = getCTWDataFromDatabase(name2)

            # Make lists of data to be used in radar chart
            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            p1RadarData = makeChartData(xDataDict)
            p2RadarData = makeChartData(yDataDict)

            return render_template('compare.html', title="Compare", displayName1=xDataDict["displayName"], displayName2=yDataDict["displayName"], xDataDict=xDataDict, yDataDict=yDataDict, 
                                   labels=radarLabels, p1Values=p1RadarData, p2Values=p2RadarData, p1Label=str(xDataDict["displayName"]), p2Label=str(yDataDict["displayName"]))
    except:
        return render_template('retrieveError.html')

    
