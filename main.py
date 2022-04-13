# If the bot isn't starting because an module is not installed, enter only the name in the requirements.txt (if this file doesn't exist create it in the root /home/container)
import discord
from discord.ext import commands
import datetime

from urllib import parse, request
import re

bot = commands.Bot(command_prefix='>', description="Nexer Hosting example Discord bot")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def sum(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne + numTwo)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Nexer Hosting example Discord bot", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    await ctx.send(embed=embed)

@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
    print(search_results)
    # I will put just the first result, you can loop the response to show more results
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])

# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Nexer Hosting example Discord bot", url="http://nexer-hosting.nl"))
    
    # Print this exact string to tell the control panel the bot has succesfully started. Otherwise it will eventualy restart because it doesn't start.
    print('Bot is ready!')


@bot.listen()
async def on_message(message):
    if " hosting " in message.content.lower():
        # in this case don't respond with the word "Hosting" or you will call the on_message event recursively
        await message.channel.send('Want some? Order now! https://nexer-hosting.nl')
        await bot.process_commands(message)

# Run the bot, paste the Discord bot token below
bot.run('GqCmZbr4TX4tTvv62ZchW8gM.DVEV93qVn63uESrnavv2q5RUkVya5HjyVv')
