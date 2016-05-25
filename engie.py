import hashlib
import signal
import json
import sys
import time
import os
import RPi.GPIO as GPIO
from pprint import pprint
from datetime import datetime

#
# Initialize the GPIOS
#

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)


#
# A big function only to check if the token is valid enough in the time.
# Compare the Now.Date with the Date of the JSON's Date message according to the 'Duree' Data stored in JSON's object.
# I'm sure there is a lot of easy way to do this but I had only few time to complete this project.
#

def Compare_Date(date, now, duree):
    FindD = 0
    FindN = 0
    MinD = 0
    MinN = 0
    HeureD = 0
    HeureN = 0
    FindD = date.find(" ")
    FindN = date.find(" ")
    joursD = date[0:FindD]
    joursN = now[0:FindN]
    print 'DAYS  ', joursD, ' --- ', joursN
    if (joursD != joursN):
        return (1)
    print "OK 1"
    date = date[FindD + 1:]
    now = now[FindN + 1:]
    FindD = date.find(":")
    FindN = date.find(":")
    joursD = date[0:FindD]
    joursN = now[0:FindN]
    if (joursD != joursN):
        res = int(joursN) - int(joursD)
        if (res == 1):
            date = date[FindD + 1:]
            now = now[FindN + 1:]
            FindD = date.find(":")
            FindN = date.find(":")
            joursD = date[0:FindD]
            joursN = now[0:FindN]
            if (joursD > joursN):
                res = int(joursD) - int(joursN)
                print res
                if (res < 30):
                    return (1)
                else:
                    return (0)
        else :
            return (1)
    print "OK 2"
    date = date[FindD + 1:]
    now = now[FindN + 1:]
    FindD = date.find(":")
    FindN = date.find(":")
    joursD = date[0:FindD]
    joursN = now[0:FindN]
    if (joursN > joursD):
        res = int(joursN) - int(joursD)
        print res
        if (res > 30):
            return (1)
        else :
            print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOK"
    return (0)


#
# Create the commande line who is use to call mail.py 
#

def Create_awnser(data, user, today, eol, token, action, duree, ans):
        cmd = 'python send_mail.py '
        if (ans == 1):
            cmd += '\"Validation du token\" '
        else :
            cmd += '\"Refus du token\" '
        cmd += token
        cmd += " "
        cmd += today
        cmd += " "
        cmd += user
        cmd += " "
        cmd += "\""
        cmd += eol
        cmd += "\""
        cmd += " "
        cmd += "\""
        cmd += action
        cmd += "\""
        cmd += " "
        cmd += str(ans)
        return (cmd)

#
# First, I store all JSON's object data into variables to read them properly.
# Then, I compare date.now() with the date into the JSON's object. If the token is too hold, it returns 1 to the main.
# 
#

def Create_MD5(date): # Changer avec Today ( INVERSER)
    with open('Data.json') as data_file:
        data = json.load(data_file)
        user = data["user"]
        today = data["date"]
        eol = data["eolienne"]
        token = data["token"]
        action = data["intervention"]
        duree = data["duree"]
        print '--------'
        print 'Compare String'
        dateString = date.strftime('%d-%m-%Y %H:%M:%S')
        if ((Compare_Date(today, dateString, duree)) == 1):
            cmd = Create_awnser(data, user, today, eol, token, action, duree, 0)
            print cmd
            os.system(cmd)
            return (1)
        print 'DATESTRING ==> ', dateString
        md5 = user, today, eol, action
        s = ""
        for i in md5:
                s += str(i)
        bytes = str.encode(s)
        md5 = hashlib.md5(bytes)
        print 'Mon token hash :'
        print md5.hexdigest()
        print '--------'
        cmd = Create_awnser(data, user, today, eol, token, action, duree, 1)
        print cmd
        os.system(cmd)
        return (0)

#
# The main. It execute the 'explorenfc-basic' command and write the output into a text file.
# Then, it takes only one lane, the 'Title' one. It writes this lane into a .json file to extract all the Data
# Finally, I call my action function and switch ON/OFF GPIO's connected diodes depending the return.
#

while True:
    date = datetime.now()
    os.system('explorenfc-basic > res.txt')
    print'finish -----'
    state = 0
    file = open('res.txt', 'r')
    for line in file:
        line = line[:-1]
        if ('Title' in line):
            line = line[8:]
            f = open('Data.json','w')
            f.write(line)
            f.close()
            state = 1
    file.close()
    if (state == 1):
        with open('Data.json') as data_file:
            data = json.load(data_file)
        pprint(data)
        print 'Token Bertrand :'
        print(data["token"])
        print '--------'
        if ((Create_MD5(date)) == 0):
            GPIO.output(20, True)
        else :
            GPIO.output(21, True)
        print 'MAIL ENVOYE'
    else :
        GPIO.output(21, True)
    time.sleep(2)
    GPIO.output(21, False)
    GPIO.output(20, False)
    os.system('rm res.txt')
