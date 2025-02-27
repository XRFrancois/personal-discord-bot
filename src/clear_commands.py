import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

# Keys are stored locally in the '.env' file for security reasons.
load_dotenv()

# Retrieves the token. 
TOKEN = os.getenv("TOKEN") 
# Retrieves the guild ID.
GUILD = discord.Object(id=os.getenv("GUILD_ID"))

# Loads the intents for the bot
intents = discord.Intents.default()
intents.message_content = True

# Creates a connection to discord
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# This event is called whenever the bot sends a callback function notifiying us that it is ready.
@client.event
async def on_ready():
    print(f'BOT logged in as: {client.user}')

    try:
        synced_global = await tree.sync(guild=GUILD)
        synced_local = await tree.sync()
        print(f'Synchronized {len(synced_global)} global commands.')
        print(f'Synchronized {len(synced_local)} server specific commands.')
    except Exception as e:
        print(e)


# Runs the bot
client.run(TOKEN)