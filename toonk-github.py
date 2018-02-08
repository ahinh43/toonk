import discord
import asyncio
import logging
import aiohttp
import traceback
import sys
import os
import re
import datetime
import subprocess
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
EQPostDict4 = {}
EQPostDict5 = {}
serverName = {}
MPACount = 0
participantCount = {}
eightMan = {}
totalPeople = {}
appended = False
client = discord.Client()
ActiveMPA = list()
debugMode = False
lastRestart = str(datetime.now())



def is_bot(m):
	return m.author == client.user
    
def is_not_bot(m):
    return m.author != client.user
def is_the_one(m):
    return m.id != '321847377659035648'
def is_pinned(m):
    return m.pinned != True
    

getTime = datetime.now()

with open("TEAMS.txt") as g:
    team = g.readlines()
    teamList = []
    for i in team:
        teamList.append(i.strip())
        
with open("classes.txt") as e:
    classesread = e.readlines()
    classes = []
    for i in classesread:
        classes.append(i.strip())


async def generateList(message,inputstring):
    global MPACount
    global serverList
    global teamList
    global classes
    pCount = 1
    nCount = 1
    sCount = 1
    mpaCount = 1
    alreadyWroteList = False
    teamIcon = ''
    serverIcon = ''
    hasIcon = False
    mpaFriendly = ''
    playerlist = '\n'
    classlist = '\n'
    serverlist = '\n'
    for word in EQTest[message.channel.name]:
        if (type(word) is PlaceHolder):
            playerlist += (teamList[7] + "" + '\n')
            serverlist += '<:noserver:408848508402008068>' + '\n'
            classlist += classes[10] + '\n'
        else:
            splitstr = word.split()
            teamName = splitstr[0]
            serverName = splitstr[1]
            classicon = splitstr[2]
            player = splitstr[3]
            if teamName.lower() == 'ishana':
                teamIcon = teamList[0]
                hasIcon = True
            elif teamName == '桜花':
                teamIcon = teamList[1]
                hasIcon = True
            elif teamName == '秋冬':
                teamIcon = teamList[2]
                hasIcon = True
            elif teamName.lower() == 'moonlightsonata':
                teamIcon = teamList[3]
                hasIcon = True
            elif teamName.lower() == 'nightwatchers':
                teamIcon = teamList[4]
                hasIcon = True
            elif teamName.lower() == 'sweetxtoxic':
                teamIcon = teamList[5]
                hasIcon = True
            elif teamName.lower() == 'etherealmelody':
                teamIcon = teamList[6]
                hasIcon = True
            else:
                teamIcon = teamList[7]
                hasIcon = False
            
            
            if serverName.lower() == 'ishana':
                serverIcon = teamList[0]
            elif serverName == '桜花':
                serverIcon = teamList[1]
            elif serverName.lower() == 'alliance':
                serverIcon = teamList[8]
            elif serverName.lower() == 'nightwatchers':
                serverIcon = teamList[4]
            elif serverName.lower() == 'etherealmelody':
                serverIcon = teamList[6]
            elif serverName.startswith('<:manual'):
                serverIcon = '<:manual:408866045156261890>'
            else:
                serverIcon = '<:noserver:408848508402008068>'
            
            if len(splitstr) > 4:
                for index in range(len(splitstr)):
                    if index == 0 or index == 1 or index == 2 or index == 3:
                        pass
                    else:
                        player+= ' ' + splitstr[index]
            if hasIcon == False:
                teamIcon = teamList[7]
            playerlist += (teamIcon + " " + player + '\n')
            serverlist += serverIcon + '\n'
            classlist += classicon + '\n'
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
            
            
    em = discord.Embed(description='Use `^addme` to sign up. \nOptionally you can add your class after addme. Example. `^addme br` \nUse `^removeme` to remove yourself from the mpa \nIf the MPA list is full, signing up will put you in the reserve list.', colour=0x4DFFFF)
    em.add_field(name='Party Status', value='`' + str(participantCount[message.channel.name]) + '/' + str(totalPeople[message.channel.name]) + '`', inline=False)
    em.add_field(name='Participant List', value=playerlist, inline=True)
    em.add_field(name='Class', value=classlist, inline=True)
    em.add_field(name='Server Added From', value=serverlist, inline=True)
    em.add_field(name='Last Action', value=inputstring, inline=False)
    em.set_author(name='An MPA is starting!', icon_url=message.server.icon_url)
            
           
    try:
        await client.edit_message(EQPostDict[message.channel.name], '', embed=em)
        await client.edit_message(EQPostDict2[message.channel.name], '', embed=em)
        await client.edit_message(EQPostDict3[message.channel.name], '', embed=em)
        await client.edit_message(EQPostDict4[message.channel.name], '', embed=em)
        await client.edit_message(EQPostDict5[message.channel.name], '', embed=em)
    except:
        print(message.author.name + ' Started an MPA on ' + message.server.name)
        MPACount += 1
        await client.send_message(client.get_channel('322466466479734784'), '```css\n' + message.author.name + ' Started an MPA on ' + message.server.name + '\nAmount of Active MPAs: ' + str(MPACount) + '```')
        print('Amount of Active MPAs: ' + str(MPACount))
        # Laplace
        EQPostDict[message.channel.name] = await client.send_message(client.get_channel('326883995641970689'), '', embed=em)
        # Alliance
        EQPostDict2[message.channel.name] = await client.send_message(client.get_channel('326875381477146624'), '', embed=em)
        # Ishana
        EQPostDict3[message.channel.name] = await client.send_message(client.get_channel('331388355289808897'), '', embed=em)
        # Ethereal Melody
        EQPostDict4[message.channel.name] = await client.send_message(client.get_channel('408379606161424394'), '', embed=em)
        # Night Watchers
        EQPostDict5[message.channel.name] = await client.send_message(client.get_channel('409233586735022080'), '', embed=em)
        
 
 

