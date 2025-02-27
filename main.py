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
intents.messages = True
client = discord.Client(intents=intents)

# Set lang
reader = easyocr.Reader(['en'])

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

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.attachments:  # FIXED: Used 'attachments' instead of 'attachment'
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image'):  # FIXED: Used 'startswith' instead of 'startwith'
                await message.channel.send("Extracting Text....")
                extracted_text = await extractTextFromImg(attachment.url)
                await message.channel.send(f"{extracted_text}")

client.run(DISCORD_TOKEN)
