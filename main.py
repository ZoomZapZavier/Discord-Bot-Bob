import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import subprocess
import requests
import linecache
import sys
import functions
import asyncio
from discord import app_commands
from googletrans import Translator
from typing import Literal


#memoryFilePath = "BobMemory.txt"

randomWordWebsiteBaseLink = "https://random-word-api.herokuapp.com/"

burnout = r"D:\VSC\Discord bot\BURN.mp3"

load_dotenv()

BFrole = "Bobs Friend"

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="UTF-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.all()

async def sherlock(username: str):

    result = await asyncio.to_thread(subprocess.run, ["sherlock", username, "--no-txt", "--print-found"], capture_output=True, text=True)
    if result.returncode == 0:
        #print(result.stdout)
        return result.stdout
    else:
        print(f"Sherlock error: {result.returncode}")


def getRandomWord():

    
    randomWordWebsite = requests.get(f"{randomWordWebsiteBaseLink}word")

            

    if randomWordWebsite.status_code == 200:

        randomWordWebsiteRaw = randomWordWebsite.json()


        return randomWordWebsiteRaw
    else:
        print(f"The random word website failed with error code: {randomWordWebsite.status_code}")


async def memoryHandler(valueToEdit: str, canEditValues: bool, maxValue: int, userID: int, setValue=None, changeAmmount=None, currentGuildID="Global"):
    memoryFilePath = f"AllBobsMemorys\BobMemory{str(currentGuildID)}.txt"
    with open(file=memoryFilePath, mode="w"):
        ...
    with open(file=memoryFilePath, mode="r") as memoryFileRead:
        print("file has been opened!")
        if setValue is None:
            print("AHHHHHHH")

        found = False
        lineNum = 0

        lines = memoryFileRead.readlines()
        print(len(lines))
        print(lines)
        totalLines = int(len(lines))
            
        
        for x in range(0, totalLines):
            print(x)
            print(lines[x])

            if str(userID) + valueToEdit in lines[x]:
                lineNum = x + 1

                print(f"{userID} is already in memory at line {lineNum}")
                found = True
                            
                lineValue = linecache.getline(filename=memoryFilePath, lineno=lineNum).replace(f"{str(userID)}{valueToEdit} ", "").strip()
                            
                      
                print(f"found it at line {lineNum} and it says {lines[x]} and the Variable of that is {lineValue}")
                linecache.clearcache()
                break
            

        
        if not found:
            with open(file=memoryFilePath, mode="a") as addText:
                addText.write(f"{userID}{valueToEdit} 0\n")
                totalLines += 1
                lineNum = totalLines
                #with open(file=memoryFilePath, mode="r") as SEEKFile:
                #    SEEKFile.seek(0)
                #    linesver = SEEKFile.readlines()
                #    lineNum = len(lines)
                
                print("u dont exist lets fix that")

                print(f"That text was not there so the new text had been added to line {lineNum}")

        lineValue = linecache.getline(filename=memoryFilePath, lineno=lineNum).replace(f"{str(userID)}{valueToEdit} ", "").strip()
        linecache.clearcache()

        print(f"the value of the variable is {int(lineValue)}")
        
        if int(lineValue) + int(changeAmmount) > maxValue:
            print("max value reatched")
            return "Max Uses Reatched!"
        elif setValue is None and changeAmmount is not None:

            print(f"attempting to change line {lineNum} to {str(userID)}{valueToEdit} {int(lineValue) + changeAmmount}")
            print(lineNum - 1)
            if not found:
                lines.append(f"{str(userID)}{valueToEdit} {int(lineValue) + int(changeAmmount)}\n")
            else:

                lines[lineNum - 1] = f"{str(userID)}{valueToEdit} {int(lineValue) + int(changeAmmount)}\n"
            

            with open(file=memoryFilePath, mode="w") as memoryFileWrite:
                for line in lines:
                    memoryFileWrite.write(line)
                return "Done!"
        elif setValue is not None and changeAmmount is None and canEditValues == True:
            line = memoryFileRead.readlines()
            line[lineNum - 1] = setValue

            with open(file=memoryFilePath, mode="w") as memoryFileWrite:
                memoryFileWrite.writelines(line)
                return "Done!"



            
        
async def Translate(message: str, language: str):
    async with Translator() as translator:
        return await translator.translate(text=message, dest=language)

    




bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} IS ALIVE!")
    try:
        guild = discord.Object(id=1291284923214336060)
        await bot.tree.sync(guild=guild)

    except Exception as e:
        print(f"error syncing commands: {e}")

GUILD_ID = discord.Object(id=1291284923214336060)

