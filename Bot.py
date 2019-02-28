import urllib.parse
import requests
import re
import json
import feedparser
import discord
from discord import Game
from discord.ext.commands import Bot
from discord import Embed


BOT_PREFIX = '?'
TOKEN = 'TOKEN'

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Games"))
    print("Logged in as " + client.user.name)


@client.command()
async def Jobbpod():
    NewsFeed = feedparser.parse(
        "https://arbetsformedlingen.podbean.com/feed.xml")
    print("numbers of posts", len(NewsFeed.entries))
    entry = NewsFeed.entries[0]

    print(entry.keys())
    print(entry.published)
    print(entry.title)
    print(entry.itunes_explicit)
    print(entry.content)

    await client.say("Här är den senaste JobbPodden :" + entry.link)


@client.command()
async def Jobb(Jobb="", Stad="", Antal="20"):

    if Jobb.isdigit() & Antal.isdigit() & Stad.isdigit():
        Jobb = "Sverige"
        Stad = ""

    if Jobb.isdigit() & Antal.isdigit():
        print(Jobb, Antal)
        Antal = Jobb
        Jobb = ""
    elif Stad.isdigit() & Antal.isdigit():
        print(Stad, Antal)
        Antal = Stad
        Stad = ""
    elif Jobb.isdigit():
        Score = Jobb
        Jobb = Antal
        Antal = Score
    elif Stad.isdigit():
        Score = Stad
        Stad = Antal
        Antal = Score
    else:
        print("False")

    jobID = []
    jobURL = []
    jobHead = []
    jobRecruit = []
    jobStad = []
    jobAnstallningsTyp = []
    jobYrkesbenamning = []
    jobSistaDatum = []
    nums = 0
    jobs = 0
    jobInfo = []
    RealNumb = int(Antal) - 1
    jobInfo.append(Jobb)
    jobInfo.append(Stad)
    main_api = 'https://api.arbetsformedlingen.se/af/v0/platsannonser/matchning?'
    params = {"nyckelord": Jobb + " " + Stad, "sida": "1", "antalrader": Antal}
    headers = {'content-type': 'application/json', 'Accept-language': 'sv'}

    print(params)
    url = main_api + urllib.parse.urlencode(params)
    print(url)

    print("working even longer")
    json_data = requests.get(url, headers=headers).json()

    while nums <= RealNumb:
        try:
            jobID.append(json_data['matchningslista']
                         ['matchningdata'][nums]['annonsid'])
            jobURL.append(json_data['matchningslista']
                          ['matchningdata'][nums]['annonsurl'])
            jobHead.append(json_data['matchningslista']
                           ['matchningdata'][nums]['annonsrubrik'])
            jobStad.append(json_data['matchningslista']
                           ['matchningdata'][nums]['kommunnamn'])
            jobAnstallningsTyp.append(json_data['matchningslista']
                                      ['matchningdata'][nums]['anstallningstyp'])
            jobRecruit.append(json_data['matchningslista']
                              ['matchningdata'][nums]['arbetsplatsnamn'])
            jobYrkesbenamning.append(json_data['matchningslista']
                                     ['matchningdata'][nums]['yrkesbenamning'])
            try:
                jobSistaDatum.append(json_data['matchningslista']
                                     ['matchningdata'][nums]['sista_ansokningsdag'])
            except:
                jobSistaDatum.append("-")
        except:
            print("Failed")

        nums += 1

    print(jobSistaDatum)
    while jobs <= RealNumb:
        try:

            embed = Embed(
                title=jobHead[jobs], description=jobYrkesbenamning[jobs], color=0x00ff00)
            if(jobSistaDatum != None):
                embed.add_field(name="Sök Senast",
                                value=jobSistaDatum[jobs][0:10], inline=False)
            embed.add_field(name="Stad", value=jobStad[jobs], inline=False)
            embed.add_field(name="Arbetsgivare",
                            value=jobRecruit[jobs], inline=False)
            embed.add_field(name="Anställningstyp",
                            value=jobAnstallningsTyp[jobs], inline=False)
            embed.add_field(name="Mer info", value=jobURL[jobs], inline=False)
            await client.say(embed=embed)
            jobs += 1
        except:
            ("Not enough work")
            jobs += 1


@client.command()
async def Spel(Spel="", Roll=""):
    Spel = Spel.lower()
    Roll = Roll.lower()

    if (Spel or Roll == "world of warcraft" or "wow"):
        print(Spel)
        print(Roll)
        if(Spel == "support" or Spel == "support" or Roll == "support" or Roll == "support"):
            print("support in WoW")
        elif(Spel == "tank" or Roll == "tank"):
            print("Tank")
        elif(Spel == "dps" or Roll == "dps"):
            print("DPS")
        else:
            print("No role Chosen")
    elif (Spel == Spel):
        print("Wrong")

    await client.say("Hello")

client.run(TOKEN)
