import discord
from discord import app_commands
from discord.ext import commands

# Import your existing main function
from main import main

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user.name}")
    await bot.tree.sync()

# Create the slash command to trigger your script
@bot.tree.command(name="start_rollcall", description="Start monitoring and answering rollcalls")
async def start_rollcall(interaction: discord.Interaction):
    # 1. Critical: Defer response because wait_for_rollcall() takes longer than 3 seconds.
    # ephemeral=True makes the status message visible ONLY to the person who clicked it.
    await interaction.response.defer(ephemeral=True)
    
    try:
        # 2. Safely call your async main function within the running event loop
        await main()
        
        # 3. Notify the user via a followup message when it finishes successfully
        await interaction.followup.send("✅ Rollcall script executed successfully!")
        
    except Exception as e:
        # Catch any connection errors or exceptions and report them securely
        await interaction.followup.send(f"❌ An error occurred: {e}")

bot.run("YOUR_BOT_TOKEN_HERE")


