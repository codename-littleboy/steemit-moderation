# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import platform
import datetime
from steem import Steem
from steem.post import Post
from discord.ext.commands import Bot
from discord.ext import commands

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. Commands are strongly discouraged and will require rewriting a lot of code.
client = Bot(description="Placeholder", command_prefix="!", pm_help = True)
s = Steem()

channels_list = ['391089062947061763', # Add channels that correspond to the tags bellow.
'393024926388584484',
'393024964208492554'
]

tag_list = ['steemit', # Add your steemit tags for sorting here.
'steem',
'utopian-io'
]

allowed_channels = ['391079614270668803', # Channels that the bot will monitor, by id.
]

moderating_roles = ['developers', # Keep them lower case.
'moderators'
]

bot_role = 'bots' # Set your bot's role here.

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult Habchy or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('BasicBot created by Habchy#1665')
	print('--------')
	print('Code altered to work with STEEM by Vctr#5566')
	print('--------')
	print('Steemit profile: https://steemit.com/@jestemkioskiem')

# This is our event check. For simplicity's sake, everything happens here. You may add your own events, but commands are discouraged.

@client.event
async def on_message(message):
	msg = message
	msgcon = msg.content
	msgaut = '@' + msg.author.name # Setting some variables for Quality of life purposes.
	
	if bot_role not in [y.name.lower() for y in message.author.roles] and message.channel.id in allowed_channels: # Checking if the poster wasn't the bot and if it was in one of the monitored channels.

		if message.content.startswith('https://steemit') or message.content.startswith('steemit'): # The required beggining of a text for it to be considered not spam.			
			smsgcon = msgcon.split('@')[1]
			tmsgcon = msgcon.split('/')[3]
			sp = Post(smsgcon)

			botmsg = str('This post was nominated by **' + str(msgaut) + '** and authored by **@' + str(sp.author) + '**\n\n' + 'Title: ' + str(sp.title) + '\n' + 'Statistics: ' + str(sp.time_elapsed())[:-10] + ' hours old. Payout: ' + str(sp.reward))	

			if sp.time_elapsed() > datetime.timedelta(hours=2) and sp.time_elapsed() < datetime.timedelta(hours=48): # Checking if post is older than 2h and younger than 48h
				tempmsg = await client.send_message(message.channel, botmsg)


				res = await client.wait_for_reaction(['☑'], message=msg) # Waiting for the emote 
				if moderating_roles[0] in [y.name.lower() for y in res.user.roles] or moderating_roles[1] in [y.name.lower() for y in res.user.roles]:
					await client.delete_message(msg)
					await client.delete_message(tempmsg)

					if tmsgcon in tag_list: # Sorting the item into a correct channel
						dest_channel = tag_list.index(tmsgcon)
					else:
						dest_channel = len(tag_list)

					await client.send_message(client.get_channel(channels_list[dest_channel]), content=msgcon + "\n" + botmsg) # Target channel & message for accepted posts.
			
			else:
				tempmsg = await client.send_message(message.channel, 'Your post has to be between 2h and 48h old.')
				await client.delete_message(msg)

		elif message.content.startswith('!ping') and moderating_roles[0] in [y.name.lower() for y in message.author.roles] or moderating_roles[1] in [y.name.lower() for y in message.author.roles]: # Ping to test if bot is responsive
			await client.send_message(message.channel, ':ping_pong: Pong!')

		elif bot_role not in [y.name.lower() for y in message.author.roles]: # Removing the post if it's not a steemit link.
			await client.delete_message(msg)
			await client.send_message(message.channel, content=msgaut + ' Your link has to start with "https://steemit" or "steemit"')
	
client.run('MzkxMjA3NjQxNTIwNzk5NzQ0.DRvvmw.A8zz88yH9gKuTN2HO4QZ-WNMEw8') # <----------- PUT YOUR BOT'S TOKEN HERE!

# Basic Bot was created by Habchy#1665
# Thank you for using this and don't forget to star Habchy's repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# STEEM's functionality was coded by Vctr#5566, or @jestemkioskiem on steem and steem chat. Contact him if you have any questions.