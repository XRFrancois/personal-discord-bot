import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
import logging
import csv



""" CONFIG & SETUP """

# Keys are stored locally in the '.env' file for security reasons.
load_dotenv()

# Retrieves the token. 
TOKEN = os.getenv("TOKEN") 
# Retrieves the password.
PASSWORD = os.getenv("PASSWORD") 
# Retrieves the guild ID.
GUILD = discord.Object(id=os.getenv("GUILD_ID"))

# Sets the ID of the message. TODO extract that and make it more configurable
selector_message_id = 1349042179578007594
selector_channel_id = 1349019110243176469
user_welcome_channel_id = 1349019011324837928

# TODO add an easier way to add entries to the text file (convert emojis) >> Can take from https://emojipedia.org/video-game
# TODO export all the roles from the server and give them a random emoji?
# Retrieves the pairs of emojis - roles from the "database" data/emojis-roles.txt
emojis_roles = {}
with open('data/emojis_roles.txt', mode ='r', encoding='utf-8') as file:
    for line in file:
        line = line.replace("\n", "")
        values = line.split(',')
        emojis_roles[values[0]] = int(values[1])
        print(">> Loaded: ", values[0], values[1], values[2])
    file.close()

# Loads the intents for the bot
intents = discord.Intents.default()
intents.message_content = True

# Creates a connection to discord
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
tree = app_commands.CommandTree(client)

# Creates a handler for the logs
# handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')


""" EVENTS TRIGGER """

# Whenever the bot sends a callback function notifiying us that it is ready.
@client.event
async def on_ready():
    print(f'BOT logged in as: {client.user}')

    # Attempts to synchronize the / commands on the guild.
    # try:
    #     synced = await tree.sync(guild=GUILD)
    #     print(f'Synchronized {len(synced)} commands.')
    # except Exception as e:
    #     print(e)

    # TODO If there is no welcome channel selected, make the system one the default

    # TODO if there is no role selection message posted and linked, creates one and links it. RSM should be fetched from .env variables
    
    # Get the guild from the client
    guild = await client.fetch_guild(os.getenv("GUILD_ID"))

    # Get the role selection channel
    try:
        channel = await guild.fetch_channel(selector_channel_id)
    except discord.errors.NotFound:
        print("Could not find the channel with the provided ID.")
        return
        
    # Checks if there is already a role selection message
    try:
        selection_message = await channel.fetch_message(selector_message_id)
        print(f"Guild currently uses message {selector_message_id} as role selector.")
    except discord.errors.NotFound:
        print("Could not find the role selection message with the provided ID.")

        # Creates a message for the role selection
        role_selection_text = f"# Role Selector\n*Reacting to this message with one of the following emojis will grant you the associated role, allowing you to view and interact with the desired channels.\nRemove the reaction to revert the action.*\n## Currently supported roles are:\n"
        roles_text = []
        emojis = []
        for emoji in emojis_roles.keys():
            role_name = await guild.fetch_role(emojis_roles[emoji])
            entry = emoji + " -> `" + role_name.name + "`"
            emojis.append(emoji)
            roles_text.append(entry)
        roles_text = "\n".join(roles_text)

        # Sends the message. Its ID will be tracked from within "on_message"
        message = await channel.send(role_selection_text + roles_text)
        message.pin()
        
        # Adds the related emojis reactions
        for emoji in emojis:
            await message.add_reaction(emoji)
    
    # TODO Whenever there is a change to the role-emojis, update the message  


# Whenever there is a message posted in the server on which the bot is installed
@client.event
async def on_message(message):
    
    # Prints any message event's author and its content
    print(f"Message from {message.author.display_name}: {message.content}")
    
    # Client.user
    if message.author == client.user:

        # If it is a message from the bot in the channel for role selection
        if message.channel.id == selector_channel_id: # and "selector message" in message.content:
            print("message posted in selector channel")
            global selector_message_id 
            selector_message_id = message.id
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

    # Sends a message in the chosen welcome channel according to config
    if guild.get_channel(user_welcome_channel_id) is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.get_channel(user_welcome_channel_id).send(to_send)


# Whenever someone reacts to the specific message, gives roles according to the emoji TODO exclude bot
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
    print(">> Reaction Emoji:", reaction_emoji_name)

    # Checks if the reaction emoji is in the list.
    if reaction_emoji_name not in emojis_roles.keys():
        return

    # Gets the role ID linked to the emoji name from the table
    role_to_add = guild.get_role(emojis_roles[reaction_emoji_name])

    # Adds a specific role based on the reaction
    reacting_user = payload.member
    print(">> Added role", role_to_add,"to user", reacting_user)
    await reacting_user.add_roles(role_to_add)


