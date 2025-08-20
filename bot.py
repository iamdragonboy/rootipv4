import discord
from discord.ext import commands
import json
import manager
from auth import is_admin

with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def deployipv4(ctx):
    ip, password = manager.deploy_vps(ctx.author.id)
    ssh_info = f"Your IPv4 VPS has been created!"
    try:
        await ctx.author.send(ssh_info)
        await ctx.send("VPS created! SSH details sent to your DM.")
    except discord.Forbidden:
        await ctx.send("Couldn't DM you your SSH info. Please enable DMs from server members.")

@bot.command()
async def start(ctx):
    await ctx.send(manager.start_vps(ctx.author.id))

@bot.command()
async def restart(ctx):
    await ctx.send(manager.restart_vps(ctx.author.id))

@bot.command()
async def list(ctx):
    await ctx.send(manager.list_vps(ctx.author.id))

@bot.command()
async def node(ctx):
    await ctx.send(manager.show_all_node_users())

@bot.command()
async def delvps(ctx):
    if not is_admin(ctx.author.id):
        return await ctx.send("You do not have permission.")
    await ctx.send(manager.delete_vps(ctx.author.id))

@bot.command()
async def nodeadmin(ctx):
    if not is_admin(ctx.author.id):
        return await ctx.send("You do not have permission.")
    await ctx.send(manager.node_admin())

@bot.command()
async def port(ctx, arg=None):
    if arg == "add":
        await ctx.send(manager.add_ports(ctx.author.id))
    elif arg == "http":
        await ctx.send(manager.get_port_urls(ctx.author.id))
    

@bot.command(name="help", description="Shows the help message")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="help", color=0x00ff00)
    embed.add_field(name="/deployipv4", value="Creates a new Instance with Ubuntu 22.04.", inline=False)
    embed.add_field(name="/remove <ssh_command/Name>", value="Removes a server", inline=False)
    embed.add_field(name="/start <ssh_command/Name>", value="Start a server.", inline=False)
    embed.add_field(name="/stop <ssh_command/Name>", value="Stop a server.", inline=False)
    embed.add_field(name="/regen-ssh <ssh_command/Name>", value="Regenerates SSH cred", inline=False)
    embed.add_field(name="/restart <ssh_command/Name>", value="Stop a server.", inline=False)
    embed.add_field(name="/list", value="List all your servers", inline=False)
    embed.add_field(name="/ping", value="Check the bot's latency.", inline=False)
    embed.add_field(name="/node", value="Check The Node Storage Usage.", inline=False)
    embed.add_field(name="/bal", value="Check Your Balance.", inline=False)
    embed.add_field(name="/renew", value="Renew The VPS.", inline=False)
    embed.add_field(name="/earncredit", value="earn the credit.", inline=False)
    embed.add_field(name="/delvps", value="delete vps user.", inline=False)
    embed.add_field(name="/nodeadmin", value="admin nodes.", inline=False)
    await interaction.response.send_message(embed=embed)
    
bot.run(config["DISCORD_TOKEN"])

