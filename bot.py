from time import sleep
from pyrogram import Client, filters
import asyncio
import PIL
import requests

api_id = 'your id'
api_hash = 'your hash'
session_name = 'pyscrp'
bot = Client(session_name, api_id, api_hash)


@bot.on_message(filters.command("spam", prefixes=".") & filters.me)
async def spam_command(client, message):
    command = message.command
    if len(command) < 3:
        await message.edit("Usage: .spam [count] [message]")
        await asyncio.sleep(3)
        await message.delete()
        return

    try:
        count = int(command[1])
    except ValueError:
        await message.edit("Please, enter a vaild number.")
        await asyncio.sleep(3)
        await message.delete()
        return

    text = ' '.join(command[2:])

    await message.delete()

    for _ in range(count):
        sleep(0.25)
        await bot.send_message(message.chat.id, text)


def asci(url):
    img = PIL.Image.open(requests.get(url, stream=True).raw)

    # Resize the image
    width, height = img.size
    aspect_ratio = height / width
    new_width = 44
    new_height = aspect_ratio * new_width * 0.44
    img = img.resize((new_width, int(new_height)))

    # Convert to grayscale
    img = img.convert('L')

    chars = "█", "▓", "▒", ":", "=", "#", "%"

    # Convert to ASCII art
    pixels = img.getdata()
    new_pixels = [chars[pixel // 100] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # Split into rows of equal width
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index: index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    return ascii_image


@bot.on_message(filters.command("photo", prefixes=".") & filters.me)
async def to_ascii(client, message):
    command = message.command
    if len(command) < 2:
        await message.edit("Usage: .photo [url]")
        await asyncio.sleep(3)
        await message.delete()
        return

    url = command[1]
    try:
        ascii_art = asci(url)
        await bot.send_message(message.chat.id, f"photo:\n\n{ascii_art}")
    except Exception as e:
        await message.edit(f"Error processing the image: {str(e)}")
        await asyncio.sleep(3)
        await message.delete()


bot.run()
