# importing all required moudles
import datetime
import logging
import threading
import time
import discord
import pytz
import subprocess
import os
import asyncio
import json
import re
from discord.ext import commands

# setting the correct intents for this discord bot

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.dm_messages = True
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='b!', intents=intents)

# PLEASE ENTER YOUR DISCORD BOT TOKEN HERE #######################################################
token = 'ENTER YOUR DISCORD BOT TOKEN HERE'


# The substring is what is always found in the currentgmg.txt file when there is valid winner
substring = '@'

# Writing the correct data to the currentgmg file incase nothing is found in the file to avoid errors

file = open("currentgmg.txt", "r")
content = file.readline()
file.close()

if substring not in content:
    timestamp_bypass = True
    gmg_has_been_won = False
    file = open("currentgmg.txt", "w")
    file.write("No one")
    file.close()
else:
    timestamp_bypass = False
    gmg_has_been_won = True

saved_gmg = str(content)

# The time thread is in charge of reseting GMG every 24 hours and resets it every 25 hours in case no one won gmg between 12AM to 1AM

# IF SOMEONE WON DURING 12AM TO 1AM IT DOES NOT RESET IT A SECOND TIME


def time_thread():
    while True:
        global timestamp_bypass, gmg_has_been_won, D, t, H, M, S, gmg_reset_time
        # assigning the time varables with datetime and pytz that reassign each loop
        dt = datetime.datetime.now(tz=pytz.UTC)
        t = dt.astimezone(pytz.timezone('NZ'))
        H, M, S = t.hour, t.minute, t.second
        D = t.strftime("%A")
        ms = t.strftime("%f")
        micro = ms[-3:]
        mil = ms[:3]

        D = str(D)

        if H == 0 and M == 0 and S == 0 and gmg_has_been_won == True:
            gmg_reset_time = (f'{H:02d} : {M:02d} : {S:02d} - {mil}.{micro}')
            gmg_reset_time = str(gmg_reset_time)
            if not gmg_has_been_won:
                gmg_has_been_won = True
            else:
                timestamp_bypass = False
                with open("currentgmg.txt", "w") as file:
                    file.write("No one")
                gmg_has_been_won = False
                time.sleep(120)

        if H == 1 and M == 0 and S == 0:
            with open("currentgmg.txt", "r") as file:
                content = file.readline()

            if substring not in content:
                timestamp_bypass = True
                time.sleep(120)


# Starts the time thread
time_th = threading.Thread(target=time_thread)
time_th.start()

# assigns the user cooldown dictionary as an empty list before going into the following async function
user_cooldown = {}


# The on message aysnc function event