##  GENERAL COMMANDS ##
@client.event
async def on_message(message):
    global appended
    global MPACount
    global ActiveMPA
    global EQCHANNEL1
    global EQCHANNEL2
    global EQCHANNEL3
    global debugMode
    global classes
    if message.content.startswith('^'):
		#Debugging commands
        # These commands are for Me (Tenj), or whoever runs this bot. 
        if message.content.lower() == '^^shutdown':
            if message.author.id == '153273725666590720':
                if message.server.id == '159184581830901761':
                    await client.send_message(message.channel, 'Shutting down. If anything goes wrong during the downtime, please blame yui.')
                else:
                    await client.send_message(message.channel, 'DONT DO THIS TO ME MA-')
                await client.logout()
            else:
                await client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
        elif message.content.lower().startswith('^^leaveserver'):
            if message.author.id == '153273725666590720':
                userstr = message.content
                userstr = userstr.replace("^^leaveserver", "")
                userstr = userstr.replace(" ", "")
                await client.leave_server(client.get_server(userstr))
            else:
                await client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
        elif message.content.lower() == '^gethighestrole':
            if not message.channel.name.startswith('mpa'):
                await client.send_message(message.channel, message.author.top_role)
        elif message.content.lower() == '^checkmpamanagerperm':
            if not message.channel.name.startswith('mpa'):
                doIHavePermission = message.author.top_role.permissions.manage_emojis
                if doIHavePermission:
                    await client.send_message(message.channel, 'You have the permissions to start an MPA.')
                else:
                    await client.send_message(message.channel, 'You do not have the permission to start an MPA. Take a hike.')
        elif message.content.lower() == '^^restart':
            if message.author.id == '153273725666590720':
                await client.send_message(message.channel, 'Toonk will now restart!' )
                end = time.time()
                runTime = (end - start)
                await client.send_message(client.get_channel('322466466479734784'), 'Toonk is {}'.format(client.get_server('226835458552758275').roles[24].mention) + '\nRun time: ' + time.strftime('%H hours, %M minutes, %S seconds', time.gmtime(runTime)))
                print ('The restart command was issued! Restarting Bot...')
                os.execl(sys.executable, *([sys.executable]+sys.argv))
            else:
                await client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
        elif message.content.lower() == '^^update':
            if message.author.id == '153273725666590720':
                await client.send_message(message.channel, 'Updating bot...')
                print ('Pulling new bot file from gcloud bucket...')
                subprocess.call('gsutil cp gs://tonk/crossbottest.py crossbottest.py', shell=True)
                print ('Success!')
                await client.send_message(message.channel, 'Update success! Toonk will now restart!')
                print ('Restarting bot')
                await client.send_message(client.get_channel('322466466479734784'), 'Toonk is {}'.format(client.get_server('226835458552758275').roles[24].mention))
                os.execl(sys.executable, *([sys.executable]+sys.argv))
            else:
                await client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
        elif message.content.lower().startswith('^^debugmode'):
            if message.author.id == '153273725666590720':
                userstr = message.content
                userstr = userstr.replace("^^debugmode", "")
                userstr = userstr.replace(" ", "")
                if userstr == 'on':
                    debugMode = True
                    await client.send_message(message.channel, 'Debug mode enabled! Broadcasting of MPAs has been disabled!')
                elif userstr == 'off':
                    debugMode = False
                    await client.send_message(message.channel, 'Debug mode disabled! Broadcasting of MPAs has been reenabled!')
            else:
                await client.send_message(message.channel, 'Only Tenj may use this command.')
        elif message.content.lower() == '^^lastrestart':
            if message.author.id == '153273725666590720':
                await client.send_message(message.channel, str(lastRestart))
            else:
                await client.send_message(message.channel, 'Only Tenj may use this command.')
        elif message.content.lower().startswith('^eval'):
            if message.author.id == '153273725666590720':
                userstr = message.content
                userstr = userstr.replace("^eval", "")
                try:
                    result = eval(userstr)
                except Exception:
                    formatted_lines = traceback.format_exc().splitlines()
                    await client.send_message(message.channel, 'Failed to Evaluate.\n```py\n{}\n{}\n```'.format(formatted_lines[-1], '/n'.join(formatted_lines[4:-1])))
                    return

                if asyncio.iscoroutine(result):
                    result = await result

                if result:
                    await client.send_message(message.channel, 'Evaluated Successfully.\n```{}```'.format(result))
                    return
            else:
                await client.send_message(message.channel, 'No.')
        ## MPA TRACKER COMMANDS ##
        #Starts the MPA on the current eq channel. Places the channel name into a dictionary and sets it to be a list. Then fills the list up with 12 placeholder objects.
               
        elif message.content.lower().startswith('^startmpa'):
            userstr = message.content
            userstr = userstr.replace("^startmpa", "")
            userstr2 = ''
            teamName = ''
            serverName = ''
            permissions = False
            eightMan[message.channel.name] = False
            if message.channel.name == 'mpa-crossserver':
                # This checks if Tonk has the deleting permission. If it doesn't, don't run the script at all and just stop.
                try:
                    await client.delete_message(message)
                except discord.Forbidden:
                    print (message.author.name + ' Tried to start an MPA at {}, but failed.'.format(message.server.name))
                    await client.send_message(message.author, 'I lack permissions to set up an MPA! Did you make sure I have the **Send Messages** and **Manage Messages** permissions checked?')
                    return
                if message.author.top_role.permissions.manage_emojis:
                    permissions = True
                elif message.author.top_role.permissions.administrator:
                    permissions = True
                elif message.author.id == '153273725666590720':
                    permissions = True
                else:
                    print('FALSE')
                    print(message.author.top_role)
                    print(message.author.top_role.permissions.administrator)
                    print(message.author.top_role.permissions.manage_emojis)
                if not message.channel.name in EQTest:
                    if permissions:
                        try:
                            if userstr == ' busterquest':
                                await client.send_message(message.channel, 'Would you like to say anything else? (Yes/no)')
                                prompt = await client.wait_for_message(author=message.author, timeout=10)
                                if prompt.content.lower() != 'yes':
                                    userstr2 = 'Buster Quest'
                                else:
                                    await client.send_message(message.channel, 'Please enter what you want to say')
                                    userstr2 = await client.wait_for_message(author=message.author, timeout=300)
                                    userstr2 = userstr2.content
                                    await client.purge_from(message.channel, limit=4, after=getTime)
                            else:
                                userstr2 = userstr
                            if debugMode == False:
                                if userstr2 == '':
                                    userstr2 == 'hi'
                                await client.send_message(client.get_channel('326883995641970689'), '{}'.format(message.server.default_role) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel('326875381477146624'), '{}'.format(message.server.default_role) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel('331388355289808897'), '{}'.format(message.server.default_role) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel('362247023191261195'), '{}'.format(message.server.default_role) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel('409233586735022080'), '{}'.format(message.server.default_role) + ' {}'.format(userstr2))
                                await client.send_message(client.get_channel('408379606161424394'), '{}'.format(userstr2))
                            elif message.author.id == '153273725666590720':
                                await client.send_message(client.get_channel('326883995641970689'), '*Tenj started this mpa. Ignoring everyone mention..*')
                                await client.send_message(client.get_channel('326875381477146624'), '*Tenj started this mpa. Ignoring everyone mention..*')
                                await client.send_message(client.get_channel('331388355289808897'), '*Tenj started this mpa. Ignoring everyone mention..*')
                                await client.send_message(client.get_channel('362247023191261195'), '*Tenj started this mpa. Ignoring everyone mention..*')
                                await client.send_message(client.get_channel('409233586735022080'), '*Tenj started this mpa. Ignoring everyone mention..*')
                                await client.send_message(client.get_channel('408379606161424394'), '*Tenj started this mpa. Ignoring everyone mention..*')
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
                            await client.send_message(message.author, 'I lack permissions to set up an MPA! Did you make sure I have the following permissions checked? \n**Send Messages**\n**Read Messages**\n**Manage Messages**')
                            return
                    else:
                        await client.send_message(message.channel, 'You do not have the permission to do that, starfox.')
                else:
                    await generateList(message, '```fix\nThere is already an MPA being made here!```')
            else:
                await client.send_message(message.channel, 'You can only start a MPA on a MPA channel!')
           
     
        # Removes the current MPA on the channel and cleans the channel up for the next one. Use this when the MPA is finished so the bot doesn't go insane on next MPA create.
                                 
        elif message.content.lower() == '^removempa':
            if message.author.top_role.permissions.manage_emojis or message.author.id == '153273725666590720' or message.author.top_role.permissions.administrator:
                if message.channel.name == 'mpa-crossserver' or message.channel.id == '322466466479734784':
                    if message.channel.name in EQTest:
                        try:
                            del EQTest[message.channel.name]
                            MPACount -= 1
                            await client.send_message(client.get_channel('322466466479734784'), '```diff\n- ' + message.author.name + ' Closed an MPA on ' + message.server.name + '\n- Amount of Active MPAs: ' + str(MPACount) + '```')
                            print(message.author.name + ' Closed the MPA on ' + message.server.name)
                            print('Amount of Active MPAs: ' + str(MPACount))
                            await client.purge_from(client.get_channel('326883995641970689'), limit=100, after=getTime, check=is_pinned)
                            await client.purge_from(client.get_channel('326875381477146624'), limit=100, after=getTime, check=is_pinned)
                            await client.purge_from(client.get_channel('331388355289808897'), limit=100, after=getTime, check=is_pinned)
                            await client.purge_from(client.get_channel('362247023191261195'), limit=100, after=getTime, check=is_pinned)
                            await client.purge_from(client.get_channel('408379606161424394'), limit=100, after=getTime, check=is_pinned)
                            await client.purge_from(client.get_channel('409233586735022080'), limit=100, after=getTime, check=is_pinned)
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
        elif message.content.lower() == '^clearmpa':
            if message.author.top_role.permissions.manage_emojis or message.author.id == '153273725666590720' or message.author.top_role.permissions.administrator:
                if message.channel.name == 'mpa-crossserver' or message.channel.id == '322466466479734784':
                    if message.channel.name not in EQTest:
                        try:
                            await client.purge_from(client.get_channel('326883995641970689'), limit=100, check=is_pinned)
                            await client.purge_from(client.get_channel('326875381477146624'), limit=100, check=is_pinned)
                            await client.purge_from(client.get_channel('331388355289808897'), limit=100, check=is_pinned)
                            await client.purge_from(client.get_channel('362247023191261195'), limit=100, check=is_pinned)
                            await client.purge_from(client.get_channel('408379606161424394'), limit=100, check=is_pinned)
                            await client.purge_from(client.get_channel('409233586735022080'), limit=100, check=is_pinned)
                        except KeyError:
                            pass
                    else:
                        await client.send_message(message.channel, 'This command only works if there is no MPA active.')
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
                    if message.server.id == '189900848862724096':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '189914908328984576':
                                teamName = 'MoonlightSonata'
                                break
                            elif message.author.roles[index].id == '217335164987113472':
                                teamName = '桜花'
                                break                                
                            elif message.author.roles[index].id == '201230397596631040':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '323370572937560064':
                                teamName = '秋冬'
                                break                            
                            elif message.author.roles[index].id == '405607531843551244':
                                teamName = 'NightWatcher'
                                break
                            elif message.author.roles[index].id == '406164933294948363':
                                teamName = 'EtherealMelody'
                                break
                            elif message.author.roles[index].id == '407778610049449986':
                                teamName = 'SWEETxTOXIC'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'Alliance'
                    elif message.server.id == '153346891109761024':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '154465245488742400':
                                teamName = '桜花'
                                break
                            elif message.author.roles[index].id == '308890131648086017':
                                teamName = '桜花'
                                break
                            elif message.author.roles[index].id == '341220141222330368':
                                teamName = '桜花'
                                break
                            elif message.author.roles[index].id == '224757670823985152':
                                teamName = 'Not桜花'
                                break
                            else:
                                teamName = 'None'
                        serverName = '桜花'
                    elif message.server.id == '159184581830901761':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '191162764033523712':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '254207687242285066':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '215683325950427146':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '224757670823985152':
                                teamName = 'NotIshana'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'Ishana'
                    elif message.server.id == '196583395550167040':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '311141836976816129':
                                teamName = 'EtherealMelody'
                                break
                            elif message.author.roles[index].id == '198474022483263488':
                                teamName = 'EtherealMelody'
                                break
                            elif message.author.roles[index].id == '198474801461985280':
                                teamName = 'EtherealMelody'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'EtherealMelody'
                    elif message.server.id == '383153236909096961':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '409223101302439947':
                                teamName = 'NightWatchers'
                                break
                            elif message.author.roles[index].id == '409225525811216384':
                                teamName = 'NightWatchers'
                                break
                            elif message.author.roles[index].id == '409224931004645387':
                                teamName = 'NightWatchers'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'NightWatchers'
                    else:
                        teamName = 'Unaffiliated'
                        serverName = 'Somewhere'
                    if userstr.lower() == 'hu' or userstr.lower() == 'hunter':
                        classRole += ' ' + classes[0]
                    elif userstr.lower() == 'fi' or userstr.lower() == 'fighter':
                        classRole += ' ' + classes[1]
                    elif userstr.lower() == 'ra' or userstr.lower() == 'ranger':
                        classRole += ' ' + classes[2]
                    elif userstr.lower() == 'gu' or userstr.lower() == 'gunner':
                        classRole += ' ' + classes[3]
                    elif userstr.lower() == 'fo' or userstr.lower() == 'force':
                        classRole += ' ' + classes[4]
                    elif userstr.lower() == 'te' or userstr.lower() == 'techer':
                        classRole += ' ' + classes[5]
                    elif userstr.lower() == 'bo' or userstr.lower() == 'bouncer':
                        classRole += ' ' + classes[6]
                    elif userstr.lower() == 'br' or userstr.lower() == 'braver':
                        classRole += ' ' + classes[7]
                    elif userstr.lower() == 'su' or userstr.lower() == 'summoner':
                        classRole += ' ' + classes[8]
                    elif userstr.lower() == 'hr' or userstr.lower() == 'hero':
                        classRole += ' ' + classes[9]
                    else:
                        classRole += ' ' + classes[10]
                    await client.delete_message(message)
                    for word in EQTest[message.channel.name]:
                        if isinstance(word, PlaceHolder):
                            if personInMPA == False:
                                if (message.author.name in SubDict[message.channel.name]):
                                    index = SubDict[message.channel.name].index(message.author.name)
                                    if isinstance(EQTest[message.channel.name][0], PlaceHolder):
                                        EQTest[message.channel.name].pop(0)
                                        EQTest[message.channel.name][0] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][1], PlaceHolder):
                                        EQTest[message.channel.name].pop(1)
                                        EQTest[message.channel.name][1] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][2], PlaceHolder):
                                        EQTest[message.channel.name].pop(2)
                                        EQTest[message.channel.name][2] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][3], PlaceHolder):
                                        EQTest[message.channel.name].pop(3)
                                        EQTest[message.channel.name][3] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][4], PlaceHolder):
                                        EQTest[message.channel.name].pop(4)
                                        EQTest[message.channel.name][4] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][5], PlaceHolder):
                                        EQTest[message.channel.name].pop(5)
                                        EQTest[message.channel.name][5] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][6], PlaceHolder):
                                        EQTest[message.channel.name].pop(6)
                                        EQTest[message.channel.name][6] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][7], PlaceHolder):
                                        EQTest[message.channel.name].pop(7)
                                        EQTest[message.channel.name][7] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                        appended = True
                                        break
                                    if eightMan[message.channel.name] == False:
                                        if isinstance(EQTest[message.channel.name][8], PlaceHolder):
                                            EQTest[message.channel.name].pop(8)
                                            EQTest[message.channel.name][8] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][9], PlaceHolder):
                                            EQTest[message.channel.name].pop(9)
                                            EQTest[message.channel.name][9] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][10], PlaceHolder):
                                            EQTest[message.channel.name].pop(10)
                                            EQTest[message.channel.name][10] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][11], PlaceHolder):
                                            EQTest[message.channel.name].pop(11)
                                            EQTest[message.channel.name][11] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(index)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} from the reserves to the MPA list.```'.format(message.author.name))
                                            appended = True
                                            break
                                else:
                                    if isinstance(EQTest[message.channel.name][0], PlaceHolder):
                                        EQTest[message.channel.name].pop(0)
                                        EQTest[message.channel.name].insert(0, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```css\n{} farted. #blamebob2018```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][1], PlaceHolder):
                                        EQTest[message.channel.name].pop(1)
                                        EQTest[message.channel.name].insert(1, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][2], PlaceHolder):
                                        EQTest[message.channel.name].pop(2)
                                        EQTest[message.channel.name].insert(2, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][3], PlaceHolder):
                                        EQTest[message.channel.name].pop(3)
                                        EQTest[message.channel.name].insert(3, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][4], PlaceHolder):
                                        EQTest[message.channel.name].pop(4)
                                        EQTest[message.channel.name].insert(4, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][5], PlaceHolder):
                                        EQTest[message.channel.name].pop(5)
                                        EQTest[message.channel.name].insert(5, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][6], PlaceHolder):
                                        EQTest[message.channel.name].pop(6)
                                        EQTest[message.channel.name].insert(6, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    elif isinstance(EQTest[message.channel.name][7], PlaceHolder):
                                        EQTest[message.channel.name].pop(7)
                                        EQTest[message.channel.name].insert(7, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                        participantCount[message.channel.name] += 1
                                        await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                        appended = True
                                        break
                                    if eightMan[message.channel.name] == False:
                                        if isinstance(EQTest[message.channel.name][8], PlaceHolder):
                                            EQTest[message.channel.name].pop(8)
                                            EQTest[message.channel.name].insert(8, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][9], PlaceHolder):
                                            EQTest[message.channel.name].pop(9)
                                            EQTest[message.channel.name].insert(9, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][10], PlaceHolder):
                                            EQTest[message.channel.name].pop(10)
                                            EQTest[message.channel.name].insert(10, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(message.author.name))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][11], PlaceHolder):
                                            EQTest[message.channel.name].pop(11)
                                            EQTest[message.channel.name].insert(11, teamName + ' ' + serverName + ' ' + classRole + ' ' + message.author.name)
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
            if message.author.top_role.permissions.manage_emojis or message.author.id == '153273725666590720' or message.author.top_role.permissions.administrator:
                userstr = ''
                serverName = '<:manual:408866045156261890>'
                teamName = teamList[7]
                classRole = ''
                if message.channel.name == 'mpa-crossserver':
                    if message.channel.name in EQTest:
                        userstr = message.content
                        userstr = userstr.replace("^add ", "")
                        if userstr == "":
                            await generateList(message, "```fix\nYou can't add nobody. Are you drunk?```")
                            appended = True
                        else:
                            splitstr = userstr.split()
                            if len(splitstr) == 2:
                                if splitstr[1].lower() == 'hu' or splitstr[1].lower() == 'hunter':
                                    classRole += ' ' + classes[0]
                                elif splitstr[1].lower() == 'fi' or splitstr[1].lower() == 'fighter':
                                    classRole += ' ' + classes[1]
                                elif splitstr[1].lower() == 'ra' or splitstr[1].lower() == 'ranger':
                                    classRole += ' ' + classes[2]
                                elif splitstr[1].lower() == 'gu' or splitstr[1].lower() == 'gunner':
                                    classRole += ' ' + classes[3]
                                elif splitstr[1].lower() == 'fo' or splitstr[1].lower() == 'force':
                                    classRole += ' ' + classes[4]
                                elif splitstr[1].lower() == 'te' or splitstr[1].lower() == 'techer':
                                    classRole += ' ' + classes[5]
                                elif splitstr[1].lower() == 'bo' or splitstr[1].lower() == 'bouncer':
                                    classRole += ' ' + classes[6]
                                elif splitstr[1].lower() == 'br' or splitstr[1].lower() == 'braver':
                                    classRole += ' ' + classes[7]
                                elif splitstr[1].lower() == 'su' or splitstr[1].lower() == 'summoner':
                                    classRole += ' ' + classes[8]
                                elif splitstr[1].lower() == 'hr' or splitstr[1].lower() == 'hero':
                                    classRole += ' ' + classes[9]
                            else:
                                classRole += ' ' + classes[10]
                            for word in EQTest[message.channel.name]:
                                if isinstance(word, PlaceHolder):
                                    if not(splitstr[0] in EQTest[message.channel.name]):
                                        if isinstance(EQTest[message.channel.name][0], PlaceHolder):
                                            EQTest[message.channel.name].pop(0)
                                            EQTest[message.channel.name].insert(0, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][1], PlaceHolder):
                                            EQTest[message.channel.name].pop(1)
                                            EQTest[message.channel.name].insert(1, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][2], PlaceHolder):
                                            EQTest[message.channel.name].pop(2)
                                            EQTest[message.channel.name].insert(2, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][3], PlaceHolder):
                                            EQTest[message.channel.name].pop(3)
                                            EQTest[message.channel.name].insert(3, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][4], PlaceHolder):
                                            EQTest[message.channel.name].pop(4)
                                            EQTest[message.channel.name].insert(4, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][5], PlaceHolder):
                                            EQTest[message.channel.name].pop(5)
                                            EQTest[message.channel.name].insert(5, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][6], PlaceHolder):
                                            EQTest[message.channel.name].pop(6)
                                            EQTest[message.channel.name].insert(6, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break
                                        elif isinstance(EQTest[message.channel.name][7], PlaceHolder):
                                            EQTest[message.channel.name].pop(7)
                                            EQTest[message.channel.name].insert(7, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                            appended = True
                                            break 
                                        if eightMan[message.channel.name] == False:
                                            if isinstance(EQTest[message.channel.name][8], PlaceHolder):
                                                EQTest[message.channel.name].pop(8)
                                                EQTest[message.channel.name].insert(8, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                                appended = True
                                                break
                                            elif isinstance(EQTest[message.channel.name][9], PlaceHolder):
                                                EQTest[message.channel.name].pop(9)
                                                EQTest[message.channel.name].insert(9, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                                appended = True
                                                break
                                            elif isinstance(EQTest[message.channel.name][10], PlaceHolder):
                                                EQTest[message.channel.name].pop(10)
                                                EQTest[message.channel.name].insert(10, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
                                                appended = True
                                                break
                                            elif isinstance(EQTest[message.channel.name][11], PlaceHolder):
                                                EQTest[message.channel.name].pop(11)
                                                EQTest[message.channel.name].insert(11, teamName + ' ' + serverName + ' ' + classRole + ' ' + splitstr[0])
                                                participantCount[message.channel.name] += 1
                                                await generateList(message, '```diff\n+ Added {} to the MPA list```'.format(splitstr[0]))
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
            classRole = classes[10]
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
                                EQTest[message.channel.name][index] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(0)
                                tobenamed = EQTest[message.channel.name][index].split()
                                toBeNamed2 = tobenamed[3]
                                participantCount[message.channel.name] += 1
                                await generateList(message, '```diff\n- Removed {} from the MPA list and added {}```'.format(message.author.name, toBeNamed2))
                            inMPA = True
                            return
                    if inMPA == False:
                        for index, item in enumerate(SubDict[message.channel.name]):
                            if message.author.name in item:
                                SubDict[message.channel.name].pop(index)
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
            classRole = classes[10]
            if message.author.top_role.permissions.manage_emojis or message.author.id == '153273725666590720' or message.author.top_role.permissions.administrator:
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
                                        toBeRemovedName = toBeRemoved.split()
                                        toBeRemovedName2 = toBeRemovedName[3]
                                        await generateList(message, '```diff\n- Removed {} from the MPA list```'.format(toBeRemovedName2))
                                        if len(SubDict[message.channel.name]) > 0:
                                            EQTest[message.channel.name][index] = teamName + ' ' + serverName + ' ' + classRole + ' ' + SubDict[message.channel.name].pop(0)
                                            tobenamed = EQTest[message.channel.name][index].split()
                                            toBeNamed2 = tobenamed[3]
                                            participantCount[message.channel.name] += 1
                                            await generateList(message, '```diff\n- Removed {} from the MPA list and added {}```'.format(toBeRemovedName2, toBeNamed2))
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
        # Allows the player to change their class without altering their position in the MPA list.
        elif message.content.lower().startswith('^changeclass'):
            inMPA = False
            if message.channel.name.startswith('mpa') or message.channel.id == '206673616060940288' or message.author.top_role.permissions.administrator:
                if message.channel.name in EQTest:
                    userstr = message.content
                    userstr = userstr.replace("^changeclass", "")
                    userstr = userstr.replace(" ", "")
                    await client.delete_message(message)
                    if userstr == 'hu' or userstr == 'hunter':
                        newRole = classes[0]
                        newRoleName = 'Hunter'
                    elif userstr == 'fi' or userstr == 'fighter':
                        newRole = classes[1]
                        newRoleName = 'Fighter'
                    elif userstr == 'ra' or userstr == 'ranger':
                        newRole = classes[2]
                        newRoleName = 'Ranger'
                    elif userstr == 'gu' or userstr == 'gunner':
                        newRole = classes[3]
                        newRoleName = 'Gunner'
                    elif userstr == 'fo' or userstr == 'force':
                        newRole = classes[4]
                        newRoleName = 'Force'
                    elif userstr == 'te' or userstr == 'techer':
                        newRole = classes[5]
                        newRoleName = 'Techer'
                    elif userstr == 'bo' or userstr == 'bouncer':
                        newRole = classes[6]
                        newRoleName = 'Bouncer'
                    elif userstr == 'br' or userstr == 'braver':
                        newRole = classes[7]
                        newRoleName = 'Braver'
                    elif userstr == 'su' or userstr == 'summoner':
                        newRole = classes[8]
                        newRoleName = 'Summoner'
                    elif userstr == 'hr' or userstr == 'hero':
                        newRole = classes[9]
                        newRoleName = 'Hero'
                    else:
                        newRole = classes[10]
                        newRoleName = 'None'
                    if message.server.id == '189900848862724096':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '189914908328984576':
                                teamName = 'MoonlightSonata'
                                break
                            elif message.author.roles[index].id == '217335164987113472':
                                teamName = '桜花'
                                break                                
                            elif message.author.roles[index].id == '201230397596631040':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '323370572937560064':
                                teamName = '秋冬'
                                break                            
                            elif message.author.roles[index].id == '405607531843551244':
                                teamName = 'NightWatcher'
                                break
                            elif message.author.roles[index].id == '406164933294948363':
                                teamName = 'EtherealMelody'
                                break
                            elif message.author.roles[index].id == '407778610049449986':
                                teamName = 'SWEETxTOXIC'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'Alliance'
                    elif message.server.id == '153346891109761024':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '154465245488742400':
                                teamName = '桜花'
                                break
                            elif message.author.roles[index].id == '308890131648086017':
                                teamName = '桜花'
                                break
                            elif message.author.roles[index].id == '341220141222330368':
                                teamName = '桜花'
                                break
                            elif message.author.roles[index].id == '224757670823985152':
                                teamName = 'Not桜花'
                                break
                            else:
                                teamName = 'None'
                        serverName = '桜花'
                    elif message.server.id == '159184581830901761':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '191162764033523712':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '254207687242285066':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '215683325950427146':
                                teamName = 'Ishana'
                                break
                            elif message.author.roles[index].id == '224757670823985152':
                                teamName = 'NotIshana'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'Ishana'
                    elif message.server.id == '270766856984461312':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '290149383679246336':
                                teamName = 'NightWatcher'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'NightWatcher'
                    elif message.server.id == '196583395550167040':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '311141836976816129':
                                teamName = 'EtherealMelody'
                                break
                            elif message.author.roles[index].id == '198474022483263488':
                                teamName = 'EtherealMelody'
                                break
                            elif message.author.roles[index].id == '198474801461985280':
                                teamName = 'EtherealMelody'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'EtherealMelody'
                    elif message.server.id == '383153236909096961':
                        for index in range(len(message.author.roles)):
                            if message.author.roles[index].id == '409223101302439947':
                                teamName = 'NightWatchers'
                                break
                            elif message.author.roles[index].id == '409225525811216384':
                                teamName = 'NightWatchers'
                                break
                            elif message.author.roles[index].id == '409224931004645387':
                                teamName = 'NightWatchers'
                                break
                            else:
                                teamName = 'None'
                        serverName = 'NightWatchers'
                    else:
                        teamName = 'Unaffiliated'
                        serverName = 'Somewhere'
                    for index, item in enumerate(EQTest[message.channel.name]):
                        if (type(EQTest[message.channel.name][index]) is PlaceHolder):
                            pass
                        elif message.author.name in item:
                            EQTest[message.channel.name].pop(index)
                            EQTest[message.channel.name].insert(index, teamName + ' ' + serverName + ' ' + newRole + ' ' + message.author.name)
                            await generateList(message, '```diff\n+ Changed {}\'s class to '.format(message.author.name) + newRoleName + '```')
                            inMPA = True
                            return
                    if inMPA == False:
                        await generateList(message, '```fix\nYou are not in the MPA!```')
        elif message.content.lower().startswith('^broadcast'):
            if message.channel.name.startswith('mpa-crossserver') or message.channel.id == '322466466479734784':
                if message.author.top_role.permissions.manage_emojis or message.author.id == '153273725666590720' or message.author.top_role.permissions.administrator:
                    userstr = message.content
                    if message.content.startswith('^Broadcast'):
                        userstr = userstr.replace("^Broadcast", "")
                    else:
                        userstr = userstr.replace("^broadcast", "")
                    await client.send_message(client.get_channel('326883995641970689'), '{}: '.format(message.author.name + '#' + str(message.author.discriminator)) + userstr)
                    await client.send_message(client.get_channel('326875381477146624'), '{}: '.format(message.author.name + '#' + str(message.author.discriminator)) + userstr)
                    await client.send_message(client.get_channel('331388355289808897'), '{}: '.format(message.author.name + '#' + str(message.author.discriminator)) + userstr)
                    await client.send_message(client.get_channel('409233586735022080'), '{}: '.format(message.author.name + '#' + str(message.author.discriminator)) + userstr)
                    await client.send_message(client.get_channel('408379606161424394'), '{}: '.format(message.author.name + '#' + str(message.author.discriminator)) + userstr)
                    await client.send_message(client.get_channel('322466466479734784'), '```\n' + '{}'.format(message.author.name + '#' + str(message.author.discriminator)) + ' broadcasted: {}'.format(userstr) + '\n```')
            await client.delete_message(message)
            

@client.event
async def on_ready():
    connectedServers = 0
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print ('Logged in to servers:')
    try:
        for item in client.servers:
            print (item)
            connectedServers += 1
    except:
        print ('Error fetching server list :( Restarting...')
        python = sys.executable
        os.execl(python, python, * sys.argv)
    end = time.time()
    loadupTime = (end - start)
    await client.send_message(client.get_channel('322466466479734784'), 'Toonk has {}'.format(client.get_server('226835458552758275').roles[23].mention) + '\nStartup time: ' + time.strftime('%H hours, %M minutes, %S seconds', time.gmtime(loadupTime)) + '\nConnected to **' + str(connectedServers) + '** servers' + '\nLast Restarted: ' + lastRestart)
    print ('Toonk is now ready\nFinished loadup in ' + time.strftime('%H hours, %M minutes, %S seconds', time.gmtime(loadupTime)))
    print('------')
    await client.change_presence(game=discord.Game(name='more tonk things'), status=discord.Status.online)
@client.event
async def on_server_join(server):
    await client.send_message(client.get_channel('322466466479734784'), '```diff\n+ Joined {} ```'.format(server.name) + '(ID: {})'.format(server.id))
@client.event
async def on_server_remove(server):
    await client.send_message(client.get_channel('322466466479734784'), '```diff\n- Left {} ```'.format(server.name) + '(ID: {})'.format(server.id))
@client.event
async def on_resumed():
    connectedServers = 0
    print ('Toonk has resumed from a disconnect.')
    for item in client.servers:
        connectedServers += 1
    await client.send_message(client.get_channel('322466466479734784'), 'Toonk has {}'.format(client.get_server('226835458552758275').roles[29].mention) + '\nConnected to **' + str(connectedServers) + '** servers')


client.run('')