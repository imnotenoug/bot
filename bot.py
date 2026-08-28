import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Control states mapping usernames to their active commands/settings
user_controls = {}

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user} (Synced {len(synced)} commands)")
    except Exception as e:
        print(e)


@bot.tree.command(name="getscript", description="Get the loadstring for the script.")
async def getscript(interaction: discord.Interaction):
    loadstring_text = 'loadstring(game:HttpGet("https://awh.filho.wtf/full.lua"))()'
    
    embed = discord.Embed(
        title="⚡ AWhub Loadstring",
        description=f"Here is your loadstring command:\n```lua\n{loadstring_text}\n```",
        color=0x2B2D31,
    )
    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(name="farm", description="Start or stop the auto-farm for a specific user.")
@app_commands.describe(username="Roblox username", action="Choose start or stop")
@app_commands.choices(action=[
    app_commands.Choice(name="Start", value="start"),
    app_commands.Choice(name="Stop", value="stop")
])
async def farm_control(interaction: discord.Interaction, username: str, action: app_commands.Choice[str]):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    user_controls[key]["farm"] = (action.value == "start")

    status = "🟢 Started" if action.value == "start" else "🔴 Stopped"
    embed = discord.Embed(title="Farm Control", description=f"Farm for **{username}** is now **{status}**.", color=0x00D26A if action.value == "start" else 0xED4245)
    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(name="serverhop", description="Trigger a server hop command for a specific user.")
@app_commands.describe(username="Roblox username")
async def serverhop_command(interaction: discord.Interaction, username: str):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    user_controls[key]["serverhop"] = True

    embed = discord.Embed(title="Server Hop Triggered", description=f"Server hop signal sent for **{username}**.", color=0x3498DB)
    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(name="fling", description="Trigger a player fling action for a specific user.")
@app_commands.describe(username="Roblox username")
async def fling_command(interaction: discord.Interaction, username: str):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    user_controls[key]["fling"] = True

    embed = discord.Embed(title="Fling Triggered", description=f"Fling command queued for **{username}**.", color=0xE67E22)
    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(name="autoreset", description="Toggle auto-reset options for a user.")
@app_commands.describe(username="Roblox username", mode="Select mode", state="Enable or Disable")
@app_commands.choices(
    mode=[
        app_commands.Choice(name="Murderer Reset", value="murderer"),
        app_commands.Choice(name="Sheriff Reset", value="sheriff"),
        app_commands.Choice(name="Innocent Reset", value="innocent")
    ],
    state=[
        app_commands.Choice(name="Enable", value="enable"),
        app_commands.Choice(name="Disable", value="disable")
    ]
)
async def autoreset_command(interaction: discord.Interaction, username: str, mode: app_commands.Choice[str], state: app_commands.Choice[str]):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    
    setting_key = f"reset_{mode.value}"
    is_enabled = (state.value == "enable")
    user_controls[key][setting_key] = is_enabled

    embed = discord.Embed(title="Auto-Reset Config", description=f"**{mode.name}** for **{username}** is now **{state.name}**.", color=0x9B59B6)
    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(name="status", description="Check the current control status flags for a user.")
@app_commands.describe(username="Roblox username")
async def status_command(interaction: discord.Interaction, username: str):
    key = username.strip().lower()
    data = user_controls.get(key, {})

    embed = discord.Embed(title=f"Status for {username}", color=0x2B2D31)
    embed.add_field(name="Farm", value="Active" if data.get("farm") else "Inactive", inline=True)
    embed.add_field(name="Server Hop Flag", value="Pending" if data.get("serverhop") else "Clear", inline=True)
    embed.add_field(name="Fling Flag", value="Pending" if data.get("fling") else "Clear", inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=False)


TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN environment variable not set in Railway configuration!")
