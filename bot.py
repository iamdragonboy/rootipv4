import discord
from discord.ext import commands
import json

from vps_manager import manager
from utils.auth import is_admin

with open("config.json") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="./", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def deployipv4(ctx):
    ip, password = manager.deploy_vps(ctx.author.id)
    ssh_info = f"""Your IPv4 VPS has been created!
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
    else:
        await ctx.send("Usage:\n`./port add` to assign default ports\n`./port http` to get URLs")

bot.run(config["DISCORD_TOKEN"])

