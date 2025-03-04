import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import logging

# Keys are stored locally in the '.env' file for security reasons.
load_dotenv()

# Retrieves the token. 
TOKEN = os.getenv("TOKEN") 
# Retrieves the password.
PASSWORD = os.getenv("PASSWORD") 
# Retrieves the guild ID.
GUILD = discord.Object(id=os.getenv("GUILD_ID"))



# Sets the ID of the message. TODO extract that and make it more configurable
selector_message_id = 1346498705976594512

# TODO make a separate lookup table of the pairs to pick the correct ones. Fgrom 
# Creates a list of emojis - roles pairs. Must return a role for a given emoji.
emojis_roles = {
    '🏴‍☠️': 886560442305089547, 
    '👍🏽': 688055636629389315
}

# Loads the intents for the bot
intents = discord.Intents.default()
intents.message_content = True

# Creates a connection to discord
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
tree = app_commands.CommandTree(client)

# Creates a handler for the logs
# handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')

# This event is called whenever the bot sends a callback function notifiying us that it is ready.
@client.event
async def on_ready():
    print(f'BOT logged in as: {client.user}')

    # try:
    #     synced = await tree.sync(guild=GUILD)
    #     print(f'Synchronized {len(synced)} commands.')
    # except Exception as e:
    #     print(e)

    # TODO if there is no role selection message posted and linked, creates one and links it. RSM should be fetched from .env variables

# Whenever there is a message posted in the server on which the bot is installed
@client.event
async def on_message(message):
    
    # Prints any message event's author and its content
    print(f"Message from {message.author.display_name}: {message.content}")
    
    # Client.user
    if message.author == client.user:
        return

    # If the beginning of the message is "$command", will respond with command!
    if message.content.startswith('$command'):
        await message.channel.send('Received: command!')

    # Forces the sync of the tree from the chat
    if message.content.startswith('$sync'):

        # Synchronizes the commands into the tree
        await tree.sync(guild=GUILD)

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
@tree.command(name='test', description="A command for xav's bot", guild=GUILD)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("test successful")

# Creates a bot that will respond to commands with the / prefix
@tree.command(name='parrot', description="The bot will repeat what it hears the number of times specified.", guild=GUILD)
# Describes the parameters that are passed to the slash command
@app_commands.describe(input_text="The text that the bot will repeat.", repeats_count="How many times the bot will repeat the text.")
async def parrot(interaction: discord.Interaction, input_text: str, repeats_count: int):
    return_text = ""
    for _ in range(repeats_count):
        return_text += input_text + "\n"
    await interaction.response.send_message(return_text)

# Synchronizes the slash commands
@tree.command(name='sync_commands', description="Syncs the commands onto the server. May require to reload the page.", guild=GUILD)
@app_commands.describe(input_password="Enter the password to validate the action.")
async def sync_commands(interaction: discord.Interaction, input_password: str):

    if input_password == PASSWORD:
        
        # Synchronizes the commands into the tree
        await tree.sync()
    else:
        await interaction.response.send_message("Incorrect password.")

# A command to publish leetcodes onto the server ?
@tree.command(name='leetcode_report', description="This will report the latest leetcodes completed.", guild=GUILD)
@app_commands.describe(username="The target user.")
async def leetcode_report(interaction: discord.Interaction, username: str):

    await interaction.response.send_message(f"User:{username}")

# Whenever someone reacts to the specific message, gives roles according to the emoji (OR commands?)
@client.event
async def on_raw_reaction_add(payload):


    # Ignores if the id of the message is not the desired one
    if payload.message_id != selector_message_id:
        return

    # Extracts the roles from the server
    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    
    # Retrieves the name & ID from the reaction
    reaction_emoji_name, reaction_emoji_name_id = payload.emoji.name, payload.emoji.id
    print("emoji", reaction_emoji_name, reaction_emoji_name_id)

    # Checks if the reaction emoji is in the list. TODO add a check to avoid crashes when it is not in the list and also return aerly
    if reaction_emoji_name not in emojis_roles.keys():
        
        print(reaction_emoji_name, "not found in table.")
        return

    # Gets the role ID linked to the emoji name from the table
    role_to_add = guild.get_role(emojis_roles[reaction_emoji_name])
    print("role ID to add", role_to_add)

    # Adds a specific role based on the reaction
    reacting_user = payload.member
    print("Adding role", role_to_add,"to user", reacting_user)
    await reacting_user.add_roles(role_to_add)


# Whenever someone reacts to the specific message, gives roles according to the emoji (OR commands?)
@client.event
async def on_raw_reaction_remove(payload):

    print(payload)

    # Ignores if the id of the message is not the desired one
    if payload.message_id != selector_message_id:
        return

    # Extracts the roles from the server
    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    
    # Retrieves the name & ID from the reaction
    reaction_emoji_name, reaction_emoji_name_id = payload.emoji.name, payload.emoji.id
    print("emoji", reaction_emoji_name, reaction_emoji_name_id)

    # Checks if the reaction emoji is in the list. TODO add a check to avoid crashes when it is not in the list and also return aerly
    if reaction_emoji_name not in emojis_roles.keys():
        
        print(reaction_emoji_name, "not found in table.")
        return

    # Gets the role ID linked to the emoji name from the table
    role_to_remove = guild.get_role(emojis_roles[reaction_emoji_name])
    print("role ID to remove", role_to_remove) # Why is this returing a string and not the id?

    # removes a specific role based on the reaction
    reacting_user = guild.get_member(payload.user_id)
    print("Removing role", role_to_remove,"to user", reacting_user)
    await reacting_user.remove_roles(role_to_remove)

# On join / leave role, post messages accordingly?

# Create a role (organise roles, give relevant permissions)

# Create a category (make it private)

# Create a text channel (in the category & private)

# Create a voice channel (in the category & private)

# A command that returns the list of common games for a list of players based on their tags. Could be done using the emojis system as db ?

# Runs the bot
client.run(TOKEN)
# client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)