@bot.tree.command(name="message_user", description="Message a user with bob. (PLS USE WITH CARE I GOT MY PASSWORD RESET CUZ OF THIS COMMAND)", guild=GUILD_ID)
async def MessageUser(interaction: discord.Interaction, user: discord.User, message: str):
    await interaction.response.defer(ephemeral=False)

    await asyncio.sleep(1.23)

    if(interaction.client.user.id != user.id):
        try:
            await user.send(content=f"{message}\n-# I am a bot, and this action was not performed automatically. Please [contact the maker of this bot](<https://www.youtube.com/watch?v=dQw4w9WgXcQ>) if you have any questions or concerns.")
            await interaction.followup.send(f"Sent \"{message}\" to user {user.name}")
            await interaction.response.is_done(True)
        except discord.Forbidden:
            await interaction.followup.send(f"{user.name} has DMs off.")
        except discord.HTTPException as e:
            await interaction.followup.send(f"API Error: {e}")
    else:
        await interaction.followup.send(f"nothing happens...")





# @bot.tree.command(name="translate", description="Translate text into a language", guild=GUILD_ID)
# @app_commands.choices(translate_lanuage[
#     app_commands.Choice(name="English", value="en"),
#     app_commands.Choice(name="Japanese", value="jp"),
#     app_commands.Choice(name="Russian", value="ru"),
#     app_commands.Choice(name="Spanish", value="es"),
#     app_commands.Choice(name="Mandarin", value="zh"),
#     app_commands.Choice(name="air", value="air")])
# async def Translate(interaction: discord.Interaction, text: str, translate_lanuage: app_commands.Choice[str]):
#     interaction.followup.send(f"idk how to translate {translate_lanuage}")

@bot.tree.command(name="translate", description="Translate text into a language", guild=GUILD_ID)
async def Translate(interaction: discord.Interaction, text: str, translation_lanuage: Literal["English", "Japanese", "Russian", "Spanish", "Mandarin", "Italian", "Hindi", "Arabic", "French", "Indonesian", "Bengali", "Portuguese", "Urdu"]):
    await interaction.response.defer(ephemeral=False)

    await interaction.followup.send(f"i donkey kong how to translate {translation_lanuage}")
    await interaction.response.is_done(True)



@bot.tree.command(name="set_auto_translation_channel", description="Make the current channel auto translate your messages.", guild=GUILD_ID)
async def SetChannelTranslate(interaction: discord.Interaction, auto_translate_to: Literal["English", "Japanese", "Russian", "Spanish", "Mandarin", "Italian", "Hindi", "Arabic", "French", "Indonesian", "Bengali", "Portuguese", "Urdu"]):
    await interaction.response.defer(ephemeral=False)

    await interaction.followup.send("uhhhh i donkey kong how..")
    await interaction.response.is_done(True)



@bot.tree.command(name="sherlock", description="Find accounts that have a specific username.", guild=GUILD_ID)
async def SherlockUser(interaction: discord.Interaction, username: str):
    await interaction.response.defer(thinking=True)
    if await memoryHandler(valueToEdit="SherlockUses", canEditValues=False, maxValue=4, userID=interaction.user.id, changeAmmount=1) == "Done!":
        sherlockAnswer = await sherlock(username=username)
        await interaction.followup.send(sherlockAnswer)
        await interaction.response.is_done(True)
    else:
        await interaction.followup.send("You have reatched max uses for that command!")
        await interaction.response.is_done(True)

@bot.tree.command(name="set_memory_value", description="Set a value in bobs memory. (Admin only)", guild=GUILD_ID)
async def SetValue(interaction: discord.Interaction, user: discord.User, value_name: str, value: str):
    await interaction.response.defer()
    if(interaction.guild == None):
        await interaction.followup.send("Error: Cannot set values in DMs.")
        await interaction.response.is_done(True)
        return
    editRole = discord.utils.get(interaction.guild.roles, name="CanEditValues")
    #print(editRole)
    if editRole != None:

        if(interaction.guild.get_role(editRole.id) in interaction.user.roles):
            print("YES U HAVE ROLE")
            #memoryHandler()
            await interaction.followup.send("I can definately not do that but u have the role")
            await interaction.response.is_done(True)
        else:
            if(interaction.user.id == interaction.guild.owner.id):
                interaction.user.add_roles(roles=editRole.id, reason="Automaticly assigned to the owner of the guild.")
            else:
                await interaction.followup.send("You do not have the permissions to execute this command.")
                await interaction.response.is_done(True)
    else:
        print("role does not exist making...")

        editRole = await interaction.guild.create_role(name="CanEditValues", reason="This permission is for bob to know who can set memory values.")
        if(interaction.user.id == interaction.guild.owner.id):
            interaction.user.add_roles(roles=editRole, reason="Automaticly assigned to the owner of the guild.")
        else:
            await interaction.followup.send("You do not have the permissions to execute this command.")
            await interaction.response.is_done(True)



@bot.event
async def on_member_join(person):
    await person.send(f"Welcome {person}")

