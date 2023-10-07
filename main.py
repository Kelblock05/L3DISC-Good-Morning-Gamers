
import subprocess

# incase the current directory can't be found use the following code: this is more of a linux issue though

# import os
# os.chdir('/home/kelboink/Desktop/The_Bar/')

##############################################################

# Below starts up each required python file using subprocess

cmd1 = 'python3 commands_1.py'
p1 = subprocess.Popen(cmd1, shell=True)

cmd2 = 'python3 commands_2.py'
p2 = subprocess.Popen(cmd2, shell=True)

cmd3 = 'python3 gmg.py'
p3 = subprocess.Popen(cmd3, shell=True)


############### WARNING ##########################


# WARNING DO NOT USE THIS FILE TO START: STREAK.PY
# THE GMG.PY FILE DOES THAT NOT MAIN.PY
