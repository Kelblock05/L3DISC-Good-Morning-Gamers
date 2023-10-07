# Importing all required moudles
import discord
import re
import os
import asyncio
import json
import traceback
import logging
from discord.ext import tasks
from discord.ext import commands
# setting the correct intents for this discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.dm_messages = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
token = 'ENTER YOUR TOKEN HERE' # PLEASE ENTER YOUR DISCORD BOT TOKEN HERE #######################################################

# The streaks file is setup pretty much the exact same as the gmg file since it uses the same leaderboard, the only diffrence is: instead of adding points to user each time they win
# the user gets points when they beat their previous streak.

@bot.event
async def on_ready():
    await streak_task()
    # WHEN THE STREAK TASK IS COMPLETE THE SCRIPT EXITS AND CLOSES AND IS THEN REOPENED BY THE GMG.PY FILE.
    await bot.close()
@bot.event
async def streak_task():
      await asyncio.sleep(1)
      with open("currentgmg.txt", "r") as file:
        saved_gmg = file.readline()
        saved_gmg = str(saved_gmg).replace(" ", "").replace("!", "")
        
      with open("channel_id.txt", "r") as file:
        # This is where it gathers the channel id from the channel id text file. The channel id is written to that file from the gmg file so the streaks
        # file knows where to send the gmg embed message to.
        channel_id = file.readline()
        channel_id = int(channel_id)
        channel_id = bot.get_channel(channel_id)
        
      with open("gmg_streak.txt", "r") as file:
          content = file.readline()
          
      content = str(content)


    # formatting gmg_streak.txt to get the value of the current streak, as well as checking if the current winner of gmg is the same user in the gmg_streak.txt file
    # if the user is the same it adds another point towards that user, if that gets that user higher than there previous streak highscore it continues with the leaderboard. If
    # it's not higher it ignores the leaderboard and quits the file.

    # IF the user in gmg_streak.txt is not the same as the current gmg winner the current streak value is reset to 1.
      
      content_output = content.replace('has gotten','').replace('gmg\'s in a row!!','').replace(' ','')
      current_streak_holder = re.search(r'<@(.+?)>', content_output)
      current_streak_holder = str(current_streak_holder.group())
      csh_id = str(current_streak_holder)
      csh_id = csh_id.replace('<@','').replace('>','')
      remove_id = re.search(r"<@.*?>", content_output, flags=re.IGNORECASE)
      remove_id = str(remove_id.group())
      content_output = str(content_output).replace(f'{remove_id}', '')

      with open("currentgmg.txt", "r") as file:
          current_gmg_winner = file.readline()
          current_gmg_winner = str(current_gmg_winner).replace('<@','').replace('>','')
      if current_gmg_winner in csh_id:
          try:
              streak = int(content_output)
          except:
              print('An Error Occured')
          streak += 1
          
          with open("gmg_streak.txt", "w") as file:
              file.write(f"{saved_gmg} has gotten {streak} gmg's in a row!!")


            # If the streak is greater than one it continues with the leaderboard if it's less than one it ignores the rest of the script

            # IF YOU WOULD LIKE TO SEE HOW THE LEADERBOARD FUNCTIONS PLEASE CHECK THE COMMENTS IN THE GMG.PY FILE

              
          if streak > 1:
              
              with open("gmg_streak.txt", "r") as file:
                  content = file.readline()
                  
              content = content.replace('<','').replace('>','').replace('@','')
              match = re.search(r'\d{18,19}', content)
              match = str(match.group())
              
              if match:
                  discord_id = csh_id
                  user = await bot.fetch_user(discord_id)
                  username = user.name
                  match = str(match)
                  match = match.replace('\'>','')
                  content = content.replace(f'{match}',f'{username}')

              embed = discord.Embed(title=f"{content}", color=discord.Colour.blue())
              await channel_id.send(embed=embed)
              
              leaderboard_continue = False

              file = open("streak_dictionary.txt", "r") 
              checking_if_streak_exists = file.read()
              file.close()
              if saved_gmg in checking_if_streak_exists:
                pass
              else:
                with open(r'streak_dictionary.txt', 'r') as file:
                  streak_append = file.read()
                  streak_append = streak_append.replace("}", ",")
                with open(r'streak_dictionary.txt', 'w') as file:
                  file.write(streak_append)
                file = open("streak_dictionary.txt", "a")
                file.write("\n "+"\""+ saved_gmg + '\": 2}') 
                file.close()
                leaderboard_continue = True

              with open(r'streak_dictionary.txt', 'r') as file:
                DQ = file.read()
                DQ = DQ.replace("\'", "\"")
              with open(r'streak_dictionary.txt', 'w') as file:
                file.write(DQ)
              with open('streak_dictionary.txt') as f:
                data = f.read()
                js = json.loads(data)
                ranks = {k: v for k, v in (reversed(sorted(js.items(), key=lambda item: item[1])))}
              if saved_gmg in checking_if_streak_exists:
                before_update = ranks[f"{saved_gmg}"]
                update_new_streak_val = int(before_update)
                if streak > update_new_streak_val:
                  update_new_streak_val = int(streak)
                  with open(r'streak_dictionary.txt', 'r') as file:
                    old = str(f"\"{saved_gmg}\": {before_update}")
                    new = str(f"\"{saved_gmg}\": {update_new_streak_val}")
                    Ustreak = file.read()
                    Ustreak = Ustreak.replace(old, new)
                  with open(r'streak_dictionary.txt', 'w') as file:
                    file.write(Ustreak)
                  leaderboard_continue = True
                else:
                  pass
              if leaderboard_continue == True:
                with open('streak_dictionary.txt') as f:
                  data = f.read()
                  js = json.loads(data)
                  ranks = {k: v for k, v in (reversed(sorted(js.items(), key=lambda item: item[1])))}
                ranks = str(ranks)
                file = open ("streak_dictionary.txt", "w")
                file.write(ranks)
                file.close()
                with open(r'streak_dictionary.txt', 'r') as file:
                  NL = file.read()
                  NL = NL.replace(",", "x")
                with open(r'streak_dictionary.txt', 'w') as file:
                  file.write(NL)

                with open(r'streak_dictionary.txt', 'r') as file:
                  NL = file.read()
                  NL = NL.replace("x", ",\n")
                with open(r'streak_dictionary.txt', 'w') as file:
                  file.write(NL)
                ranks = ranks.replace("{", "")
                ranks = ranks.replace("}", "")
                ranks = ranks.replace(":", "")
                ranks = ranks.replace("\'", "")
                ranks = ranks.replace("[", "")
                ranks = ranks.replace("]", "")
                ranks_list = ranks.split(",")
                if os.path.isfile("streak_format_1.txt"):
                  os.remove("streak_format_1.txt")
                logging.FileHandler('streak_format_1.txt')
                for index, ranks_list in enumerate(ranks_list, start=1):
                  file = open("streak_format_1.txt", "a")
                  file.write(f"#{index}  {ranks_list}")
                file.close()
                with open(r'streak_format_1.txt', 'r') as file:
                  NLO = file.read()
                  NLO = NLO.replace("#", "x")
                with open(r'streak_format_1.txt', 'w') as file:
                  file.write(NLO)
                with open(r'streak_format_1.txt', 'r') as file:
                  NLO = file.read()
                  NLO = NLO.replace("x", "\n#")
                with open(r'streak_format_1.txt', 'w') as file:
                  file.write(NLO)
                with open(r'streak_format_1.txt', 'r') as file:
                  NLO = file.read()
                  NLO = NLO.replace(",", "")
                with open(r'streak_format_1.txt', 'w') as file:
                  file.write(NLO)
                await asyncio.sleep(2)
                with open('streak_format_1.txt', 'r', encoding='utf-8') as input_file, open('streak_output.txt', 'w', encoding='utf-8') as output_file:
                  for line in input_file:
                    match = re.search(r'\d{18,19}', line)
                    if match:
                        discord_id = match.group()
                        user = await bot.fetch_user(discord_id)
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
                with open('streak_output.txt', 'r', encoding='utf-8') as file:
                    text = file.read()
                    text = text.replace("@", "")
                    text = text.replace("<", "")
                    text = text.replace(">", "")
                    text = text.replace("ī", "i")
                    with open('streak_output.txt', "w", encoding='utf-8') as file:
                        file.write(text)
                await asyncio.sleep(1)        
                with open('streak_output.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                with open('streak_output.txt', 'w', encoding='utf-8') as f:
                    for line in lines:
                        components = line.strip().split()
                        rank = components[0].replace(' ', '')
                        score = components[-1].replace(' ', '')
                        name = ' '.join(components[1:-1])
                        E = (f'{rank},{name},{score}\n')
                        f.write(f'{rank},{name},{score}\n')

                await asyncio.sleep(1)

                def clean_name(name):
                    name = name.encode('ascii', 'ignore').decode()
                    name = re.sub(r'[^\w\s\d\.\-\']+', '', name)
                    if len(name) > 16:
                        name = name[:13] + "..."
                    elif len(name) < 16:
                        name = name.ljust(16)
                    return name

                with open('streak_output.txt', 'r') as file:
                    lines = file.readlines()
                    leaderboard = []
                    for line in lines:
                        rank, name, score = line.strip().split(',')
                        rank = rank.strip()
                        name = clean_name(name.strip())
                        score = score.strip()
                        leaderboard.append((rank, name, score))
                    leaderboard.sort(key=lambda x: int(x[0].replace("#","")))
                    with open('streak_output.txt', 'w', encoding='utf-8') as output_file:
                        for rank, name, score in leaderboard:
                            spacing = " " * (2 if int(rank[1:]) < 10 else 1)
                            output_file.write(f"{rank}{spacing}{name}  {score}\n")
              else:
                pass

          else:
              return
      else:
          streak = 1
          with open("gmg_streak.txt", "w") as file:
              file.write(f"{saved_gmg} has gotten {streak} gmg's in a row!!")



bot.run(token)