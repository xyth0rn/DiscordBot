import discord
from discord.ext import commands
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf   # yahoo finance
import mplfinance as mpf
import datetime as dt
from dateutil import relativedelta
import os
import os.path
from os import path
import requests as rq

class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        help = '''
        List popular stocks and their symbols.
        ''',
        brief = "List popular stocks and their symbols"
    )
    async def list_stocks(self, ctx):
        return await ctx.send('''
        Popular stocks:
        TSM (TSMC)
        TSLA (Tesla)
        GOOGL (Google)
        FB (Facebook)
        AAPL (Apple)
        NVDA (Nvidia)
        QCOM (Qualcomm)
        '''
        )

    @commands.command(
        help = '''
        Get the quote of a stock for the past year.
        $year <stock symbol>
            ex. $year TSM
        ''',
        brief = "Get the quote of a stock for the past year."
    )
    async def year(self, ctx, symbol=None):
        if symbol == None:
            return await ctx.send('''
            ERROR: No stock symbol.
            Please enter a valid stock symbol
            '''
            )

        today = str(dt.date.today())    # '2021-07-02'
        starting_day = str(dt.date.today() - relativedelta.relativedelta(months=12))
        data_frame = yf.download(symbol, start=starting_day, end=today, progress=False)
        if len(data_frame) == 0:
            return await ctx.send('''
            ERROR: Invalid stock symbol, no data found.
            Please enter a valid stock symbol
            '''
            )
        else:
            mpf.plot(data_frame, type='candle', mav=(5,22), volume=True, title="Daily Price : " + symbol,  savefig="stock_quote.png")
            original_path = r'stock_quote.png'
            changed_path = r'..\storage\stock_quote.png'

            
            if path.exists(changed_path):
                os.remove(changed_path)
            
            os.rename(original_path, changed_path)
            with open(changed_path, "rb") as fh:
                f = discord.File(fh, filename=changed_path)
            return await ctx.send(file=f)



    @commands.command(
        help = '''
        Get the quote of a stock for the past quarter.
        $quarter <stock symbol>
            ex. $quarter GOOGL
        ''',
        brief = "Get the quote of a stock for the past quarter."
        )
    async def quarter(self, ctx, symbol=None):
        if symbol == None:
            return await ctx.send('''
            ERROR: No stock symbol.
            Please enter a valid stock symbol
            '''
            )

        today = str(dt.date.today())    # '2021-07-02'
        starting_day = str(dt.date.today() - relativedelta.relativedelta(months=3))
        data_frame = yf.download(symbol, start=starting_day, end=today, progress=False)
        '''
        data_frame =
                        Open        High         Low       Close   Adj Close    Volume
        Date
        2020-07-01   56.970001   57.470001   56.759998   56.820000   55.865040   6866500
        2020-07-02   57.950001   59.070000   57.950001   58.619999   57.634785  10021200
        2020-07-06   60.669998   62.130001   60.560001   61.880001   60.840004  12725600
        2020-07-07   61.259998   61.500000   60.680000   60.709999   59.689663   6672300
        2020-07-08   61.639999   62.740002   61.500000   62.590000   61.538071   8721900
        ...                ...         ...         ...         ...         ...       ...
        2021-06-25  117.449997  117.930000  116.529999  116.529999  116.529999   6712800
        2021-06-28  117.290001  119.949997  117.180000  119.610001  119.610001  11026600
        2021-06-29  119.400002  120.290001  118.419998  120.230003  120.230003   7874900
        2021-06-30  120.160004  120.760002  119.010002  120.160004  120.160004   7924600
        2021-07-01  120.099998  120.205498  118.029999  118.419998  118.419998   8098992
            '''
        
        if len(data_frame) == 0:
            return await ctx.send('''
            ERROR: Invalid stock symbol, no data found.
            Please enter a valid stock symbol
            '''
            )
        else:
            mpf.plot(data_frame, type='candle', mav=(5,22), volume=True, title="Daily Price : " + symbol,  savefig="stock_quote.png")
            original_path = r'stock_quote.png'
            changed_path = r'..\storage\stock_quote.png'

            if path.exists(changed_path):
                os.remove(changed_path)
            
            os.rename(original_path, changed_path)
            with open(changed_path, "rb") as fh:
                f = discord.File(fh, filename=changed_path)
            return await ctx.send(file=f)


def setup(bot):
    bot.add_cog(Stock(bot))