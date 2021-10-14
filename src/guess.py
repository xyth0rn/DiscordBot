# 功能：猜數字

import random
import discord
from discord.ext import commands

class Game:
    def __init__(self):
        self.answer = ""
        self.a_count = 0
        self.b_count = 0

    
    def generate(self):
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(items)
    
        self.answer=''
        for i in range(4):
            self.answer+=str(items[i])
        print(self.answer)


class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game = Game()
        self.is_playing = 0

    @commands.command(
        help = "Play 1A2B, a number-guessing game.",
        brief = "Play 1A2B."
        )
    async def new_game(self, ctx):
        self.game.generate()
        self.is_playing = 1
        return await ctx.send('Game start!\nTake a 4-digit number guess by typing "$guess <4-digit-number>".')
    
    @commands.command(
        help = """
        Guess a 4-digit number. (need to start new game first)
        $guess <4-digit number>
            ex. $guess 1234
        """,
        brief = "Take a guess. (need to start new game first)"
    )
    async def guess(self, ctx, num):
        number = num
        # await ctx.send(number)
        if self.is_playing == 0:
            return await ctx.send('Wanna play 1A2B? Start a new round first! Insert "$new_game" to start a new round.')

        if number.isdecimal() != True or len(number) != 4:
            return await ctx.send('Error: Invalid input.\nPlease insert 4-digit number!')

        if number==self.game.answer:
            self.is_playing = 0
            return await ctx.send('Yay! You got it! Insert "$new_game" to play another round.')

        for i in range(4):
            for j in range(4):
                if i == j and number[i] == self.game.answer[j]:
                    self.game.a_count += 1
                    
                elif number[i] == self.game.answer[j]:
                    self.game.b_count+=1
        await ctx.send(str(self.game.a_count) + 'A' + str(self.game.b_count) + 'B')
        self.game.a_count=0
        self.game.b_count=0

    @commands.command(
        help = "End game.",
        brief = "End game."
        )
    async def end_game(self, ctx):
        self.is_playing = 0
        return await ctx.send('Game ended. The answer was ' + self.game.answer)

def setup(bot):
    bot.add_cog(Guess(bot))