@bot.event
async def on_message(message):
    if(message.channel.id == 1323224504364961842 and message.author.id != bot.application_id):
        translatedMessage = await Translate(text=message.content, translation_language="ja")
        await message.reply(content=translatedMessage)

    if message.content.lower() == "bob?":
        if random.randint(1, 25) == 7:
            await message.channel.send("https://files.catbox.moe/7ddmlc.png")
        else:
            await message.channel.send("Nothing happens...")
    elif message.author == bot.user:
        return
    elif "idk" in message.content.lower():
        await message.author.send("Invalid Answer.")
        await message.delete()
        if message.content.message_length > 10:
            await message.channel.send(f"{message.author.mention} said ~{message.content}~ btw")
    # elif "!sherlock" in message.content.lower():
    #     if memoryHandler(valueToEdit="SherlockUses", canEditValues=False, maxValue=4, userID=message.author.id, changeAmmount=1) == "Done!":
    #         messageWithNoSherlock = message.content.lower().replace("!sherlock ", "")
    #         print(f"MESSAGE WITH NO SHERLOCK WAS: {messageWithNoSherlock}")
    #         sherlockAnswer = sherlock(messageWithNoSherlock)
    #         print(f"Answer was: {sherlockAnswer}")
    #         await message.channel.send(sherlockAnswer)
    #     else:
    #         await message.channel.send("You have reatched max uses for that command!")

        

    elif "!random" in message.content.lower():
        print("U SAY RANDOM")
        randomWord = getRandomWord()
        print(randomWord)
        randomWordCLEAN = randomWord.pop(0)
        
        
        if randomWordCLEAN == "doors":
            await message.channel.send("IM RUSHIN HERE!")
        elif randomWordCLEAN == "dors":
            await message.channel.send("TEAM DOORS IS RUSHING AWAY AGAIN!!!")
        else:
            await message.channel.send(f"{randomWordCLEAN} happens")

    elif "!burnout" in message.content.lower():
        burnoutBURN = discord.File(burnout)
        await message.channel.send(file=burnoutBURN)
    # elif "!addnum" in message.content.lower():
    #     print("ADDNUM RECIGNISED CONTINUING")
    #     await message.channel.send(memoryHandler(valueToEdit="Test", canEditValues=False, maxValue=4, userID=message.author.id, changeAmmount=1))
    elif "!killzavierswifi" in message.content.lower():
        if memoryHandler(valueToEdit="WifiKills", canEditValues=False, maxValue=2, userID=message.author.id, changeAmmount=1) == "Done!":
            print("oh..")
            functions.killWifi(1)
    elif "!setvalue" in message.content:
        print("Hi")
        print(message.author.id)
        if str(message.author.id) == "1196010537943842946":
            print("hi zavier")
            userValue = message.content.replace("!setvalue ", "")
            print(userValue)
            print(len(userValue))
            print(userValue[0])
            for y in range(0, 25):
                print("hi")
                if isNum(userValue[0]) == True:
                    print("SOUP")
                    userValue.pop(0)
                    print(userValue[0])
                else:
                    print(f"{userValue[0]} IS NOT A NUMBER")
                    break
            print(userValue)
            userId = message.content.replace("!setvalue ", "")
            userId.replace(userValue, "")
            setValue = userId
            offset = 0
            for x in range(0, len(userId)):
                if isNum(userId[x - offset]) == True:
                    userId.pop(x)
                    offset += 1
            userId.strip()
            print(userId)
            setValue.replace(userId, "")
            setValue.strip()
            userValue.replace(setValue, "")
            print(f"The value to set is {setValue}")
    elif "hlkw" in message.content.lower():
        await message.channel.send("hlkw")
    elif "!getuserfromid" in message.content.lower():
        userID = message.content.lower().replace("!getuserfromid ", "")
        message = userID
        LookupUser = await bot.fetch_user(userID)
        if(LookupUser):
            await message.channel.send(f"User ID: {LookupUser.id}\nUsername: {LookupUser.name}\nDisplay Name: {LookupUser.display_name}\nAccount Creation Date: {LookupUser.created_at}\nisBot: {LookupUser.bot}\nAvatar: {LookupUser.avatar}\nFlags: {LookupUser.public_flags}\nCollectables: {LookupUser.collectibles}\nPing: {LookupUser.mention}")
        else:
            await message.channel.send("Failed to find user from ID.")
    elif "!killbob" in message.content.lower():
        os._exit(0)


    await bot.process_commands(message)

@bot.command()
async def RandomNumber(ctx):
    await ctx.send(f"Your Number is {random.randint(1,100000000000000000000000000000000000000000000000)} <:Bob:1514493902613254184>")


@bot.command()
async def assignBobsFriend(ctx):
    role = discord.utils.get(ctx.guild.roles, name=BFrole)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been given the role {role}")
    else:
        ctx.channel.send(f"Yea somthings wrong")

@bot.command()
async def removeBobsFriend(ctx):
    role = discord.utils.get(ctx.guild.roles, name=BFrole)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} no longer has the role {role}")
    else:
        ctx.channel.send(f"Yea somthings wrong")


def isNum(char: str):
    if char == "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
        print(f"{char} is a number")
        return True
    else:
        print(f"{char} is not a number")
        return False


bot.run(token, log_handler=handler, log_level=logging.DEBUG)


