#import libraries
import discord #DC api
import os #access env file
from dotenv import load_dotenv #load the env vars
from PIL import Image #handle img
import numpy as np  
from io import BytesIO #handle imgs
import aiohttp #fetch img
import easyocr # OCR
from colorama import Fore

# Load ENV
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()

# Enable all necessary intents manually
intents.message_content = True  # Allows reading message content
intents.guilds = True  # Allows bot to receive guild (server) updates
intents.members = True  # Allows bot to receive member updates (e.g., join/leave)
intents.reactions = True  # Allows bot to receive reaction events
intents.presences = True  # Allows bot to see members' presence (status)
intents.typing = True  # Allows bot to receive typing notifications
intents.messages = True  # Allows bot to receive message events
intents.dm_messages = True  # Allows bot to receive direct messages
intents.guild_messages = True  # Allows bot to receive messages in servers
intents.guild_reactions = True  # Allows bot to receive reactions in servers
intents.guild_typing = True  # Allows bot to receive typing events in servers

# Create bot client with the specified intents
client = discord.Client(intents=intents)

# Set lang
reader = easyocr.Reader(['en'])

#File Extraction Function
async def extractTextFromImg(image_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image = Image.open(BytesIO(image_data)).convert('RGB')
                    image_array = np.array(image)

                    result = reader.readtext(image_array, detail=0)
                    text = "\n".join(result)

                    return text.strip() if text.strip() else "No Text Found"
                
                else:
                    return "Error: Unable To Fetch Image, Please Try Again"
                
    except Exception as e:
        return f"Error: {str(e)}"
#Check if The Bot Is Alived 
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):#Checks if the message is from the bot itself
    if message.author == client.user:
        return

    if message.attachments:  
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image'): 
                await message.channel.send("Extracting Text....")
                extracted_text = await extractTextFromImg(attachment.url)
                await message.channel.send(f"{extracted_text}")

client.run(DISCORD_TOKEN)
