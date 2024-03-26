import tls_client
import requests
from veilcord import VeilCord
from terminut import log
from capmonster_python import HCaptchaTask
import json
import random

# Veilcord
veilcord = VeilCord(
    session=None,
    device_type="browser",
    user_agent=None
)
xsuper = veilcord.generateXProp()
fp, cookies = veilcord.getFingerprint(
    xsuper,
    withCookies=True,
    cookieType="json"
)

session = tls_client.Session(
    client_identifier="chrome121",
    random_tls_extension_order=True
)

# Put stuff here
bot_id = ""
captcha_key = "" #Capmonster, Hcop kinda ass rn

# Import Proxies
with open("./data/proxies.txt", "r") as file:
    proxies = file.readlines()
    random_proxy = random.choice(proxies)

def solver():
    log.info("Solving Captcha...")
    while True:
        try:
          capmonster = HCaptchaTask(captcha_key)
          capmonster.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
          task_id = capmonster.create_task("https://discord.com/", "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34")
          result = capmonster.join_task_result(task_id)
          capkey = result.get("gRecaptchaResponse")
          log.info(f"Solved {capkey[:40]}!")
          return capkey
        except Exception as e:
            print(f"Error: {e}")
            continue

def main(token: str):
    url = "https://discord.com/api/v9/guilds"
    payload = json.dumps({
        "name": "12345",
        "icon": None,
        "channels": [],
        "system_channel_id": None,
        "guild_template_code": "2TffvPucqHkN"
    })
    headers = {
        'authority': 'discord.com',
        'accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'authorization': token,
        'content-type': 'application/json',
        'cookie': cookies,
        'origin': 'https://discord.com',
        'referer': 'https://discord.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-discord-locale': 'en-US',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'x-discord-timezone': 'America/New_York',
        'x-super-properties': xsuper
    }
    res = session.post(url, headers=headers, data=payload)
    res_json = json.loads(res.text)
    if res.status_code == 201:
        server_id = res_json["id"]
        log.vert(": Server Created!", ID=server_id)
        log.log(f"Adding Bot, ID: {bot_id} To {server_id}")

        # Add bot to server
        url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=0"
        payload = json.dumps({
           "permissions": "0",
            "authorize": True,
            "captcha_key": solver(),
        })

        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'authorization': token,
            'content-type': 'application/json',
            'cookie': cookies,
            'origin': 'https://discord.com',
            'referer': 'https://discord.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'x-discord-locale': 'en-US',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'x-discord-timezone': 'America/New_York',
            'x-super-properties': xsuper
        }
        res = session.post(url, headers=headers, data=payload)
        if res.status_code == 200:
            log.success("Bot Added!")
        else:
            log.error("Failed to Add Bot :(")
    else:
        log.error(f"Error Creating Server: {res.status_code}")

if __name__ == "__main__":
    with open('./data/tokens.txt', 'r') as file:
        for tokens in file:
            token = tokens.strip()
            main(token)
