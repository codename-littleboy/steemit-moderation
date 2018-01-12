	# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import datetime
from steem import Steem
from steem.post import Post
from steem.instance import set_shared_steemd_instance
from steem.steemd import Steemd
from discord.ext.commands import Bot
from discord.ext import commands
from coinmarketcap import Market
import os

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. @client.command is strongly discouraged, edit your commands into the command() function instead.
client = Bot(description="Server-Management-Bot", command_prefix='!', pm_help = True)
s = Steem(nodes=["https://api.steemit.com"])
steemd_nodes = [
    'https://api.steemit.com/',
    'https://gtg.steem.house:8090/',
    'https://steemd.steemitstage.com/',
    'https://steemd.steemgigs.org/'
    'https://steemd.steemit.com/',
]
set_shared_steemd_instance(Steemd(nodes=steemd_nodes)) # set backup API nodes
ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
btc_usd = cmc.ticker("bitcoin", limit="3", convert="USD")[0].get("price_usd", "none")

react_dict = {}
cmc = Market() # Coinmarketcap API call.

SERVER_ID = '368472502139093002' # Put Discord server's ID
ROLE_NAME = '' # Put Discord server's granted role name
bot_role = 'marshal' # Set a role for all of your bots here. You need to give them such role on the discord server.

minimum_payment = 1.000 # 1 STEEM

allowed_channels = ['387030201961545728', #community-review
]

moderating_roles = ['developers', # Keep them lower case.
'moderators']

channels_list = ['389762510779187200', #introduceyourself
'389608804972756993', #steemit
'389762038408282112', #bitcoin
'389762302330535946', #cryptocurrency
'389762891823316992', #blog
'389761959014432778', #steem
'389764215537270787', #crypto
'389764282700660737', #health	
'389764314313129984', #science
'389890366427627520', #technology
'389890644551794688', #programming
'389890578499764226', #tutorials
'389764366456586240' #all_other
]

tag_list = ['introduceyourself',
'steemit',
'bitcoin',
'cryptocurrency',
'blog',
'steem',
'crypto',
'health',
'science',
'technology',
'programming',
]

registered_users = {
	
}

#########################
# DEFINE FUNCTIONS HERE #
#########################

 # Used to run any commands. Add your custom commands here, each under a new elif command.startswith(name):.
async def command(msg,command):
	command = str(command)
	command = command[1:]
	if command.startswith('ping'):
		await client.send_message(msg.channel,":ping_pong: Pong!")
	elif command.lower().startswith('register'):
		await client.send_message(msg.author, "<@" + msg.author.id + ">, to register send transaction for " + str(minimum_payment) + " STEEM to @" + BOT_USER_NAME + " with memo: " + msg.author.id)
	
	else:
		command_error = await client.send_message(msg.channel, "Incorrect command.")
		await asyncio.sleep(6)
		await client.delete_message(command_error)

# Deletes posts in channel_list channels older than given hours.
async def del_old_mess(hours): 
	currtime = datetime.datetime.now() - datetime.timedelta(hours=hours)
	chn = []
	for x in client.get_all_channels():
		if x.id in channels_list:
			chn.append(x)
	for x in chn:
		async for y in client.logs_from(x,limit=100,before=currtime):
			await client.delete_message(y)

async def payout(total,sbd,ste):
	total = float(total) * 0.8 # Currator cut, anywhere between 0.85 and 0.75.
	totalsbd = str(total * 0.5 * float(sbd))[:6]
	totalsp = total * 0.5 * float(ste)
	totalsp = str(totalsp * 1/float(ste))[:6] # SBD is always worth 1$ in the steem blockchain, so price of SBD to price of STE is always 1/STE.
	payout = str(float(totalsbd) + float(totalsp))[:6]
	return payout

async def get_info(msg):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	if check_age(p,2,48):
		embed=discord.Embed(color=0xe3b13c)
		embed.add_field(name="Title", value=str(p.title), inline=False)
		embed.add_field(name="Author", value=str("@"+p.author), inline=True)
		embed.add_field(name="Nominator", value=str('<@'+ msg.author.id +'>'), inline=True)
		embed.add_field(name="Age", value=str(p.time_elapsed())[:-10] +" hours", inline=False)
		embed.add_field(name="Payout", value=str(p.reward), inline=True)
		embed.add_field(name="Payout in USD", value=await payout(p.reward,sbd_usd,ste_usd), inline=True)
		embed.set_footer(text="Marshal - a Steem bot by Vctr#5566 (@jestemkioskiem)")
		return embed
	else:
		age_error = await client.send_message(msg.channel, 'Your post has to be between 2h and 48h old.')
		await client.delete_message(msg)
		await asyncio.sleep(6)
		await client.delete_message(age_error)

