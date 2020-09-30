import discord
from discord.ext import commands,tasks
import time
import random

bot = commands.Bot(command_prefix='+')

class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None

botdata = BotData()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='reading your texts'))
    print('bot ready!!')
    



    bot.reaction_roles = []

@bot.event
async def on_raw_reaction_add(payload):
    for role , msg,emoji in bot.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    for role , msg,emoji in bot.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            await bot.get_guild(payload.guild_id).get_member(payload.member_id).remove_roles(role)

            
@bot.command()
async def reaction(ctx,role:discord.Role,msg:discord.Message,emoji=None):
    if role !=None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        bot.reaction_roles.append((role,msg,emoji))
    else:
        await ctx.send("Invalid arguments!")

@bot.event
async def on_member_join(member):
    if botdata.welcome_channel !=None:
        await botdata.welcome_channel.send(f"welcome! {member.mention}")
    else:
        print("welcome channel not set")

@bot.event
async def on_member_remove(member):
    if botdata.goodbye_channel != None:
        await botdata.goodbye_channel.send(f"GoodBye! {member.mention}")
    else:
        print("goodbye channel not set")


@bot.command()
async def welcome_channel(ctx,channel_name = None):
    if channel_name !=None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                botdata.welcome_channel = channel
                await ctx.channel.send(f"the welcome channel have been set to : {channel.name}")
                await channel.send("hello! this is the new welcome channel!")
    else:    
        await ctx.channel.send("include the name of the welcome channel")

@bot.command()
async def goodbye_channel(ctx,channel_name = None):
    if channel_name !=None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                botdata.goodbye_channel = channel
                await ctx.channel.send(f"the goodbye channel have been set to : {channel.name}")
                await channel.send("hello! this is the new goodbye channel!")
    else:    
        await ctx.channel.send("include the name of the goodbye channel")

@bot.command()
async def ping(ctx):
    await ctx.send(str(ctx.author.mention)+' your ping is :{0} '.format(round(bot.latency,1)))

@bot.command()
async def hello(ctx):
    channel = ctx.channel
    await channel.send(":wave: hello!! "+ str(ctx.author.mention))

@bot.command()
async def repeat(ctx,*,arg=None):
    if arg ==None:
        await ctx.channel.send("please give an argument to repeat!!")
    else:
        await ctx.channel.send(str(ctx.author.mention)+" "+str(arg))

@bot.command()
async def dm(ctx,user_id=None,*,args=None):
    
    if user_id !=None and args!=None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)
            await ctx.channel.send("'"+args+"'has been sen to: "+target.name)
        except:
            await ctx.channel.send("Couldn't send dms to the user!")
    else:
        await ctx.channel.send(str(ctx.author.mention)+' user id or arguments are absent!')
      
@bot.command(pass_context=True)


async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=int(amount)):
              messages.append(message)

    await channel.delete_messages(messages)
    await ctx.send(amount,'Messaged deleted.')

@bot.event
async def on_member_join(member):
    await bot.change_presence(activity=discord.Game(name='moderators'))



@bot.command()
async def dm_all(ctx,*,args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'"+args+"' sent to : "+member.name)
            except:
                print("'couldn't send'"+args+"'to'"+member.name)
    else:
        await ctx.channel.send("Got it but what should i send them ?")

bot.run('NzMzNjU5MzcxNzUzNDM5MjQy.XxGXiA.C3A3BBZr9QvXtzdCIo_sKvLEHmw')