@client.event
async def on_message(message):
    global substring
    global timestamp_bypass
    global saved_gmg
    global gmg_reset_time
    global gmg_has_been_won
    substring = '@'

    with open("currentgmg.txt", "r") as file:
        content = file.readline()

    if substring not in content:
        timestamp_bypass = True
        gmg_has_been_won = False
    else:
        timestamp_bypass = False
        gmg_has_been_won = True

    # Assigns all the data for the logs

    user_id = str(message.author.id).split('#')[0]
    channel_data = str(message.channel)
    server_id = message.guild.id
    channel_id = str(message.channel.id)
    user_log = await client.fetch_user(user_id)
    user_log = str(user_log).replace("#0", "")

    # ignores any messages sent to the discord bot: that were sent as a direct message
    if message.author == client.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        return

    # List of allowed server IDs so users can't add the bot to their own servers and win gmg else were
    # This is in place to avoid confuesion so all users can easily find where the winning message was sent

    # PLEASE ENTER YOUR ALLOWED SERVER ID'S ##########################################################################
    allowed_servers = ['REPLACE WITH A SERVER ID', 'server 1','server 2']

    if message.guild:
        server_id = str(message.guild.id)

        if server_id not in allowed_servers:
            # Sends a message when the bot is used in an external server that is not allowed
            await message.channel.send("The GMG Discord Bot only functions in the offical discord server: please use the bot in the valid server")
            return

    # Checks if the message contains good morning gamers
    if message.content.lower() in ('good morning gamers', 'goodmorninggamers', 'goodmorning gamers', 'good morninggamers', 'gamers morning good', 'morning good gamers'):
        # Cooldown to avoid user spam messages
        if user_id in user_cooldown:
            current_time = time.time()
            cooldown_time = 1

            if current_time - user_cooldown[user_id] < cooldown_time:
                return

        # Adds the user to the cooldown dictionary with the current timestamp
        user_cooldown[user_id] = time.time()
        with open("new_gmg_happened.txt", "r") as file:
            content = file.readline()
        if content == 'true':
            return
        with open("currentgmg.txt", "r") as file:
            content = file.readline()

        # Further info for GMG LOG
        message_url = message.jump_url

        # Gets timestamp of the GMG message
        flake = str(message.id).replace(" ", "").replace(
            "<", "").replace(">", "").replace("@", "")
        snowflake = int(flake)
        a = snowflake / 4194304 + 1420070400000
        a = int(a) / 1000
        from datetime import datetime
        ts_A = datetime.fromtimestamp(a, tz=pytz.timezone('NZ'))
        # more data for the gmg logs
        DATE = ts_A.strftime('%d / %m / %Y')
        TIME = ts_A.strftime('%I : %M : %S %p\n\n**Milliseconds:** %f')[:-3]
        timestamp_hour = ts_A.strftime('%H')

        timestamp_bypass = True

        # first gate of validation: the timestamp validation (checks if user message is in the valid hour)
        if timestamp_bypass:
            timestamp_hour = '0'
            timestamp_bypass = False

        hour_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                     '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        if timestamp_hour in hour_list:
            # if the message is not in the valid hour it returns the message straight away with a return statement
            bot_message = (
                f'{content} Is the current winner, good luck next time!')
            bot_message = bot_message.replace('\n', '')
            await message.channel.send(f'{bot_message}')
            return

        # MAIN MESSAGE VALIDATION GATE IF THE MESSAGE PASSES IT IS THE WINNING MESSASGE ELSE IT'S THE LOSING MESSAGE
        if substring not in content and timestamp_hour not in hour_list and not gmg_has_been_won:
            # Writes the current channel ID of where the GMG winning message was sent so the streaks python file knows where to send it's message
            with open("channel_id.txt", "w") as file:
                file.write(f'{channel_id}')

            # Starts the streak python file
            cmd1 = 'python3 streak.py'
            p1 = subprocess.Popen(cmd1, shell=True)

            with open("currentgmg.txt", "r") as file:
                content = file.readline()
                if substring in content:
                    return
                else:

                    # Formats current winning user as the saved gmg incase of data loss
                    saved_gmg = str(message.author.mention).strip().replace(
                        " ", "").replace("!", "")
                    with open("currentgmg.txt", "w") as file:
                        file.write(saved_gmg)
                    with open("new_gmg_happened.txt", "w") as file:
                        file.write("true")

                    gmg_has_been_won = True

                    # The unique event that happens every monday gives two points instead of one point if it's monday
                    if D == 'Monday':
                        bot_message = (
                            f'{message.author.mention} You Are The Newest Epic Gamer and it\'s Monkey Monday so here\'s double points!!!')
                        bot_message = bot_message.replace('\n', '')
                        await message.channel.send(f'{bot_message}')
                    else:
                        # if it's not monday
                        bot_message = (
                            f'{message.author.mention} You Are The Newest Epic Gamer!')
                        bot_message = bot_message.replace('\n', '')
                        await message.channel.send(f'{bot_message}')

                    # CHANGE THIS TO YOUR OWN CHANNEL YOU WANT THE GMG LOGS TO SEND TO ########################################################
                    gmg_logs = client.get_channel(000000000000000000) # replace "000000000000000000" with your own channel id

                    with open("gmg_output.txt", "r") as file:
                        ranks = file.read()

                    # Sends the leaderboard output of the previous day as a log refrence
                    embed = discord.Embed(
                        title=f"Before GMG Reset Leaderboard {DATE}", description=f"```\n{ranks}\n```", color=discord.Colour.greyple())
                    await gmg_logs.send(embed=embed)
                    await asyncio.sleep(5)

                   # The next 160 lines is the leaderboard of the main points leaderboard for gmg

                    file = open("gmg_dictionary.txt", "r")
                    checking_if_gmg_exists = file.read()
                    file.close()
                    if saved_gmg in checking_if_gmg_exists:
                        pass
                    else:
                        with open(r'gmg_dictionary.txt', 'r') as file:  # appending new gmg
                            gmg_append = file.read()
                            gmg_append = gmg_append.replace("}", ",")
                        with open(r'gmg_dictionary.txt', 'w') as file:
                            file.write(gmg_append)
                        file = open("gmg_dictionary.txt", "a")
                        if D == 'Monday':
                            file.write("\n "+"\"" + saved_gmg + '\": 2}')
                        else:
                            file.write("\n "+"\"" + saved_gmg + '\": 1}')
                        file.close()

                    with open(r'gmg_dictionary.txt', 'r') as file:  # double quotes
                        DQ = file.read()
                        DQ = DQ.replace("\'", "\"")
                    with open(r'gmg_dictionary.txt', 'w') as file:
                        file.write(DQ)
                    with open('gmg_dictionary.txt') as f:
                        data = f.read()
                        js = json.loads(data)

                        # sorts the leaderboard from highest points to lowest
                        ranks = {k: v for k, v in (
                            reversed(sorted(js.items(), key=lambda item: item[1])))}
                    if saved_gmg in checking_if_gmg_exists:
                        before_update = ranks[f"{saved_gmg}"]
                        update_new_gmg_val = int(before_update)
                        if D == 'Monday':
                            update_new_gmg_val += 2
                        else:
                            update_new_gmg_val += 1
                        with open(r'gmg_dictionary.txt', 'r') as file:  # update gmg
                            old = str(f"\"{saved_gmg}\": {before_update}")
                            new = str(f"\"{saved_gmg}\": {update_new_gmg_val}")
                            UGMG = file.read()
                            UGMG = UGMG.replace(old, new)
                        with open(r'gmg_dictionary.txt', 'w') as file:
                            file.write(UGMG)
                    with open('gmg_dictionary.txt') as f:
                        data = f.read()
                        js = json.loads(data)
                        # sorts the leaderboard from highest points to lowest again
                        ranks = {k: v for k, v in (
                            reversed(sorted(js.items(), key=lambda item: item[1])))}
                    ranks = str(ranks)
                    file = open("gmg_dictionary.txt", "w")
                    file.write(ranks)
                    file.close()
                    # formatting the leaderboard
                    with open(r'gmg_dictionary.txt', 'r') as file:  # add newline
                        NL = file.read()
                        NL = NL.replace(",", "X")
                    with open(r'gmg_dictionary.txt', 'w') as file:
                        file.write(NL)

                    with open(r'gmg_dictionary.txt', 'r') as file:  # add newline
                        NL = file.read()
                        NL = NL.replace("X", ",\n")
                    with open(r'gmg_dictionary.txt', 'w') as file:
                        file.write(NL)
                    ranks = ranks.replace("{", "")
                    ranks = ranks.replace("}", "")
                    ranks = ranks.replace(":", "")
                    ranks = ranks.replace("\'", "")
                    ranks = ranks.replace("[", "")
                    ranks = ranks.replace("]", "")
                    ranks_list = ranks.split(",")
                    if os.path.isfile("gmg_format_1.txt"):
                        os.remove("gmg_format_1.txt")
                    logging.FileHandler('gmg_format_1.txt')
                    # sorts out the rank postions
                    for index, ranks_list in enumerate(ranks_list, start=1):
                        file = open("gmg_format_1.txt", "a")
                        file.write(f"#{index}  {ranks_list}")
                    file.close()
                    with open(r'gmg_format_1.txt', 'r') as file:  # add newline
                        NLO = file.read()
                        NLO = NLO.replace("#", "pp")
                    with open(r'gmg_format_1.txt', 'w') as file:
                        file.write(NLO)
                    with open(r'gmg_format_1.txt', 'r') as file:  # add newline
                        NLO = file.read()
                        NLO = NLO.replace("pp", "\n#")
                    with open(r'gmg_format_1.txt', 'w') as file:
                        file.write(NLO)
                    with open(r'gmg_format_1.txt', 'r') as file:  # add newline
                        NLO = file.read()
                        NLO = NLO.replace(",", "")
                    with open(r'gmg_format_1.txt', 'w') as file:
                        file.write(NLO)
                    await asyncio.sleep(2)
                    # Opens the input and output files
                    with open('gmg_format_1.txt', 'r', encoding='utf-8') as input_file, open('gmg_output.txt', 'w', encoding='utf-8') as output_file:
                        # Iterates over each line in the input file
                        for line in input_file:
                            # finds each discord ID and converts it to a normal username
                            match = re.search(r'\d{18,19}', line)
                            if match:
                                discord_id = match.group()
                                user = await client.fetch_user(discord_id)
                                username = user.name
                                # The following 4 lines allow you to manually catch usernames and edit them if required: copy the 4 lines of code per username

                                # PLEASE EDIT THE CODE TO CATCH AND EDIT ANY USERNAME TO SUIT YOUR NEEDS
                                if username in ('a username to catch'):
                                    username = 'a username'  # enter your edit here
                                else:
                                    pass
                                line = line.replace(discord_id, username)
                                output_file.write(line)

                    await asyncio.sleep(1)

                    # Further formatting and removing non ASCII characters

                    with open('gmg_output.txt', 'r', encoding='utf-8') as file:
                        text = file.read()
                        text = text.replace("@", "")
                        text = text.replace("<", "")
                        text = text.replace(">", "")
                        text = text.replace("ī", "i")
                        with open('gmg_output.txt', "w", encoding='utf-8') as file:
                            file.write(text)
                    await asyncio.sleep(1)
                    with open('gmg_output.txt', 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    # Open the output file for writing
                    with open('gmg_output.txt', 'w', encoding='utf-8') as f:
                        for line in lines:
                            # Splits the lines into components (rank, username, score)
                            components = line.strip().split()
                            rank = components[0].replace(' ', '')
                            score = components[-1].replace(' ', '')
                            name = ' '.join(components[1:-1])
                            E = (f'{rank},{name},{score}\n')
                            f.write(f'{rank},{name},{score}\n')

                    await asyncio.sleep(1)

                    def clean_name(name):
                        # Removes any non-ASCII characters
                        name = name.encode('ascii', 'ignore').decode()
                        name = re.sub(r'[^\w\s\d\.\-\']+', '', name)
                        # Shortens usernames if longer than 16 characters
                        if len(name) > 16:
                            # adds "..." to usernames that were longer than 16 so the user knows there is more to that username
                            name = name[:13] + "..."
                        elif len(name) < 16:
                            name = name.ljust(16)
                        return name

                    with open('gmg_output.txt', 'r') as file:
                        lines = file.readlines()
                        leaderboard = []
                        for line in lines:
                            rank, name, score = line.strip().split(',')
                            rank = rank.strip()
                            name = clean_name(name.strip())
                            score = score.strip()
                            leaderboard.append((rank, name, score))
                        leaderboard.sort(
                            key=lambda x: int(x[0].replace("#", "")))
                        with open('gmg_output.txt', 'w', encoding='utf-8') as output_file:
                            for rank, name, score in leaderboard:
                                # Adjusts spacing based on rank: so if the rank is less than 10 it gets 2 spaces else it gets 1 so flow is continued with formating
                                spacing = " " * \
                                    (2 if int(rank[1:]) < 10 else 1)
                                output_file.write(
                                    f"{rank}{spacing}{name}  {score}\n")

                    await asyncio.sleep(50)
                    # Further info to be added to the gmg log: what is the current streak of the current user
                    with open("gmg_streak.txt", "r") as file:
                        content = file.readline()

                    content = str(content)
                    content_output = content.replace('has gotten', '').replace(
                        'gmg\'s in a row!!', '').replace(' ', '')
                    remove_id = re.search(
                        r"<@.*?>", content_output, flags=re.IGNORECASE)
                    remove_id = str(remove_id.group())
                    streak_val = str(content_output).replace(
                        f'{remove_id}', '')

                    # the main logged message of the winning GMG message
                    embed = discord.Embed(title=f"{user_log}", description=f"**Message:** {message.content}\n\n**Channel:** {channel_data}\n\n**Date:** {DATE}\n\n**Time:**  {TIME}\n\n**Reset Time:** {gmg_reset_time}\n\n**Current Streak:** {streak_val}\n\n**User Snowflake:** {user_id}\n\n**Server Snowflake:** {server_id}\n\n**Message Snowflake:** {message.id}\n\n**Jump to Message:** {message_url}", color=discord.Colour.gold())
                    await gmg_logs.send(embed=embed)
                    with open("gmg_output.txt", "r") as file:
                        ranks = file.read()
                        file.close()
                        # After leaderboard update log
                        embed = discord.Embed(
                            title=f"After GMG Reset Leaderboard {DATE}", description=f"```\n{ranks}\n```", color=discord.Colour.greyple())
                        await gmg_logs.send(embed=embed)

        else:
            # if a gmg message fails the winning message validation gates

            file = open("new_gmg_happened.txt", "r")
            content = file.readline()
            file.close()

            if 'true' in content:
                pass
            else:
                file = open("currentgmg.txt", "r")
                content = file.readline()
                file.close()

                if 'No one' in content:
                    pass
                else:
                    bot_message = (
                        f'{content} Is the current winner, good luck next time!')
                    bot_message = bot_message.replace('\n', '')
                    await message.channel.send(f'{bot_message}')


client.run(token)
