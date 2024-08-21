from app import app, db
from flask import render_template, redirect, url_for
from app.forms import SearchForm, CompareForm
from app.models import Player
import grequests
import requests
import os
from dotenv import find_dotenv, load_dotenv
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
    
# returns the API key using environment variables
def getAPIKey():
    dotenv_path = find_dotenv()

    load_dotenv(dotenv_path)

    API_KEY = os.getenv("API_KEY")

    return API_KEY
    
# return a dictionary of relevant CTW stats from a section of the API response
def getCTWData(data):

    statsData = data["stats"]

    dataDict = {
        "gamesPlayed": 0,
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
        #test comment

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
    if checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData) != 0:
        dataDict["winrateInt"] = checkDataExists("participated_wins", statsData) / (checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData))
    dataDict["winPercent"] = round(dataDict["winrateInt"] * 100, 2)
    if checkDataExists("participated_losses", statsData) != 0:
        dataDict["winRatio"] = round(checkDataExists("participated_wins", statsData) / checkDataExists("participated_losses", statsData), 2)
    else:
        dataDict["winRatio"] = checkDataExists("participated_wins", statsData)
    dataDict["wins"] = checkDataExists("participated_wins", statsData)
    dataDict["losses"] = checkDataExists("participated_losses", statsData)

    #cap data
    dataDict["caps"] = checkDataExists("wools_captured", statsData)
    if checkDataExists("deaths", statsData) != 0:
        dataDict["capDeathRatio"] = round(checkDataExists("wools_captured", statsData) / checkDataExists("deaths", statsData), 2)
    else:
        dataDict["capDeathRatio"] = checkDataExists("wools_captured", statsData)
    dataDict["woolsStolen"] = checkDataExists("wools_stolen", statsData)
    if checkDataExists("wools_stolen", statsData) != 0:
        dataDict["capSuccessRate"] = round((checkDataExists("wools_captured", statsData) / checkDataExists("wools_stolen", statsData)) * 100, 2)
    if checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData) != 0:
        dataDict["capsPerGame"] = round(checkDataExists("wools_captured", statsData) / (checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData)), 2)
    else:
        dataDict["capsPerGame"] = checkDataExists("wools_captured", statsData)

    #general kill/death data
    if checkDataExists("deaths", statsData) != 0:
        dataDict["kdr"] = round(checkDataExists("kills", statsData) / checkDataExists("deaths", statsData), 2)
    else:
        dataDict["kdr"] = checkDataExists("kills", statsData)
    dataDict["kills"] = checkDataExists("kills", statsData)
    dataDict["deaths"] = checkDataExists("deaths", statsData)
    dataDict["assists"] = checkDataExists("assists", statsData)
    if checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData) != 0:
        dataDict["killsPerGame"] = round(checkDataExists("kills", statsData) / (checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData)), 2)
    else:
        dataDict["killsPerGame"] = checkDataExists("kills", statsData)

    #kill/death data against woolholder
    if checkDataExists("deaths_to_woolholder", statsData) != 0:
        dataDict["huntingKDR"] = round(checkDataExists("kills_on_woolholder", statsData) / checkDataExists("deaths_to_woolholder", statsData), 2)
    else:
        dataDict["huntingKDR"] = checkDataExists("kills_on_woolholder", statsData)
    dataDict["huntingKills"] = checkDataExists("kills_on_woolholder", statsData)
    dataDict["huntingDeaths"] = checkDataExists("deaths_to_woolholder", statsData)
    if checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData) != 0:
        dataDict["huntingKillsPerGame"] = round(checkDataExists("kills_on_woolholder", statsData) / (checkDataExists("participated_wins", statsData) + checkDataExists("participated_losses", statsData)), 2)
    else:
        dataDict["huntingKillsPerGame"] = checkDataExists("kills_on_woolholder", statsData)

    #kill/death data as woolholder
    if checkDataExists("deaths_with_wool", statsData) != 0:
        dataDict["woolholderKDR"] = round(checkDataExists("kills_with_wool", statsData) / checkDataExists("deaths_with_wool", statsData), 2)
    else:
        dataDict["woolholderKDR"] = checkDataExists("kills_with_wool", statsData)
    dataDict["woolholderKills"] = checkDataExists("kills_with_wool", statsData)
    dataDict["woolholderDeaths"] = checkDataExists("deaths_with_wool", statsData)

    #miscellaneous data
    dataDict["capPR"] = checkDataExists("fastest_wool_capture", statsData)
    dataDict["draws"] = checkDataExists("participated_draws", statsData)
    dataDict["winPR"] = checkDataExists("fastest_win", statsData)

    #inventory layout data
    layoutData = checkDataExists("layout", data)
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

    dataDict["gamesPlayed"] = dataDict["wins"] + dataDict["losses"] + dataDict["draws"]
    
    return dataDict