# Whenever someone removes a reaction on the specific message, removes roles according to the emoji
@client.event
async def on_raw_reaction_remove(payload):

    # Ignores if the id of the message is not the desired one
    if payload.message_id != selector_message_id:
        return

    # Extracts the roles from the server
    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    
    # Retrieves the name & ID from the reaction
    reaction_emoji_name, reaction_emoji_name_id = payload.emoji.name, payload.emoji.id
    print(">> Reaction to removed Emoji:", reaction_emoji_name)

    # Checks if the reaction emoji is in the list.
    if reaction_emoji_name not in emojis_roles.keys():
        return

    # Gets the role ID linked to the emoji name from the table
    role_to_remove = guild.get_role(emojis_roles[reaction_emoji_name])

    # Removes a specific role based on the emoji reaction. Fetch is used because get_member() would lead to cache misses that crashed the program.
    reacting_user = await guild.fetch_member(payload.user_id)
    print(">> Removed role", role_to_remove,"from user", reacting_user)
    await reacting_user.remove_roles(role_to_remove)



""" BOT COMMANDS """

# TODO rework or remove. Creates a bot that will respond to commands with the / prefix
@tree.command(name='test', description="A command for xav's bot", guild=GUILD)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("test successful")


# TODO rework or remove. Creates a bot that will respond to commands with the / prefix
@tree.command(name='parrot', description="The bot will repeat what it hears the number of times specified.", guild=GUILD)
# Describes the parameters that are passed to the slash command
@app_commands.describe(input_text="The text that the bot will repeat.", repeats_count="How many times the bot will repeat the text.")
async def parrot(interaction: discord.Interaction, input_text: str, repeats_count: int):
    return_text = ""
    for _ in range(repeats_count):
        return_text += input_text + "\n"
    await interaction.response.send_message(return_text)


# Command to synchronizes the slash commands from the code
@tree.command(name='sync_commands', description="Syncs the commands onto the server. May require to reload the page.", guild=GUILD)
@app_commands.describe(input_password="Enter the password to validate the action.")
async def sync_commands(interaction: discord.Interaction, input_password: str):

    if input_password == PASSWORD:
        
        # Synchronizes the commands into the tree
        await tree.sync()
    else:
        await interaction.response.send_message("Incorrect password.")


# TODO rework or remove. A command to publish leetcodes onto the server ?
@tree.command(name='leetcode_report', description="This will report the latest leetcodes completed.", guild=GUILD)
@app_commands.describe(username="The target user.")
async def leetcode_report(interaction: discord.Interaction, username: str):

    await interaction.response.send_message(f"User:{username}")


# Command to add a new emoji-role pair to the "database" file.
@tree.command(name='add_emoji_role_pair', description="This allows users to add a new emoji-role relation into the database. Requires the password.", guild=GUILD)
@app_commands.describe(input_password="Password to validate the request.", input_emoji="The emoji that will be associated to the role.", input_role="The role associated to the emoji.")
async def add_emoji_role_pair(interaction: discord.Interaction, input_password: str, input_emoji: str, input_role: str):

    # If the password is correct
    if input_password == PASSWORD:
        
        # Attempts to find the role by ID on the guild.
        try:
            role_name = interaction.guild.get_role(int(input_role)).name
        except:
            print("Provided ID did not match an existing role.")
            await interaction.response.send_message("Provided ID did not match an existing role.")

        # Adds the pair to the database file.
        with open('data/emojis_roles.txt', mode ='a', encoding='utf-8') as file:
            line = "\n" + input_emoji + "," + input_role + "," + role_name
            file.write(line)
        file.close()
        await interaction.response.send_message(f"## Command result:\nSuccessfully added the pair **Emoji**: {input_emoji} - **Role**: {role_name} to the database.")
    else:
        await interaction.response.send_message("Incorrect password.")

# On join / leave role, post messages accordingly?

# Create a role (organise roles, give relevant permissions)

# Create a category (make it private)

# Create a text channel (in the category & private)

# Create a voice channel (in the category & private)

# A command that returns the list of common games for a list of players based on their tags. Could be done using the emojis system as db ?

# Runs the bot
client.run(TOKEN)
# client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)