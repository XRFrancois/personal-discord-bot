import discord
from discord.ext import commands
from discord import app_commands
import logging

# Open the file in read mode and returns the token it contains
def get_local_token(token_file_path: str) -> str:
    file = open(token_file_path, "r")
    bot_token = file.read()
    file.close()

    return bot_token

# Retrieves the token. It is stored locally for security reasons.
bot_token_path = "./data/bot_token.txt"
bot_token = get_local_token(bot_token_path)

# Loads the intents for the bot
intents = discord.Intents.default()
intents.message_content = True

# Creates a connection to discord
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
tree = app_commands.CommandTree(client)

# Creates a handler for the logs
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# This event is called whenever the bot sends a callback function notifiying us that it is ready.
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Synchronizes the commands into the tree
    try:
        await tree.sync()
    except Exception as e:
        print(e)

# Whenever there is a message posted in the server on which the bot is installed
@client.event
async def on_message(message):
    
    # Prints any message event's author and its content
    print(f"Message from {message.author.display_name}: {message.content}")
    
    # Client.user
    if message.author == client.user:
        return

    # If the beginning of the message is "$hello", will respond with Hello!
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # If the beginning of the message is "$hello", will respond with Hello!
    if message.content.startswith('$xaviersaitpasfairemarcherlebot'):
        await message.channel.send("Je suis un bot recalcitrant qui veut pas faire ce qu'on lui demande")

# Whenever someone edits a message
@client.event
async def on_message_edit(before, after):
    msg = f'**{before.author}** edited their message:\n{before.content} -> {after.content}'
    print(msg)

# Whenever someone deletes a message
@client.event
async def on_message_delete(message):
    msg = f'{message.author} has deleted the message: {message.content}'
    print(msg)

# Whenever someone joins the server
@client.event
async def on_member_join(member):
    guild = member.guild

    # TODO add a way to specify the channel.

    # Sends a message in the system channel
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.system_channel.send(to_send)

    # Can I change the specific channel?

# Creates a bot that will respond to commands with the / prefix
@tree.command(name='test', description="A command for xav's bot")
async def test(interaction: discord.Integration):
    await interaction.response.send_message("test successful")

# Runs the bot
client.run(bot_token, log_handler=handler, log_level=logging.DEBUG)