# Used to authorize posts and sort them into correct channels.
async def authorize_post(msg, user): 
	msg_tag = msg.content.split('/')[3]
	p = Post(msg.content.split('@')[1])

	if check_age(p,2,48):
		await client.delete_message(msg)

		if msg_tag in tag_list: # Sorting the item into a correct channel
			dest_channel = tag_list.index(msg_tag)
		else:
			dest_channel = len(tag_list)

		print(msg)
		embed = await get_info(msg)
		await client.send_message(client.get_channel(channels_list[dest_channel]), content=msg.content)
		await client.send_message(client.get_channel(channels_list[dest_channel]), embed=embed) # Target channel & message for accepted posts.
		await client.send_message(client.get_channel(channels_list[dest_channel]), content="This post was accepted by <@" + user.id + ">" )
			

# Returns true if the post's age is between two dates.
def check_age(post,low,high): 
	if post.time_elapsed() > datetime.timedelta(hours=low) and post.time_elapsed() < datetime.timedelta(hours=high):
		return True
	else:
		return False

# Returns true if message's author has a moderating_roles role.
def is_mod(user): 
	auth_roles = []
	for x in user.roles:
		auth_roles.append(x.name.lower())

	for x in moderating_roles:
		if x in auth_roles:
			return True
			break
		else:
			return False

async def check_for_payments():
	await client.wait_until_ready()
	role = discord.utils.get(client.get_server(SERVER_ID).roles, name=ROLE_NAME)
	
	while not client.is_closed:
		transfers = account.history_reverse(filter_by='transfer')
		now = datetime.datetime.now() - datetime.timedelta(days=7) # check only last 7 days
		
		for t in transfers:
				
			#print('Received from: ' + t['from'] + ' +' + t['amount'] + '. Memo: ' + t['memo'] + ' at ' + t['timestamp'])
			
			if now > datetime.datetime.strptime(t['timestamp'], "%Y-%m-%dT%H:%M:%S"):
				break
				
			if t['from'] == BOT_USER_NAME: # skip mine transactions
				continue
			
			if not t['memo'].isdigit(): # skip invalid MEMO
				continue
			
			if 'STEEM' in t['amount']: # STEEM payment only?
				payment = float(t['amount'].replace("STEEM", ""))
				if payment >= minimum_payment:
					member = discord.utils.get(client.get_server(SERVER_ID).members, id=t['memo']) # get member by id
					if role in member.roles:
						continue

					registered_users[t['from']] = msg.author.id # Storing registered users in a dictionary for later database functionality.
					f = open("users.txt", "a")
					for x in registered_users:
						f.write(str(x))
						f.write(":")
						f.write(str(a[x]))
						f.write("\n")

					await client.add_roles(member, role) # add role to member
					await client.send_message(member, "<@" + member.id + ">, You have been successfully registered :)")
				
	await asyncio.sleep(60) # check every minute

######################
# DEFINE EVENTS HERE #
######################

@client.event
async def on_ready():
	print('\nInvite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Server-Management-Bot was built by Vctr#5566')
	print('Steemit profile: https://steemit.com/@jestemkioskiem')


# This is our event check. For simplicity's sake, everything happens here. You may add your own events, but commands are discouraged, for that, edit the command() function instead.
@client.event
async def on_message(message):
	ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
	sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
	btc_usd = cmc.ticker("bitcoin", limit="3", convert="USD")[0].get("price_usd", "none")
	await del_old_mess(132)

	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

	elif bot_role not in [y.name.lower() for y in message.author.roles] and message.channel.id in allowed_channels: # Checking if the poster wasn't the bot and if it was in one of the monitored channels.
		if message.content.startswith('https://steemit.com') or message.content.startswith('https://busy.org'):
			embed = await get_info(message)
			botmsg = await client.send_message(message.channel, embed=embed)
			react_dict[message.id] = botmsg.id

		else:
			if not is_mod(message.author):
				await client.delete_message(message)
				link_error = await client.send_message(message.channel, content= '@' + str(message.author) + ' Your link has to start with "https://steemit.com" or "https://busy.org"')
				await asyncio.sleep(6)
				await client.delete_message(link_error)	

@client.event
async def on_reaction_add(reaction, user):
	if is_mod(user):
		if reaction.emoji == '☑':
			await authorize_post(reaction.message, user)
			botmsg = await client.get_message(reaction.message.channel, react_dict[reaction.message.id])
			await client.delete_message(botmsg)

if __name__ == '__main__': # Starting the bot.
	client.run(os.getenv('TOKEN'))