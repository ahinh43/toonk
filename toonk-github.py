import discord
import asyncio
import aiohttp
import traceback
import sys
import os
import re
import datetime
import time
from datetime import datetime,tzinfo,timedelta
from random import randint


class FakeMember():
    def __init__(self, name):
        self.name = name
 
class PlaceHolder():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return str(self.name)

        
print ('Logging into Discord...\n')
start = time.time()
EQTest = {}
SubDict = {}
guestEnabled = {}
EQPostDict = {}
EQPostDict2 = {}
EQPostDict3 = {}
serverName = {}
MPACount = 0
participantCount = {}
eightMan = {}
totalPeople = {}
appended = False
client = discord.Client()
ActiveMPA = list()
debugMode = False


def is_bot(m):
	return m.author == client.user
    
def is_not_bot(m):
    return m.author != client.user
def is_pinned(m):
    return m.pinned != True
    

getTime = datetime.now()


# REQUIRED IDS
# All of these fields need to be filled in order for the bot to work.
#input your user ID here
OWNER_ID = ''


# First server's channel you want to put the list into
SERVER1 = ''
# First server's ID
SERVER1ID = ''
# Second server's channel you want to put the list into
SERVER2 = ''
# Second server's ID
SERVER2ID = ''
# Third server's channel you want to put the list into
SERVER3 = ''
# Third server's ID
SERVER3ID = ''



async def generateList(message,inputstring):
    global MPACount
    global SERVER1
    global SERVER2
    global SERVER3
    pCount = 1
    nCount = 1
    sCount = 1
    mpaCount = 1
    alreadyWroteList = False
    mpaFriendly = ''
    playerlist = '\n'
    teamlist = '\n'
    serverlist = '\n'
    for word in EQTest[message.channel.name]:
        if (type(word) is PlaceHolder):
            playerlist += (str(nCount) + ". " + "" + '\n')
            teamlist += 'None' + '\n'
            serverlist += 'None' + '\n'
        else:
            splitstr = word.split()
            teamName = splitstr[0]
            serverName = splitstr[1]
            player = splitstr[2]
            if teamName.lower() == 'moonlight' and serverName.lower() == 'sonata':
                teamName = splitstr[0] + ' ' + splitstr[1]
                serverName = splitstr[2]
                player = splitstr[3]
                if len(splitstr) > 4:
                    for index in range(len(splitstr)):
                        if index == 0 or index == 1 or index == 2 or index == 3:
                            pass
                        else:
                            player+= ' ' + splitstr[index]
            else:
                if len(splitstr) > 3:
                    for index in range(len(splitstr)):
                        if index == 0 or index == 1 or index == 2:
                            pass
                        else:
                            player+= ' ' + splitstr[index]
            playerlist += (str(nCount) + ". " + player + '\n')
            teamlist += teamName + '\n'
            serverlist += serverName + '\n'
        pCount+=1
        nCount+=1
        if nCount == 13:
            playerlist += ('\n')
            nCount = 1

    if len(SubDict[message.channel.name]) > 0:
        playerlist += ('\n**Reserve List**:\n')
        for word in SubDict[message.channel.name]:
            playerlist += (str(sCount) + ". " + word + '\n')
            sCount += 1  
            
            
    em = discord.Embed(description='Use `^addme` to sign up. \nUse `^removeme` to remove yourself from the mpa \nIf the MPA list is full, signing up will put you in the reserve list.', colour=0x4DFFFF)
    em.add_field(name='Party Status', value='`' + str(participantCount[message.channel.name]) + '/' + str(totalPeople[message.channel.name]) + '`', inline=False)
    em.add_field(name='Participant List', value=playerlist, inline=True)
    em.add_field(name='From Team', value=teamlist, inline=True)
    em.add_field(name='Server Added From', value=serverlist, inline=True)
    em.add_field(name='Last Action', value=inputstring, inline=False)
    em.set_author(name='An MPA is starting!', icon_url=message.server.icon_url)
            
           
    try:
        await client.edit_message(EQPostDict[message.channel.name], '', embed=em)
        await client.edit_message(EQPostDict2[message.channel.name], '', embed=em)
        await client.edit_message(EQPostDict3[message.channel.name], '', embed=em)
    except:
        print(message.author.name + ' Started an MPA on ' + message.server.name)
        MPACount += 1
        print('Amount of Active MPAs: ' + str(MPACount))
        EQPostDict[message.channel.name] = await client.send_message(client.get_channel(SERVER1), '', embed=em)
        EQPostDict2[message.channel.name] = await client.send_message(client.get_channel(SERVER2), '', embed=em)
        EQPostDict3[message.channel.name] = await client.send_message(client.get_channel(SERVER3), '', embed=em) 
 
 