# return a dictionary of relevant CTW stats from the specified player object in the database
def getCTWDataFromDatabase(name):
    dataDict = {
        "displayName": "",
        "uuid": "",

        "gamesPlayed": 0,

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
    dataDict["uuid"] = player.uuid

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

    dataDict["gamesPlayed"] = str(int(dataDict["wins"]) + int(dataDict["losses"]) + int(dataDict["draws"]))
    
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
@app.route('/', methods=['GET', 'POST'])
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

            x = autoGetInfo(API_KEY, name)

            uuid = str(x["player"]["uuid"]) 
            displayName = str(x["player"]["displayname"])
            data = x["player"]["stats"]["WoolGames"]["capture_the_wool"]

            # get CTW data in dictionary form
            dataDict = getCTWData(data)

            #Making values to be used in player radar chart
            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            radarData = makeChartData(dataDict)

            #deal with entering all this information into the database
            storeData(uuid, name, displayName, dataDict)

            return render_template('player.html', displayName=displayName, uuid=uuid, title=displayName, dataDict=dataDict,
                                labels=radarLabels, values=radarData)
            
        except:
            name = playerName

            # get CTW data in dictionary form FROM THE DATABASE
            dataDict = getCTWDataFromDatabase(name)
            
            # radar chart data
            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            radarData = makeChartData(dataDict)
            
            return render_template('player.html', displayName=dataDict["displayName"], uuid=dataDict["uuid"], title=dataDict["displayName"], dataDict=dataDict, 
                                labels=radarLabels, values=radarData)
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
            xData = x["player"]["stats"]["WoolGames"]["capture_the_wool"]
            
            uuid2 = str(y["player"]["uuid"])
            displayName2 = str(y["player"]["displayname"])
            yData = y["player"]["stats"]["WoolGames"]["capture_the_wool"]

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

            return render_template('compare.html', title="Compare", displayName1=displayName1, displayName2=displayName2, uuid1=uuid1, uuid2=uuid2, xDataDict=xDataDict, yDataDict=yDataDict, 
                                   labels=radarLabels, p1Values=p1RadarData, p2Values=p2RadarData, p1Label=displayName1, p2Label=displayName2)
        except:
            
            name1 = playerName1
            name2 = playerName2


            #get CTW data from both players in dictionary form FROM THE DATABASE
            xDataDict = getCTWDataFromDatabase(name1)
            yDataDict = getCTWDataFromDatabase(name2)

            # Make lists of data to be used in radar chart
            radarLabels = ["Winrate", "Caps", "Woolholder Kills", "Kills"]
            p1RadarData = makeChartData(xDataDict)
            p2RadarData = makeChartData(yDataDict)

            return render_template('compare.html', title="Compare", displayName1=xDataDict["displayName"], uuid1=xDataDict["uuid"], uuid2=yDataDict["uuid"], displayName2=yDataDict["displayName"], xDataDict=xDataDict, yDataDict=yDataDict, 
                                   labels=radarLabels, p1Values=p1RadarData, p2Values=p2RadarData, p1Label=str(xDataDict["displayName"]), p2Label=str(yDataDict["displayName"]))
    except:
        return render_template('retrieveError.html')

    
