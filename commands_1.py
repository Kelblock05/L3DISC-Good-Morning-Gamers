# The command files were seperated for testing reasons however it was just easier to work on each file separately so they remain as 2 files long term


# Importing all required moudles
import time
from discord.ext import admin_users
import threading
import discord
import pytz

# a list of authorised users to use private admin admin_users

auth_private_users = ['REPLACE WITH A ADMIN DISCORD USER ID', 'user 1','user 2']

# List of allowed server IDs so users can't add the bot to their own servers and win gmg else were
# This is in place to avoid confuesion so all users can easily find where the winning message was sent

# PLEASE ENTER YOUR ALLOWED SERVER ID'S ##########################################################################

allowed_servers = ['REPLACE WITH A SERVER ID', 'server 1','server 2']

global dela_complete
global dela_trigger
dela_trigger = False
dela_complete = True

# writes to file if they happen to not exist or having missing required data

with open("new_gmg_happened.txt", "r") as file:
    rank_delay = file.readline()
    file.close()

if "delay_is_over" not in rank_delay:
    with open("new_gmg_happened.txt", "w") as file:
        if "true" in rank_delay:
            file.write("delay_is_over")
            file.close()
        else:
            file.write("delay_is_over")
            file.close()


def min_delay():
    # This functions job is to create a seprate delay so a user can't see the leaderboards untill a minute has passed since gmg was activated
    # the reason why this is in place so it allows plenty of time for the leaderboard to refresh: stopping any errors from occuring
    global dela_trigger, dela_complete
    while True:
        file = open("new_gmg_happened.txt", "r")
        content = file.readline()
        file.close()

        if content.lower() == "true":
            time.sleep(60)
            file = open("new_gmg_happened.txt", "w")
            file.write("delay_is_over")
            file.close()
            dela_complete = True
            dela_trigger = False
        else:
            pass
        time.sleep(1)


# PLEASE ENTER YOUR DISCORD BOT TOKEN HERE #######################################################
token = 'PLEASE ENTER YOUR DISCORD BOT TOKEN HERE'


# all intents that are required for this bots functionality

intents = discord.Intents.default()
bot = admin_users.Bot(command_prefix='b!', intents=intents)
intents.typing = False
intents.members = True
intents.message_content = True
intents.presences = False
client = discord.Client(intents=intents)

# Below removes the default help command #####################

bot.remove_command('help')

client = discord.Client(intents=intents)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, admin_users.CommandNotFound):
        return


@bot.event
async def on_help_command(ctx, command):
    return


@bot.command(hidden=True)
async def help(ctx):
    return

#############################################################


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        return  # Ignore DMs

    if message.guild:
        server_id = str(message.guild.id)

        if server_id not in allowed_servers:
            # Sends a message when the bot is used in an external server that is not allowed
            # This is in place to avoid confuesion so all users can easily find where the winning message was sent
            await message.channel.send("The GMG Discord Bot only functions in the offical discord server: please use the bot in the valid server")
            return

    user_message_data = str(message.content).lower()
    # Assigns date and time using pytz and datetime moudles
    import datetime
    dt = datetime.datetime.now(tz=pytz.UTC)
    t = dt.astimezone(pytz.timezone('NZ'))
    H = (t.hour)
    M = (t.minute)
    S = (t.second)
    D = t.strftime("%A")
    t = str(t)
    D = str(D)

    # takes over the GMG file when there is the delay in place (For 1 minute after a user wins GMG)
    if user_message_data.lower() in ('good morning gamers', 'goodmorninggamers', 'goodmorning gamers', 'good morninggamers', 'gamers morning good'):
        file = open("new_gmg_happened.txt", "r")
        content = file.readline()
        file.close()
        if 'delay_is_over' in content:
            pass
        else:
            file = open("currentgmg.txt", "r")
            content = file.readline()
            file.close()
            sec_list = [57, 58, 59]
            if H == 23 and M == 59 and S in sec_list:
                return
            else:
                saved_gmg = str(message.author.mention).strip().replace(
                    " ", "").replace("!", "")
                if saved_gmg in content:
                    pass
                else:
                    await message.channel.send(f'{content} Is the current winner, good luck next time!')
        if D == 'Monday':
            min_list = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
            hour_list = [11]
            if M in min_list and H in hour_list:
                return
            else:
              # Sends the monkey monday video when it's monday during the unique event during the week
                await message.channel.send("Good Monkey Monday Fellow Gamers!", file=discord.File("gmm.mp4"))
                time.sleep(4)
        else:
            pass
    if user_message_data.lower() in ('good monkey monday', 'mondaymonkeygood', 'goodmonkeymonday', 'goodmonkey monday', 'good monkeymonday'):
        if D == 'Monday':
            await message.channel.send("Good Monkey Monday Fellow Gamers!", file=discord.File("gmm.mp4"))
        else:
            await message.channel.send("It\'s not monkey monday sad 😭")

    # The GMG ranks command
    if user_message_data.lower() in ('b!gmgranks', 'b! gmg ranks', '!bgmgranks', '!b gmg ranks', '!b gmgranks', '! b gmg ranks', 'b ! gmgranks', 'b!gmg ranks', 'b! gmgranks', '!b gmgranks'):
        with open("new_gmg_happened.txt", "r") as file:
            newgmghapp = file.read()
            file.close()

        if newgmghapp == "delay_is_over" and dela_complete == True:
            with open("gmg_output.txt", "r") as file:
                ranks = file.read()
                file.close()
                # sends the leaderboard as a code block so spacing is maintained for better readablity
                embed = discord.Embed(title="The Good Morning Gamers Leaderboard",
                                      description=f"```\n{ranks}\n```", color=discord.Colour.purple())
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="The Leaderboard is currently refreshing\nPlease wait for one minute", color=discord.Colour.red())
            await message.channel.send(embed=embed)

    # The GMG streak command

    if user_message_data.lower() in ('b!streakranks', 'b! streak ranks', '!bstreakranks', '!b streak ranks', '!b streakranks', '! b streak ranks', 'b ! streakranks', 'b!streak ranks', 'b! streakranks', '!b streakranks'):
        with open("new_gmg_happened.txt", "r") as file:
            newgmghapp = file.read()
            file.close()

        if newgmghapp == "delay_is_over" and dela_complete == True:
            with open("streak_output.txt", "r") as file:
                ranks = file.read()
                file.close()
                # sends the leaderboard as a code block so spacing is maintained for better readablity
                embed = discord.Embed(title="The Good Morning Gamers Streak Leaderboard",
                                      description=f"```\n{ranks}\n```", color=discord.Colour.blurple())
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="The Leaderboard is currently refreshing\nPlease wait for one minute...", color=discord.Colour.red())
            await message.channel.send(embed=embed)

# starts the delay thread and runs the discord bot
dela = threading.Thread(target=min_delay)
dela.start()
client.run(token)
