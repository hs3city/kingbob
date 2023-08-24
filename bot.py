import logging
import os
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import tasks

discord_token = os.getenv("DISCORD_TOKEN")

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Discord configuration
intents = discord.Intents.default()
client = discord.Client(intents=intents)

channel_ids: list[int] = []


async def notify_the_subjects(now):
    for channel_id in channel_ids:
        channel = client.get_channel(channel_id)

        counter = 0
        messages = []
        logging.info(f"Have I already spoken in {channel.name}?")
        async for message in channel.history(limit=200):
            if (
                message.author == client.user
                and message.type == discord.MessageType.default
                and now - message.created_at < timedelta(days=1)
            ):
                counter += 1
                messages.append(message)

        if counter == 0:
            logging.info("Gonna notify them subjects")
            await client.get_channel(channel_id).send(
                "🪴 King Bob ma sucho. Polej mu! 💧"
            )
        else:
            logging.info(f"Seems like I have already spoken: {messages}")


# Fire every minute
@tasks.loop(hours=6)
async def is_king_bob_happy():
    logging.info("Checking the status")
    now = datetime.now(timezone.utc)
    if now.weekday() == 2:
        logging.info("Wednesday Evening Blues")
        await notify_the_subjects(now)


@client.event
async def on_ready():
    global channel_ids
    for guild in client.guilds:
        logging.info(f"{client.user} has connected to Discord server {guild}!")
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                if "general" in channel.name or "ogólne" in channel.name:
                    logging.info(
                        f"{channel.name} with ID {channel.id} is of my interest"
                    )
                    channel_ids.append(channel.id)
    is_king_bob_happy.start()


client.run(discord_token)
