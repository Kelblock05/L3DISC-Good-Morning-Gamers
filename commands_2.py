import discord
from discord.ext import commands
import pytz
import datetime
from discord.ext import commands, tasks
import re
# setting the correct intents for this discord bot
intents = discord.Intents.default()
intents.dm_messages = True  # Allow DM messages
intents.guilds = True
intents.bans = True
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.members = True
intents.invites = True
bot = commands.Bot(command_prefix='b!', intents=intents, case_insensitive=True)
bot.remove_command('help')  # Remove the default help command

# List of allowed server IDs
allowed_servers = ['REPLACE WITH A SERVER ID', 'server 1','server 2']

# List of authorized user IDs
admin_users = ['REPLACE WITH A ADMIN DISCORD USER ID', 'user 1','user 2']

# The on ready event so the program waits untill a successful connection to the bot has been made


@bot.event
async def on_ready():

    print(f'Logged in as {bot.user.name}')
    # changes the activty of the bot (this is only done to make things look fancy on discord :D )
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name='Martini Mixing 🍸'
    )

    await bot.change_presence(activity=activity)


# The bot will leave a server if it has found itself in a discord server that is not valid
@bot.event
async def on_guild_join(guild):
    temp_guild = guild.id
    temp_guild = str(temp_guild)
    if temp_guild in allowed_servers:
        pass
    else:
        # Leaves the server if it's not in the allowed servers list
        await guild.leave()

# The aysnc function in charge of the on message events


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # stops users from trying to use the bot in direct messages with the bot (therefore you can only use the bot in valid discord servers)
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("Please use my functionality in a discord server not in direct messages Thanks =D")
        return
    if message.guild:
        guild_temp = str(message.guild.id)
        if guild_temp not in allowed_servers:
            # Sends a message when the bot is used in an external server
            embed = discord.Embed(
                title="The GMG Discord Bot only functions in the offical discord server: please use the bot in the valid server", color=discord.Colour.red())
            await message.channel.send(embed=embed)
            return

    await bot.process_commands(message)

# The custom help command


@bot.command(hidden=True)
async def help(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.channel.send("Please use my functionality in a discord server not in direct messages Thanks =D")
        return
    else:
        embed = discord.Embed(title="Bot Commands",
                              color=discord.Color.green())
        embed.add_field(name="**b!gmg ranks**\n\n",
                        value="Outputs the current\nGood Morning Gamers\nLeaderboard\n-----------------\n\n", inline=False)
        embed.add_field(name="**b!streak ranks**\n\n",
                        value="Outputs the current\n Good Morning Gamers Streak\nLeaderboard\n-----------------\n\n", inline=False)
        embed.add_field(name="**Good Morning Gamers**\n\n",
                        value="GMG is a mini game we play\nthat resets at 12:00am NZST (GMT+12)\n and improves your sleep trust =D\n-----------------\n\n", inline=False)
        embed.add_field(name="**Good Monkey Monday**\n\n",
                        value="Monkeeeeee yipeeeee\n-----------------\n\n", inline=False)
        embed.add_field(name="**b!admin_help**\n\n",
                        value="Just incase the admins\nforgot the bot commands...\n-----------------\n\n", inline=False)
        await ctx.channel.send(embed=embed)


#################################
# Stops the defult help command from overiding the custom help command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@bot.event
async def on_help_command(ctx, command):
    return
##################################

# The Admin help commands


@bot.command()
async def admin_help(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.channel.send("Please use my functionality in a discord server not in direct messages Thanks =D")
        return
    else:
        temp_auth = str(ctx.author.id)
        if temp_auth in admin_users:
            embed = discord.Embed(title="Admin Bot Commands",
                                  color=discord.Color.dark_teal())
            embed.add_field(name="**b!set_gmg_as {discord user id\}**\n\n",
                            value="Allows you to manually edit\nthe current GMG winner\n(doesn't affect leaderboard points)\n-----------------\n\n", inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="You are not authorized to use this command", color=discord.Colour.red())
            await ctx.send(embed=embed)

# The admin command to manaully edit who won GMG (DOES NOT CHANGE ANY POINTS THAT MUST BE DONE IN THE TEXT FILES)


@bot.command()
async def set_gmg_as(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.channel.send("Please use my functionality in a discord server not in direct messages Thanks =D")
        return
    else:
        discord_id = ctx.message.content.lower()
        discord_id = str(discord_id)
        discord_id = discord_id.replace("b!set_gmg_as", "")
        discord_id = discord_id.replace(" ", "")
        temp_auth = str(ctx.author.id)
        if temp_auth in admin_users:
            embed = discord.Embed(
                title=f"GMG is now set as {discord_id}", color=discord.Colour.teal())
            await ctx.send(embed=embed)
            file = open("currentgmg.txt", "w")
            file.write(f"<@{discord_id}>")

        else:
            # stops non authorized users from using this command
            embed = discord.Embed(
                title="You are not authorized to use this command", color=discord.Colour.red())
            await ctx.send(embed=embed)

# PLEASE ENTER YOUR DISCORD BOT TOKEN HERE #######################################################
bot.run('ENTER YOUR TOKEN HERE')
