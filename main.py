import discord
import asyncio
import discord.ext
from discord.ext import commands
import json


bot = discord.Client()
bot = commands.Bot(command_prefix='!')

onGoing = "⌛"

@bot.event
async def on_ready():
    print ("Our Python Bot Is Online!!")

#opening a goal sheet
@bot.command()
async def goal(ctx):
    with open("goal.json", 'r') as f:
        users = json.load(f)

        #first time using the command
        if str(ctx.author.id) not in users:
            users[str(ctx.author.id)] = {}
            users[str(ctx.author.id)]["goals"] = []


    with open("goal.json", "w") as f:
        json.dump(users, f, indent=4)


#adding goals to goal list
@bot.command()
async def add(ctx, *, usergoal):
    onGoingGoal = onGoing + usergoal
    with open("goal.json", 'r') as f:
        users = json.load(f)
        goalList = users[str(ctx.author.id)]["goals"]
        goalList.append(onGoingGoal)
        users[str(ctx.author.id)]["goals"] = goalList

    with open("goal.json", "w") as f:
        json.dump(users, f, indent=4)

    embed = discord.Embed(title = "📜Adding Your Goal To The List....📜",
                          color = discord.Color.green())
    embed.set_author(name=ctx.author,
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name="You Added: ", value=usergoal, inline=False)
    embed.add_field(name="Check Your Goals: ", value="Enter !mygoals to see all of your goals", inline=False)

    embed.set_footer(text="Made By Shaun")


    await ctx.send(embed=embed)

#return the goals
@bot.command()
async def mygoals(ctx):
    with open("goal.json", 'r') as f:
        users = json.load(f)
        goalList = users[str(ctx.author.id)]["goals"]

        #calculating prograss
        totalgoal = len(goalList)
        if (totalgoal > 0):
            finished = 0
            for goal in goalList:
                if "✅" in goal:
                    finished = finished + 1

            progras = finished / totalgoal
            progras = progras * 100
            progras = int(progras)

            embed = discord.Embed(title='💡Your On Going Goals💡', color = discord.Color.green())
            nameslist = '\n'.join(goalList)
            embed.add_field(name = 'Your Goals: ', value = nameslist, inline=False)
            embed.add_field(name="Your progress: ",  value=f"{progras}%", inline=False)
            embed.set_footer(text="Made By Shaun")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='❌Error❌', color = discord.Color.green())
            embed.add_field(name = 'Empty Goal Sheet: ', value = "Please type !add to add goals first!", inline=False)
            embed.set_footer(text="Made By Shaun")
            await ctx.send(embed = embed)

@bot.command()
async def finish(ctx, index:int):
    with open("goal.json", 'r') as f:
        users = json.load(f)
        goalList = users[str(ctx.author.id)]["goals"]
        finishedGoal = goalList[index-1]
        finishedGoal = '✅' + finishedGoal[1:]
        goalList[index-1] = finishedGoal
        embed = discord.Embed(title='💯Finished A Goal💯', color = discord.Color.green())
        embed.add_field(name="The Goal You Finished: ", value=finishedGoal)
        embed.set_footer(text="Made By Shaun")
        await ctx.send(embed=embed)

        
    with open("goal.json", "w") as f:
        json.dump(users, f, indent=4)

@bot.command()
async def done(ctx):
    with open("goal.json", 'r') as f:
        users = json.load(f)
        goalList = users[str(ctx.author.id)]["goals"]
        goalList.clear()
        
        embed = discord.Embed(title='☑️Finished All Goals ☑️', color = discord.Color.green())
        embed.add_field(name="You Have Cleared Your Goal Sheet!", value="Type !add to add new goals!")
        embed.set_footer(text="Made By Shaun")
        
        await ctx.send(embed = embed)

    with open("goal.json", "w") as f:
        json.dump(users, f, indent=4)



#Your token
bot.run('')