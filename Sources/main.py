# -*- coding: utf-8 -*-

import discord
import os
import re
import bday
import user_db
import insta_importer
import http_port
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'])

@bot.command()
async def register(ctx, arg):
    date = str.strip(arg)
    author = ctx.message.author.mention
    if re.match(r"\d{2}\.\d{2}\.\d{4}", date) is None:
        await ctx.send(f"Sorry, {author}, can't register your bday due the unrecognized date format ;(")
    try:
        user_db.register_user(author, date)
        bday.schedule_bday(author, date)
        await ctx.send(f"Congrats, {author}, you've been registred :D")
    except Exception as e:
        await ctx.send(f"Sorry, {author}, can't register your bday due error: {e} ;(")
    

@bot.command()
async def instagram(ctx : discord.ext.commands.Context, arg):
    try:
        video = insta_importer.import_video(arg)
        emb = discord.Embed(title=video["title"], description=video["description"], url=video["url"])
        emb.set_image(url=video["preview"])
        emb.set_author(name=video['username'], url=f"https://instagram.com/{video['username']}", icon_url=video["usericon"])
        await ctx.send(embed=emb)

    except Exception as e:
        await ctx.send(f"Sorry, cannot upload the video: {e}")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print("Port: ", port )

    try:
        http_port.init(port)
        bot.run(os.environ['TOKEN'])
    except Exception as e:
        print(e)
    finally:
        http_port.uninit()