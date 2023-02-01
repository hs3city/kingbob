import logging
import os
from datetime import datetime

import discord
from discord.ext import tasks

discord_token = os.getenv("DISCORD_TOKEN")

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Discord configuration
intents = discord.Intents.default()
client = discord.Client(intents=intents)

channel_ids: list[int] = []


async def notify_the_subjects():
    for channel_id in channel_ids:
        channel = client.get_channel(channel_id)

        counter = 0
        logging.info("Have I already spoken?")
        async for message in channel.history(limit=200):
            if (
                message.author == client.user
                and message.type == discord.MessageType.default
            ):
                counter += 1

        if counter == 0:
            logging.info("Gonna notify them subjects")
            await client.get_channel(channel_id).send(
                "🪴 King Bob ma sucho. Polej mu! 💧"
            )
        else:
            logging.info("Seems like I have already spoken")


# Fire every minute
@tasks.loop(hours=6)
async def is_king_bob_happy():
    logging.info("Checking the status")
    today = datetime.today()
    if today.weekday() == 4:
        logging.info("It's Friday, I'm in love!")
        await notify_the_subjects()


@client.event
async def on_ready():
    global channel_ids
    for guild in client.guilds:
        logging.info(f"{client.user} has connected to Discord server {guild}!")
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            if "general" in channel.name or "ogóln" in channel.name:
                logging.info(f"{channel.name} with ID {channel.id} is of my interest")
                channel_ids.append(channel.id)
    is_king_bob_happy.start()


client.run(discord_token)
