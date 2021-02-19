import os
import random
import io
import aiohttp

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HTTP_URL = os.getenv('HTTP_URL')
NUM_IMAGES=os.getenv('NUM_IMAGES')
START_IMAGE_NUMBER=os.getenv('START_IMAGE_NUMBER')
END_IMAGE_NUMBER=os.getenv('END_IMAGE_NUMBER')
IMAGE_NUMBER_ZERO_PADDING_LENGTH=os.getenv('IMAGE_NUMBER_ZERO_PADDING_LENGTH')
IMAGE_FILE_EXTENSION=os.getenv('IMAGE_FILE_EXTENSION')

print(f'TOKEN: {TOKEN}');
print(f'HTTP_URL: {HTTP_URL}')
print(f'NUM_IMAGES: {NUM_IMAGES}')
print(f'START_IMAGE_NUMBER: {START_IMAGE_NUMBER}')
print(f'END_IMAGE_NUMBER: {END_IMAGE_NUMBER}')
print(f'IMAGE_NUMBER_ZERO_PADDING_LENGTH: {IMAGE_NUMBER_ZERO_PADDING_LENGTH}')
print(f'IMAGE_FILE_EXTENSION: {IMAGE_FILE_EXTENSION}')

client = discord.Client()

@client.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guilds:\n'
    )

    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    imageListLength = int(NUM_IMAGES)

    if message.content == 'O!':
        if(imageListLength > 0):
            randomFilenameIndex = random.randint(int(START_IMAGE_NUMBER), int(END_IMAGE_NUMBER))
            my_url = HTTP_URL + str(randomFilenameIndex).zfill(int(IMAGE_NUMBER_ZERO_PADDING_LENGTH)) + IMAGE_FILE_EXTENSION
            print(f'url to download: {my_url}')
            async with aiohttp.ClientSession() as session:
                async with session.get(my_url) as resp:
                    if resp.status != 200:
                        return await message.channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await message.channel.send(file=discord.File(data, 'awesome_O_image.png'))
        else:
            await message.channel.send(file=discord.File('panda.jpg'))

client.run(TOKEN)
