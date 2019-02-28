import urllib.parse
import requests
import webbrowser
import re
import json
import feedparser

from discord import Game
from discord.ext.commands import Bot


BOT_PREFIX = '?'
TOKEN = 'TOKEN'

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Games"))
    print("Logged in as " + client.user.name)


@client.command()
async def Jobbpod():
    NewsFeed = feedparser.parse("https://arbetsformedlingen.podbean.com/feed.xml")
    print("numbers of posts", len(NewsFeed.entries) )
    entry = NewsFeed.entries[0]

    print(entry.keys())
    print(entry.published)
    print(entry.title)
    print(entry.itunes_explicit)
    print(entry.content)


    await client.say("Här är den senaste JobbPodden :" +  entry.link)


@client.command()
async def Fråga(Word1 = "" ,Word2 = "" , Word3 = "" , Word4 = "" , Word5 = "" , Word6 = "" , Word7 = "" , Word8 = "" , Word9 = "" , Word10 = "" , Word11 = "" , Word12 = "" , Word13 = "" , Word14 = "" , Word15 = "" , Word16 = "" , Word17 = "" , Word18 = ""   ):
    message = Word1 + " " + Word2 + " "+ Word3 + " "+ Word4 + " "+ Word5 + " "+ Word6 + " "+ Word7 + " "+ Word8 + " "+ Word9 + " "+ Word10 + " "+ Word11 + " "+ Word12+ " " + Word13+ " " + Word14+ " " + Word15+ " " + Word16+ " " + Word17+ " " + Word18 
    
    main_api = "https://qna-innovationscenter.azurewebsites.net/qnamaker/knowledgebases/bd006025-8f47-426b-8e35-f3d0e18ff30e/generateAnswer?"
    print(message)
    params = {"question": message, "top": "1"}
    headers = {"AUTHORIZATION": "EndpointKey 8762728a-b4e0-456c-b900-08be5ac68623",
               "Content-Type": "application/json"}
    print(params)
    url = main_api + urllib.parse.urlencode(params)
    quest = json.dumps(params)
    print(url)
    print(headers)
    print("working even longer")

    json_data = requests.post(url, quest, headers=headers).json()

    print(json_data)

    await client.say(json_data['answers'][0]['answer'])


@client.command()
async def Jobb(Jobb="", Stad="", Antal="5"):

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
        jobID.append(json_data['matchningslista']
                     ['matchningdata'][nums]['annonsid'])
        jobURL.append(json_data['matchningslista']
                      ['matchningdata'][nums]['annonsurl'])
        jobHead.append(json_data['matchningslista']
                       ['matchningdata'][nums]['annonsrubrik'])
        nums += 1

    while jobs <= RealNumb:
        await client.say(jobHead[jobs] + "\n" + jobURL[jobs])
        jobs += 1

client.run(TOKEN)
