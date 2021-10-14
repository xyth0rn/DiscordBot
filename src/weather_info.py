# https://openweathermap.org/current#data
import discord
from discord.ext import commands
import requests, json
from datetime import datetime

def get_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    api_key = 'e2268334f08849d9672d6415854ae1d7'

    response = requests.get(url + "appid=" + api_key + "&q=" + city)
    # convert json format data into python format data
    weather_data = response.json()
    '''
    weather_data

    {	'coord': {'lon': 121.0078, 'lat': 24.8383}, 
        'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 
        'base': 'stations', 
        'main': {'temp': 303.72, 'feels_like': 310.72, 'temp_min': 301.84, 'temp_max': 305.31, 'pressure': 1005, 'humidity': 75}, 
        'visibility': 10000, 
        'wind': {'speed': 1.34, 'deg': 300, 'gust': 4.02}, 
        'clouds': {'all': 82}, 
        'dt': 1625361711, 
        'sys': {'type': 2, 'id': 205017, 'country': 'TW', 'sunrise': 1625346662, 'sunset': 1625395758}, 
        'timezone': 28800, 
        'id': 1677112, 
        'name': 'Zhubei', 
        'cod': 200	}
    '''
    return weather_data
    
    '''
	weather = weather_data['weather'][0]
	main 	= weather_data['main']
	wind 	= weather_data['wind']
	sys 	= weather_data['sys']

    weather['main']
	weather['description']
	weather['icon']

	main['temp']/10			# C degree
	main['feels_like']/10	# C
	main['pressure']		# PA
	main['humidity']		# %

	wind['speed']			# m/s
	wind['deg']/10			# C
	wind['gust']			# m/s

	sys['sunrise']
	sys['sunset']
    '''

class Weather_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        help = '''
        Get the main weather info of a city.
        $weather <city>
            ex. $weather Zhubei
        ''',
        brief = "Get the main weather info of a city."
        )
    async def weather(self, ctx, city=None):
        if city == None:
            return await ctx.send('Error: No city input.')

        weather_data = get_weather(city)

        if weather_data['cod'] != 200:  # Invalid city
            return await ctx.send('Error: Invalid city.')
        
        else:
            weather = weather_data['weather'][0]

        return await ctx.send(
            """
            {}:
            The main weather is {}.
            {}
            """.format( city, weather['main'], weather['description'] )
        )
        
    @commands.command(
        help = '''
        Get the temperature, humidity, and pressure of a city.
        $temp_humid <city>
            ex. $temp_humid Zhubei
        ''',
        brief = "Get the temperature, pressure, and humidity of a city."
        )
    async def temp_humid(self, ctx, city=None):
        if city == None:
            return await ctx.send('Error: No city input.')

        weather_data = get_weather(city)

        if weather_data['cod'] != 200:  # Invalid city
            return await ctx.send('Error: Invalid city.')

        else:
            main 	= weather_data['main']

        return await ctx.send(
            """
            {}:
            The temperature is {}°​C (Feels like {}°​C)
            The humidity is {}%
            The pressure is {}PA
            """.format( city, main['temp']/10, main['feels_like']/10, main['humidity'], main['pressure'] )
        )

    @commands.command(
        help = '''
        Get the wind and gust speed of a city.
        $wind <city>
            ex. $wind Zhubei
        ''',
        brief = "Get the wind and gust speed of a city."
        )
    async def wind(self, ctx, city=None):
        if city == None:
            return await ctx.send('Error: No city input.')

        weather_data = get_weather(city)

        if weather_data['cod'] != 200:  # Invalid city
            return await ctx.send('Error: Invalid city.')

        else:
            wind 	= weather_data['wind']
        
        return await ctx.send(
            """
            {}:
            The approximate wind speed is {} m/s
            The approximate gust speed is {} m/s
            """.format( city, wind['speed'], wind['gust'] )
        )

    @commands.command(
        help = '''
        Get the sunrise and sunset time of a city.
        $sun <city>
            ex. $sun Zhubei
        ''',
        brief = "Get the sunrise and sunset time of a city."
        )
    async def sun(self, ctx, city=None):
        if city == None:
            return await ctx.send('Error: No city input.')
            
        weather_data = get_weather(city)

        if weather_data['cod'] != 200:  # Invalid city
            return await ctx.send('Error: Invalid city.')
        
        else:
            sys 	= weather_data['sys']
        
        return await ctx.send(
            """
            {}:
            Sunrise at {}.
            Sunset at {}.
            """.format( city, datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M:%S'), \
                datetime.fromtimestamp(sys['sunset']).strftime('%H:%M:%S') )
        )

def setup(bot):
    bot.add_cog(Weather_info(bot))