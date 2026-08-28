import os
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

# Fixed: Removed privileged message content intent to prevent startup errors
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

# Store farm states for usernames keyed by lowercase username
farm_states = {}


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user} (Synced {len(synced)} commands)")
    except Exception as e:
        print(e)


@bot.tree.command(name="script", description="Get the modded Roblox script to copy on PC or mobile.")
async def get_script(interaction: discord.Interaction):
    await interaction.response.defer()
    
    # Fetch the script live from your URL
    async with aiohttp.ClientSession() as session:
        async with session.get("https://awh.filho.wtf/full.lua") as resp:
            if resp.status != 200:
                await interaction.followup.send("Failed to fetch the script from the URL.", ephemeral=True)
                return
            roblox_script = await resp.text()

    # Send a text file for mobile users
    file_bytes = discord.File(
        fp=__import__("io").BytesIO(roblox_script.encode("utf-8")),
        filename="script.lua",
    )

    embed = discord.Embed(
        title="⚡ AWhub Script",
        description=(
            "Here is your script! PC users can copy from the code box below, "
            "and mobile users can download the attached file."
        ),
        color=0x2B2D31,
    )

    await interaction.followup.send(embed=embed, file=file_bytes)

    # Chunk the script for easy in-chat copying
    chunks = [roblox_script[i : i + 1900] for i in range(0, len(roblox_script), 1900)]
    for chunk in chunks:
        await interaction.followup.send(f"```lua\n{chunk}\n```", ephemeral=True)


@bot.tree.command(
    name="farm", description="Start or stop the farm for a specific username."
)
@app_commands.describe(
    username="Your Roblox username",
    action="Choose whether to start or stop the farm",
)
@app_commands.choices(
    action=[
        app_commands.Choice(name="Start", value="start"),
        app_commands.Choice(name="Stop", value="stop"),
    ]
)
async def farm_control(
    interaction: discord.Interaction, username: str, action: app_commands.Choice[str]
):
    key = username.strip().lower()
    farm_states[key] = action.value == "start"

    status_text = "🟢 Started" if action.value == "start" else "🔴 Stopped"

    embed = discord.Embed(
        title="Farm Control Panel",
        description=(
            f"Successfully updated farm status for user **{username}**."
        ),
        color=0x00D26A if action.value == "start" else 0xED4245,
    )
    embed.add_field(name="Target Username", value=f"`{username}`", inline=True)
    embed.add_field(name="New Status", value=status_text, inline=True)

    await interaction.response.send_message(embed=embed, ephemeral=False)


# Run the bot using the token environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print(
        "Error: DISCORD_TOKEN environment variable not set in Railway configuration!"
    )
