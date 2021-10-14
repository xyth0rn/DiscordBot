import discord
from discord.ext import commands
import random
import re
import requests
from bs4 import BeautifulSoup
import os
from os import path
import argparse
from PIL import Image

def single(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('div', id='comic')
    for word in str(tag.contents[1]).split():
        if 'src=' in word:
            url = 'https:' + word[5:len(word)-1]
    
    # save images
    res = requests.get(url)
    
    comic_path = r'..\storage\xkcd.png'
    if path.exists(comic_path):
        os.remove(comic_path)

    if path.exists(comic_path):
        os.remove(comic_path)
            
    with open(comic_path, 'wb') as fh:
        fh.write(res.content)
    
    fh.close()


class Xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        help = '''
        Show a xkcd comic.
        $comic <index of comic>
        ''',
        brief = "Show a xkcd comic."
        )
    async def comic(self, ctx, idx=None):
        if idx == None:
            return await ctx.send('Error: No comic index input.')
        elif idx.isdigit() == False:
            return await ctx.send('Error: Invalid comic index.')

        response = requests.get('https://xkcd.com/'+str(idx)+'/')
        if response.status_code != 200:
            return await ctx.send('Error: Invalid comic index.')
        single(response)

        with open(r'..\storage\xkcd.png', 'rb') as fh:
            f = discord.File(fh, filename=r'..\storage\xkcd.png')
        
        f.close()
        return await ctx.send(file=f)
    
    @commands.command(
        help = '''
        Show a random xkcd comic.
        $random_comic
        ''',
        brief = "Show a random xkcd comic."
        )
    async def random_comic(self, ctx):
        idx = random.randint(1, 2466)
        response = requests.get('https://xkcd.com/'+str(idx)+'/')
        if response.status_code != 200:
            return await ctx.send('Error: Invalid comic index.')
        single(response)

        with open(r'..\storage\xkcd.png', 'rb') as fh:
            f = discord.File(fh, filename=r'..\storage\xkcd.png')
        f.close()
        return await ctx.send(file=f)

def setup(bot):
    bot.add_cog(Xkcd(bot))