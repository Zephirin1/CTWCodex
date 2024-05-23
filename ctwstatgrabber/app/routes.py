from app import app, db
from flask import render_template, redirect, url_for
from app.forms import SearchForm
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


@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('player', playerName = form.playerName.data))
    return render_template('playerSearch.html', form=form)


@app.route('/player/<playerName>')
def player(playerName):
    try:
        try:
            API_KEY = "293d3258-0e8c-432a-b9c0-e86efb9f8e3e"
            name = playerName

            name_link = f"https://api.hypixel.net/player?key={API_KEY}&name={name}"

            x = getInfo(name_link)

            uuid = str(x["player"]["uuid"])
            displayName = str(x["player"]["displayname"])
            data = x["player"]["stats"]["Arcade"]

            #skywarsWins = str(data["player"]["stats"]["SkyWars"]["wins"])  <-- example to get specific data from json

            #win/loss data
            winRateInt = data["woolhunt_participated_wins"] / (data["woolhunt_participated_wins"] + data["woolhunt_participated_losses"])
            winPercent = str(round(winRateInt * 100, 2))
            winRatio = str(round(data["woolhunt_participated_wins"] / data["woolhunt_participated_losses"], 2))
            wins = str(data["woolhunt_participated_wins"])
            losses = str(data["woolhunt_participated_losses"])

            #cap data
            capDeathRatio = str(round(data["woolhunt_wools_captured"] / data["woolhunt_deaths"], 2))
            caps = str(data["woolhunt_wools_captured"])
            woolsStolen = str(data["woolhunt_wools_stolen"])
            capSuccessRate = str(round((data["woolhunt_wools_captured"] / data["woolhunt_wools_stolen"]) * 100, 2))
            capsPerGame = str(round(data["woolhunt_wools_captured"] / (data["woolhunt_participated_wins"] + data["woolhunt_participated_losses"]), 2))

            #general kill/death data
            kdr = str(round(data["woolhunt_kills"] / data["woolhunt_deaths"], 2))
            kills = str(data["woolhunt_kills"])
            deaths = str(data["woolhunt_deaths"])
            assists = str(data["woolhunt_assists"])
            killsPerGame = str(round(data["woolhunt_kills"] / (data["woolhunt_participated_wins"] + data["woolhunt_participated_losses"]), 2))

            #kill/death data against woolholder
            huntingKDR = str(round(data["woolhunt_kills_on_woolholder"] / data["woolhunt_deaths_to_woolholder"], 2))
            huntingKills = str(data["woolhunt_kills_on_woolholder"])
            huntingDeaths = str(data["woolhunt_deaths_to_woolholder"])
            huntingKillsPerGame = str(round(data["woolhunt_kills_on_woolholder"] / (data["woolhunt_participated_wins"] + data["woolhunt_participated_losses"]), 2))

            #kill/death data as woolholder
            woolholderKDR = str(round(data["woolhunt_kills_with_wool"] / data["woolhunt_deaths_with_wool"], 2))
            woolholderKills = str(data["woolhunt_kills_with_wool"])
            woolholderDeaths = str(data["woolhunt_deaths_with_wool"])

            #miscellaneous data
            capPR = str(data["woolhunt_fastest_wool_capture"])
            try:
                draws = str(data["woolhunt_participated_draws"])
            except:
                draws = str(0)
            winPR = str(data["woolhunt_fastest_win"])

            #inventory layout data
            layoutData = data["woolhunt_inventorylayout"]
            layoutDataKeys = list(layoutData.keys())
            layoutDataValues = list(layoutData.values())
            inventoryList = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
            imageList = ['images/Stone_Sword.png', 'images/Iron_Pickaxe_JE3_BE2.png', 'images/Bow_JE2_BE1.png', 'images/Iron_Axe_JE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Oak_Planks_JE6_BE3.png', 'images/Golden_Apple_JE1_BE1.png', 'images/Arrow.png', 'images/Empty.png']
            altTextList = ["Sword", "Pickaxe", "Bow", "Axe", "Planks", "Planks", "Planks", "Golden Apple", "Arrows", "Empty"]

            count = 0
            for key in layoutDataKeys:
                inventoryList[int(key)] = layoutDataValues[count]
                count = count + 1

            hotbarImageList = []
            hotbarAltTextList = []
            i = 0
            while i < 9:
                hotbarImageList.append(imageList[inventoryList[i]])
                hotbarAltTextList.append(altTextList[inventoryList[i]])
                i = i + 1

            #Making values to be used in player radar chart
            playerWinIndex = winRateInt
            playerKillIndex = data["woolhunt_kills"] / (data["woolhunt_kills"] + data["woolhunt_deaths"])
            playerHuntingIndex = data["woolhunt_kills_on_woolholder"] / (data["woolhunt_kills_on_woolholder"] + data["woolhunt_deaths_to_woolholder"])
            playerCapIndex = data["woolhunt_wools_captured"] / data["woolhunt_wools_stolen"]

            radarLabels = ["Winrate", "Capping", "Killing Woolholders", "Killing"]
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

            return render_template('player.html', displayName=displayName, title=displayName, winPercent=winPercent, winRatio=winRatio, wins=wins, losses=losses, 
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
            
            
            
            
            return render_template('player.html', displayName=displayName, title=displayName, winPercent=winPercent, winRatio=winRatio, wins=wins, losses=losses, 
                                capDeathRatio=capDeathRatio, caps=caps, woolsStolen=woolsStolen, capSuccessRate=capSuccessRate, capsPerGame=capsPerGame, 
                                kdr=kdr, kills=kills, deaths=deaths, assists=assists, killsPerGame=killsPerGame, 
                                huntingKDR=huntingKDR, huntingKills=huntingKills, huntingDeaths=huntingDeaths, huntingKillsPerGame=huntingKillsPerGame, 
                                woolholderKDR=woolholderKDR, woolholderKills=woolholderKills, woolholderDeaths=woolholderDeaths,
                                capPR=capPR, winPR=winPR, draws=draws,
                                hotbarImageList=hotbarImageList, hotbarAltTextList=hotbarAltTextList)
    except:
        return render_template('apiError.html')
    