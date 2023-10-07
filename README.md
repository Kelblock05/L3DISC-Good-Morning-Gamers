# Good-Morning-Gamers-DISC-L3-2023
This my Level 3 Digital Science Project: The Good Morning Gamers Discord Bot

## Authors

- [@Brosnank10101](https://github.com/Brosnank10101) & [@Kelblock05](https://github.com/Kelblock05) 
- Same Developer ones my school account and the other is my personal account you get the point...

## How To Use My Discord Bot

My Discord bot has pretty simple easy to use commands with the command prefix: b!

- b!gmg ranks - Displays the current Good Morning Gamers Points Leaderboard
  
- b!streak ranks - Displays the current Good Morning Gamers Streak Leaderboard
  
- good morning gamers - To interact with the minigame event good morning gamers

- b!set_gmg_as - An admin command that allows the admin to manunally edit the current winner of GMG
- Example: b!set_gmg_as 944400624269811783 - Sets winner to user 944400624269811783 (The format uses discord user ID's)

- Good Morning Gamers resets at 12 : 00 : 00 AM NZST
  
## Requirements
- [The latest version of python](https://www.python.org/downloads/)<br />Python 3.12 is best however Python 3.8 or higher should work fine anything lower you will run into problems. 

- [A Discord Account](https://discord.com/register) and a discord bot 
  [application](https://discord.com/developers/docs/game-sdk/applications) is required.
  


## How to Setup a Discord Bot

![](https://i.imgur.com/evQaq2W.png)
- Go to the discord developer portal go to [applacations](https://discord.com/developers/applications) and either sign in with your discord account or register a new discord account. 

![](https://i.imgur.com/fJGJi0A.png)
- Create a new applacation, name your applacation and click confirm to the terms and conditions.

![](https://i.imgur.com/EByG0G3.png)
- Got to bot.

![](https://i.imgur.com/ih1wtnJ.png)
- create a new bot and click yes create a bot

![](https://i.imgur.com/PS82HSs.png)

- Reset the token and copy it and keep it somewhere safe.
  Using this token copy it and paste into every token variable across the files
![](https://i.imgur.com/CmU3KfB.png)

![](https://i.imgur.com/glJqwY4.png)

- Under Bot enable all the gateway intents like I have here.

![](https://i.imgur.com/7AcPs3M.png)

- Go to OAuth2 and go to url editor select the scopes and bot perms that I have selected. Copy the URL and paste it into a new tab and add it to your discord server.<br /><br />If your confuesed on how to make a discord server here is a quick tutorial I found on youtube:<br />https://www.youtube.com/watch?v=VZUIvADKuu4&ab_channel=TechInsider

## How to setup the Good Morning Gamers Discord Bot

- First place you're discord bot token in every token variable
![](https://i.imgur.com/CmU3KfB.png)

- Get the channel id's of all you're valid discord servers that you wish the discord bot to operate in

![](https://i.imgur.com/PhKNwdz.png)

- Copy those channel id's and paste them into every "allowed_servers" list

- Follow the same instructions for the allowed users: to use admin commands the lists will be called "admin_users"
![](https://i.imgur.com/3fRbso1.png)

- You will require to make changes to the two dictionary text files "gmg" and "streak"
![](https://i.imgur.com/xY9rd5O.png)

- find any three users in you're discord server and add them where the "000000000000000000" are located, once that has been done in both files delete the comments that I added for functionality of the discord bot.

## Download all the python modules in the requirements.txt file

 - There you go your discord bot is all setup you just need to run MAIN.PY and it enjoy =D
