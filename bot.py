import os
import aiohttp
import asyncio
from aiohttp import web
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Stores control states for each username
user_controls = {}

async def handle_status(request):
    username = request.query.get("username", "").strip().lower()
    if not username:
        return web.json_response({"error": "Missing username"}, status=400)
    
    # Default values if user isn't registered yet
    data = user_controls.get(username, {
        "farm": True,
        "serverhop": False,
        "fling": False,
        "reset_murderer": True,
        "reset_sheriff": True,
        "reset_innocent": True
    })
    
    # Copy data and clear one-shot triggers (like serverhop/fling) so they don't loop infinitely
    response_data = data.copy()
    if data.get("serverhop"):
        user_controls[username]["serverhop"] = False
    if data.get("fling"):
        user_controls[username]["fling"] = False
        
    return web.json_response(response_data)

async def web_server():
    app = web.Application()
    app.router.add_get('/get_status', handle_status)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user} (Synced {len(synced)} commands)")
    except Exception as e:
        print(e)

@bot.tree.command(name="script", description="Get the complete execution loadstring and script source.")
async def script_command(interaction: discord.Interaction):
    await interaction.response.defer()
    
    async with aiohttp.ClientSession() as session:
        async with session.get("https://awh.filho.wtf/full.lua") as resp:
            if resp.status != 200:
                await interaction.followup.send("Failed to retrieve script source from remote server.", ephemeral=True)
                return
            script_content = await resp.text()

    file_bytes = discord.File(
        fp=__import__("io").BytesIO(script_content.encode("utf-8")),
        filename="AWhub.lua",
    )

    loadstring_code = 'loadstring(game:HttpGet("https://awh.filho.wtf/full.lua"))()'

    embed = discord.Embed(
        title="AWhub Execution Suite",
        description="Loadstring command and source file ready for deployment.",
        color=0x1E1F22,
    )
    embed.add_field(name="Loadstring", value=f"```lua\n{loadstring_code}\n```", inline=False)
    embed.set_footer(text="Mobile users can download the attached file.")

    await interaction.followup.send(embed=embed, file=file_bytes)

@bot.tree.command(name="farm", description="Toggle the automated farming loop for a user.")
@app_commands.describe(username="Target Roblox username", action="Execution state")
@app_commands.choices(action=[
    app_commands.Choice(name="Enable", value="start"),
    app_commands.Choice(name="Disable", value="stop")
])
async def farm_control(interaction: discord.Interaction, username: str, action: app_commands.Choice[str]):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    user_controls[key]["farm"] = (action.value == "start")

    state_desc = "Operational" if action.value == "start" else "Suspended"
    embed = discord.Embed(title="Configuration Updated", description=f"Auto-farm parameters modified for target: **{username}**", color=0x23A55A if action.value == "start" else 0xF23F43)
    embed.add_field(name="Target User", value=username, inline=True)
    embed.add_field(name="Status", value=state_desc, inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.tree.command(name="serverhop", description="Force an immediate server hop sequence.")
@app_commands.describe(username="Target Roblox username")
async def serverhop_command(interaction: discord.Interaction, username: str):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    user_controls[key]["serverhop"] = True

    embed = discord.Embed(title="Command Dispatched", description=f"Server migration signal queued for **{username}**.", color=0x5865F2)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.tree.command(name="fling", description="Execute target elimination protocol.")
@app_commands.describe(username="Target Roblox username")
async def fling_command(interaction: discord.Interaction, username: str):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    user_controls[key]["fling"] = True

    embed = discord.Embed(title="Command Dispatched", description=f"Fling routine initialized for **{username}**.", color=0xFAA61A)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.tree.command(name="autoreset", description="Configure automatic round resets based on assigned roles.")
@app_commands.describe(username="Target Roblox username", mode="Target role category", state="Configuration setting")
@app_commands.choices(
    mode=[
        app_commands.Choice(name="Murderer", value="murderer"),
        app_commands.Choice(name="Sheriff", value="sheriff"),
        app_commands.Choice(name="Innocent", value="innocent")
    ],
    state=[
        app_commands.Choice(name="Active", value="enable"),
        app_commands.Choice(name="Inactive", value="disable")
    ]
)
async def autoreset_command(interaction: discord.Interaction, username: str, mode: app_commands.Choice[str], state: app_commands.Choice[str]):
    key = username.strip().lower()
    if key not in user_controls:
        user_controls[key] = {}
    
    setting_key = f"reset_{mode.value}"
    is_enabled = (state.value == "enable")
    user_controls[key][setting_key] = is_enabled

    embed = discord.Embed(title="Parameters Updated", description=f"Auto-reset for **{mode.name}** class set to **{state.name.lower()}** on account **{username}**.", color=0xEB459E)
    await interaction.response.send_message(embed=embed, ephemeral=False)

@bot.tree.command(name="status", description="Inspect live telemetry and status flags for a user.")
@app_commands.describe(username="Target Roblox username")
async def status_command(interaction: discord.Interaction, username: str):
    key = username.strip().lower()
    data = user_controls.get(key, {})

    embed = discord.Embed(title=f"Telemetry: {username}", description="Active runtime state flags retrieved from server memory.", color=0x2B2D31)
    embed.add_field(name="Auto-Farm", value="Active" if data.get("farm") else "Idle", inline=True)
    embed.add_field(name="Server Hop", value="Pending" if data.get("serverhop") else "Clear", inline=True)
    embed.add_field(name="Fling Routine", value="Pending" if data.get("fling") else "Clear", inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=False)

async def main():
    await web_server()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set!")
        return
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
