import os
import time
import sched
import discord
import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

PRICES = dict()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    channel = client.get_channel(696558030870806608)
    await channel.send('hello')


async def send_prices():
    channel = client.get_channel(696558030870806608)

    formatted_msg = "" 
    for key in PRICES:
        formatted_msg += f"{key}'s price is: {PRICES[key]}\n"
    if formatted_msg == "":
        await channel.send("Nobody has published their updated turnip prices yet! You could be the first! ;)")
    else:
        await channel.send(formatted_msg)


@client.event
async def on_message(msg):

    if msg.content.startswith('t'):  ## FIXME
        await send_prices()

    elif msg.content.startswith("p "):  ## FIXME
        price = msg.content.split("p")[1]
        author = msg.author.display_name
        PRICES[author] = price

        await send_prices()


async def time_check():
    await client.wait_until_ready()
    now = datetime.datetime.now()
    # get the difference between the alarm time and now

    # if now is between 8 am and 12 pm then seconds = 12pm-now
    # else seconds = 8am - now
    if now.hour <= 7:
        seconds = (now.replace(hour=8, minute=0, second=0) - now).total_seconds()
        print("8", seconds)
    elif now.hour <= 11:
        seconds = (now.replace(hour=12, minute=0, second=0) - now).total_seconds()
        print("garbage", seconds)
    else:
        seconds = ((now + datetime.timedelta(days=1)).replace(hour=8, minute=0, second=0) - now).total_seconds()
        print("slimepit", seconds)


    # create a scheduler
    s = sched.scheduler(time.perf_counter, time.sleep)
    # arguments being passed to the function being called in s.enter
    args = (clear_prices(),)
    # enter the command and arguments into the scheduler
    s.enter(seconds, 1, client.loop.create_task, args)
    s.run() # run the scheduler, will block the event loop


async def clear_prices():
    PRICES = dict()
    channel = client.get_channel(696558030870806608)
    await channel.send("Cleared prices")
    client.loop.create_task(time_check())


client.loop.create_task(time_check())

client.run(TOKEN)