##  GENERAL COMMANDS ##
@client.event
async def on_message(message):
    global appended
    global MPACount
    global ActiveMPA
    global SERVER1
    global SERVER2
    global SERVER3
    global SERVER1ID
    global SERVER2ID
    global SERVER3ID
    global debugMode
    if message.content.startswith('^'):
		#Debugging commands
        # These commands are for Me (Tenj), or whoever runs this bot. 
        if message.content.lower() == '^^shutdown':
            if message.author.id == OWNER_ID:
                await client.send_message(message.channel, 'Shutting down...')
                await client.logout()
            else:
                await client.send_message(message.channel, 'You lack permissions to use this command.')
        elif message.content.lower() == '^^restart':
            if message.author.id == OWNER_ID:
                await client.send_message(message.channel, 'Toonk will now restart!')
                print ('The restart command was issued! Restarting Bot...')
                os.execl(sys.executable, *([sys.executable]+sys.argv))
            else:
                await client.send_message(message.channel, 'You lack permissions to use this command.')
        ## MPA TRACKER COMMANDS ##
        # Starts an MPA on all the channels the bot is configured for. The more servers this bot is configured for, the slower it will run for all servers.
               
        elif message.content.lower().startswith('^startmpa'):
            userstr = message.content
            userstr = userstr.replace("^startmpa", "")
            userstr2 = ''
            teamName = ''
            serverName = ''
            eightMan[message.channel.name] = False
            if message.channel.name == 'mpa-crossserver':
                # This checks if Toonk has the deleting permission. If it doesn't, don't run the script at all and just stop.
                try:
                    await client.delete_message(message)
                except discord.Forbidden:
                    print (message.author.name + ' Tried to start an MPA at {}, but failed.'.format(message.server.name))
                    await client.send_message(message.author, 'I lack permissions to set up an MPA! Did you make sure I have the **Send Messages** and **Manage Messages** permissions checked?')
                    return
                if not message.channel.name in EQTest:
                    if message.author.top_role.permissions.manage_emojis or message.author.id == OWNER_ID or message.author.top_role.permissions.administrator:
                        try:
                            if userstr == ' busterquest':
                                userstr2 = 'Buster Quest'
                            else:
                                userstr2 = userstr
                            if debugMode == False:
                                await client.send_message(client.get_channel(SERVER1), '{}'.format(message.server.roles[0]) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel(SERVER2), '{}'.format(message.server.roles[0]) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel(SERVER3), '{}'.format(message.server.roles[0]) + ' {}'.format(userstr2))
                            if userstr == ' 8man' or userstr == ' pvp' or userstr == ' busterquest':
                                eightMan[message.channel.name] = True
                            EQTest[message.channel.name] = list()
                            SubDict[message.channel.name] = list()
                            ActiveMPA.append(message.channel.name)
                            guestEnabled[message.channel.name] = False
                            participantCount[message.channel.name] = 0
                            if eightMan[message.channel.name] == True:
                                for index in range(8):
                                    EQTest[message.channel.name].append(PlaceHolder(""))
                                totalPeople[message.channel.name] = 8
                            else:
                                for index in range(12):
                                    EQTest[message.channel.name].append(PlaceHolder(""))
                                totalPeople[message.channel.name] = 12
                            await generateList(message, '```dsconfig\nStarting MPA. Please use !addme to sign up!```')
                        except discord.Forbidden:
                            print (message.author.name + 'Tried to start an MPA at {}, but failed.'.format(message.server.name))
                            await client.send_message(message.author, 'I lack permissions to set up an MPA! Did you make sure I have the **Send Messages** and **Manage Messages** permissions checked?')
                            return
                    else:
                        await client.send_message(message.channel, 'You do not have the permission to do that, starfox.')
                else:
                    await generateList(message, '```fix\nThere is already an MPA being made here!```')
            else:
                await client.send_message(message.channel, 'You can only start a MPA on a MPA channel!')
           
     
        # Removes the current MPA on the channel and cleans the channel up for the next one. Use this when the MPA is finished so the bot doesn't go insane on next MPA create.
                                 
        elif message.content.lower() == '^removempa':
            if message.author.top_role.permissions.manage_emojis or message.author.id == OWNER_ID or message.author.top_role.permissions.administrator:
                if message.channel.name == 'mpa-crossserver':
                    if message.channel.name in EQTest:
                        try:
                            del EQTest[message.channel.name]
                            MPACount -= 1
                            print(message.author.name + ' Closed an MPA on ' + message.server.name)
                            print('Amount of Active MPAs: ' + str(MPACount))
                            await client.purge_from(client.get_channel(SERVER1), limit=100, after=getTime)
                            await client.purge_from(client.get_channel(SERVER2), limit=100, after=getTime)
                            await client.purge_from(client.get_channel(SERVER3), limit=100, after=getTime)
                            participantCount[message.channel.name] = 0
                            index = ActiveMPA.index(message.channel.name)
                            ActiveMPA.pop(index)
                        except KeyError:
                            pass
                    else:
                        await client.send_message(message.channel, 'There is no MPA to remove!')
                else:
                    await client.send_message(message.channel, 'This command can only be used in a MPA channel!')
            else:
                await generateList(message, '```fix\nYou are not a manager. GTFO```')
                   
            #Adds a player into the MPA list on the current eq channel. Checks for a placeholder object to remove and inserts the user's user object into the list.
        elif message.content.lower().startswith('^addme'):
            bypassCheck = False
            userstr = ''
            classRole = ''
            index = 0
            personInMPA = False
            personInReserve = False
            if message.channel.name == 'mpa-crossserver':
                if message.channel.name in EQTest:
                    userstr = message.content
                    userstr = userstr.replace("^addme", "")
                    userstr = userstr.replace(" ", "")
                    for index, item in enumerate(EQTest[message.channel.name]):
                        if (type(EQTest[message.channel.name][index]) is PlaceHolder):
                            pass
                        elif message.author.name in item:
                            personInMPA = True
                            break
                    for index, item in enumerate(SubDict[message.channel.name]):
                        if message.author.name in item:
                            personInReserve = True
                            break
                    if userstr == 'reserve':
                        if personInMPA == False: 
                            await generateList(message, "```fix\nReserve list requested. Adding...```")
                            await client.delete_message(message)
                            if personInReserve == False:
                                SubDict[message.channel.name].append(message.author.name)
                                await generateList(message, '```diff\n+ Added {} to the Reserve list```'.format(message.author.name))
                            else:
                                await generateList(message, "```diff\n+ You are already in the Reserve List```")
                        else:
                            await generateList(message, "```fix\nYou are already in the MPA```")
                        return
                    if message.server.id == SERVER1ID:
                        teamName = 'Team1'
                        serverName = 'server1'
                    elif message.server.id == SERVER2ID:
                        teamName = 'Team2'
                        serverName = 'server2'
                    elif message.server.id == SERVER3ID:
                        teamName = 'Team3'
                        serverName = 'server3'
                    else:
                        teamName = 'Unaffiliated'
                        serverName = 'Somewhere'
                    await client.delete_message(message)
                    for word in EQTest[message.channel.name]:
                        if isinstance(word, PlaceHolder):
                            if personInMPA == False:
                                if (message.author.name in SubDict[message.channel.name]):
                                    index = SubDict[message.channel.name].index(message.author.name)
                                    if isinstance(EQTest[message.channel.name][0], PlaceHolder):
                                        EQTest[message.channel.name].pop(0)
                                        EQTest[message.channel.name][0] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][1], PlaceHolder):
                                        EQTest[message.channel.name].pop(1)
                                        EQTest[message.channel.name][1] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][2], PlaceHolder):
                                        EQTest[message.channel.name].pop(2)
                                        EQTest[message.channel.name][2] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][3], PlaceHolder):
                                        EQTest[message.channel.name].pop(3)
                                        EQTest[message.channel.name][3] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][4], PlaceHolder):
                                        EQTest[message.channel.name].pop(4)
                                        EQTest[message.channel.name][4] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][5], PlaceHolder):
                                        EQTest[message.channel.name].pop(5)
                                        EQTest[message.channel.name][5] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][6], PlaceHolder):
                                        EQTest[message.channel.name].pop(6)
                                        EQTest[message.channel.name][6] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][7], PlaceHolder):
                                        EQTest[message.channel.name].pop(7)
                                        EQTest[message.channel.name][7] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    if eightMan[message.channel.name] == False:
                                        if isinstance(EQTest[message.channel.name][8], PlaceHolder):
                                            EQTest[message.channel.name].pop(8)
                                            EQTest[message.channel.name][8] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][9], PlaceHolder):
                                            EQTest[message.channel.name].pop(9)
                                            EQTest[message.channel.name][9] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][10], PlaceHolder):
                                            EQTest[message.channel.name].pop(10)
                                            EQTest[message.channel.name][10] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][11], PlaceHolder):
                                            EQTest[message.channel.name].pop(11)
                                            EQTest[message.channel.name][11] = teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                else:
                                    if isinstance(EQTest[message.channel.name][0], PlaceHolder):
                                        EQTest[message.channel.name].pop(0)
                                        EQTest[message.channel.name].insert(0, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```css\n{} farted. I put him to top.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][1], PlaceHolder):
                                        EQTest[message.channel.name].pop(1)
                                        EQTest[message.channel.name].insert(1, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][2], PlaceHolder):
                                        EQTest[message.channel.name].pop(2)
                                        EQTest[message.channel.name].insert(2, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][3], PlaceHolder):
                                        EQTest[message.channel.name].pop(3)
                                        EQTest[message.channel.name].insert(3, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][4], PlaceHolder):
                                        EQTest[message.channel.name].pop(4)
                                        EQTest[message.channel.name].insert(4, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][5], PlaceHolder):
                                        EQTest[message.channel.name].pop(5)
                                        EQTest[message.channel.name].insert(5, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][6], PlaceHolder):
                                        EQTest[message.channel.name].pop(6)
                                        EQTest[message.channel.name].insert(6, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][7], PlaceHolder):
                                        EQTest[message.channel.name].pop(7)
                                        EQTest[message.channel.name].insert(7, teamName + ' ' + serverName + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    if eightMan[message.channel.name] == False:
                                        if isinstance(EQTest[message.channel.name][8], PlaceHolder):
                                            EQTest[message.channel.name].pop(8)
                                            EQTest[message.channel.name].insert(8, teamName + ' ' + serverName + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][9], PlaceHolder):
                                            EQTest[message.channel.name].pop(9)
                                            EQTest[message.channel.name].insert(9, teamName + ' ' + serverName + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][10], PlaceHolder):
                                            EQTest[message.channel.name].pop(10)
                                            EQTest[message.channel.name].insert(10, teamName + ' ' + serverName + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][11], PlaceHolder):
                                            EQTest[message.channel.name].pop(11)
                                            EQTest[message.channel.name].insert(11, teamName + ' ' + serverName + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                            else:
                                await generateList(message, "```fix\nYou are already in the MPA```")
                                break
                    if not appended:
                        if personInMPA == False: 
                            await generateList(message, "```css\nThe MPA is full. Adding to reserve list.```")
                            if personInReserve == False:
                                SubDict[message.channel.name].append(message.author.name)
                                await generateList(message, '```diff\n+ Added {} to the Reserve list```'.format(message.author.name))
                            else:
                                await generateList(message, "```css\nYou are already in the Reserve List```")
                        else:
                            await generateList(message, "```css\nYou are already in the MPA```")
                    appended = False                                
                else:
                    await client.send_message(message.channel, 'There is no MPA to add yourself to!')
                    return
            else:
                await client.delete_message(message)
                            
        #Adds a string/name of a player that the Manager wants into the MPA list.      
        elif message.content.lower().startswith('^add '):
            if message.author.top_role.permissions.manage_emojis or message.author.id == OWNER_ID or message.author.top_role.permissions.administrator:
                userstr = ''
                serverName = 'Manual'
                teamName = 'None'
                if message.channel.name == 'mpa-crossserver':
                    if message.channel.name in EQTest:
                        userstr = message.content
                        userstr = userstr.replace("^add ", "")
                        userstr = userstr.replace(" ", "")
                        if userstr == "":
                            await generateList(message, "```fix\nYou can't add nobody. Are you drunk?```")
                            appended = True
                        else:
                            for word in EQTest[message.channel.name]:
                                if isinstance(word, PlaceHolder):
                                    if not(userstr in EQTest[message.channel.name]):
                                        if isinstance(EQTest[message.channel.name][0], PlaceHolder):
                                            EQTest[message.channel.name].pop(0)
                                            EQTest[message.channel.name].insert(0, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][1], PlaceHolder):
                                            EQTest[message.channel.name].pop(1)
                                            EQTest[message.channel.name].insert(1, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][2], PlaceHolder):
                                            EQTest[message.channel.name].pop(2)
                                            EQTest[message.channel.name].insert(2, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][3], PlaceHolder):
                                            EQTest[message.channel.name].pop(3)
                                            EQTest[message.channel.name].insert(3, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][4], PlaceHolder):
                                            EQTest[message.channel.name].pop(4)
                                            EQTest[message.channel.name].insert(4, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][5], PlaceHolder):
                                            EQTest[message.channel.name].pop(5)
                                            EQTest[message.channel.name].insert(5, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][6], PlaceHolder):
                                            EQTest[message.channel.name].pop(6)
                                            EQTest[message.channel.name].insert(6, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][7], PlaceHolder):
                                            EQTest[message.channel.name].pop(7)
                                            EQTest[message.channel.name].insert(7, teamName + ' ' + serverName + ' ' + userstr)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                            appended = True
                                            break 
                                        if eightMan[message.channel.name] == False:
                                            if isinstance(EQTest[message.channel.name][8], PlaceHolder):
                                                EQTest[message.channel.name].pop(8)
                                                EQTest[message.channel.name].insert(8, teamName + ' ' + serverName + ' ' + userstr)
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                                appended = True
                                                break
                                            elif isinstance(EQTest[message.channel.name][9], PlaceHolder):
                                                EQTest[message.channel.name].pop(9)
                                                EQTest[message.channel.name].insert(9, teamName + ' ' + serverName + ' ' + userstr)
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                                appended = True
                                                break
                                            elif isinstance(EQTest[message.channel.name][10], PlaceHolder):
                                                EQTest[message.channel.name].pop(10)
                                                EQTest[message.channel.name].insert(10, teamName + ' ' + serverName + ' ' + userstr)
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                                appended = True
                                                break
                                            elif isinstance(EQTest[message.channel.name][11], PlaceHolder):
                                                EQTest[message.channel.name].pop(11)
                                                EQTest[message.channel.name].insert(11, teamName + ' ' + serverName + ' ' + userstr)
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(userstr))
                                                appended = True
                                                break
                        if not appended:
                            await generateList(message, "```css\nThe MPA is full. Adding to reserve list.```")
                            SubDict[message.channel.name].append(userstr)
                            await generateList(message, '```diff\n+ Added {} to the Reserve list```'.format(userstr))
                    else:
                        await client.send_message(message.channel, 'There is no MPA.')
                    await client.delete_message(message)
                else:
                    await client.send_message(message.channel, 'This command can only be used in a MPA channel!')
            else:
                await client.send_message(message.channel, "You don't have permissions to use this command")
            appended = False
        #Removes the user object from the MPA list.
        elif message.content.lower() == '^removeme':
            inMPA = False
            serverName = 'None'
            teamName = 'None'
            if message.channel.name == 'mpa-crossserver':
                if message.channel.name in EQTest:
                    await client.delete_message(message)
                    for index, item in enumerate(EQTest[message.channel.name]):
                        if (type(EQTest[message.channel.name][index]) is PlaceHolder):
                            pass
                        elif message.author.name in item:
                            EQTest[message.channel.name].pop(index)
                            EQTest[message.channel.name].insert(index, PlaceHolder(''))
                            participantCount[message.channel.name] -= 1
                            await generateList(message, '```diff\n- Removed {} from the MPA list```'.format(message.author.name))
                            if len(SubDict[message.channel.name]) > 0:
                                EQTest[message.channel.name][index] = SubDict[message.channel.name].pop(0)
                                participantCount[message.channel.name] += 1
                                await generateList(message, '```diff\n- Removed {} from the MPA list and added {}```'.format(message.author.name, EQTest[message.channel.name][index]))
                            inMPA = True
                            return
                    if inMPA == False:
                        for index, item in enumerate(SubDict[message.channel.name]):
                            if message.author.name in item:
                                teamName + ' ' + serverName + ' ' + SubDict[message.channel.name].pop(index)
                                await generateList(message, '```diff\n- Removed {} from the Reserve list```'.format(message.author.name))
                                return
                            else:
                                await generateList(message, '```fix\nYou were not in the MPA list in the first place.```')
                        if len(SubDict[message.channel.name]) == 0:
                            await generateList(message, '```fix\nYou were not in the MPA list in the first place.```')
        #Removes the player object that matches the input string that is given.
        elif message.content.lower().startswith('^remove'):
            teamName = 'None'
            serverName = 'None'
            if message.author.top_role.permissions.manage_emojis or message.author.id == OWNER_ID or message.author.top_role.permissions.administrator:
                if message.channel.name == 'mpa-crossserver':
                    if message.channel.name in EQTest:
                        if len(EQTest[message.channel.name]):
                                userstr = message.content
                                userstr = userstr.replace("^remove ", "")
                                for index in range(len(EQTest[message.channel.name])):
                                    appended = False
                                    if (type(EQTest[message.channel.name][index]) is PlaceHolder):
                                        pass
                                    elif userstr.lower() in EQTest[message.channel.name][index].lower():
                                        toBeRemoved = EQTest[message.channel.name][index]
                                        EQTest[message.channel.name][index] = userstr
                                        EQTest[message.channel.name].remove(userstr)
                                        EQTest[message.channel.name].insert(index, PlaceHolder(''))
                                        userstr = userstr
                                        participantCount[message.channel.name] -= 1
                                        await generateList(message, '```diff\n- Removed {} from the MPA list```'.format(toBeRemoved))
                                        if len(SubDict[message.channel.name]) > 0:
                                            EQTest[message.channel.name][index] = SubDict[message.channel.name].pop(0)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n- Removed {} from the MPA list and added {}```'.format(toBeRemoved, EQTest[message.channel.name][index]))
                                        appended = True
                                        break
                                if not appended:
                                    for index in range(len(SubDict[message.channel.name])):
                                        appended = False
                                        if userstr in SubDict[message.channel.name][index]:
                                            toBeRemoved = SubDict[message.channel.name][index]
                                            SubDict[message.channel.name][index] = userstr
                                            SubDict[message.channel.name].remove(userstr)
                                            userstr = userstr
                                            await generateList(message, '```diff\n- Removed {} from the Reserve list```'.format(toBeRemoved))
                                            appended = True
                                            break
                                if not appended:    
                                    await generateList(message, "```fix\nPlayer {} does not exist in the MPA list```".format(userstr))
                        else:
                            await client.send_message(message.channel, "There are no players in the MPA.")
                    else:
                        await client.send_message(message.channel, 'There is no MPA.')
                    await client.delete_message(message)
                else:
                    await client.send_message(message.channel, 'This command can only be used in a MPA Channel!')
            else:
                await generateList(message, "You don't have permissions to use this command")
        elif message.content.lower().startswith('^broadcast'):
            if message.channel.name.startswith('mpa-crossserver'):
                if message.author.top_role.permissions.manage_emojis or message.author.id == OWNER_ID or message.author.top_role.permissions.administrator:
                    userstr = message.content
                    userstr = userstr.replace("^broadcast", "")
                    await client.send_message(client.get_channel(SERVER1), userstr)
                    await client.send_message(client.get_channel(SERVER2), userstr)
                    await client.send_message(client.get_channel(SERVER3), userstr)
            await client.delete_message(message)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print ('Logged in to servers:')
    try:
        for item in client.servers:
            print (item)
    except:
        print ('Error fetching server list :( Restarting...')
        python = sys.executable
        os.execl(python, python, * sys.argv)
    end = time.time()
    loadupTime = (end - start)
    print ('Toonk is now ready\nFinished loadup in ' + time.strftime('%H hours, %M minutes, %S seconds', time.gmtime(loadupTime)))
    print('------')

client.run('key')