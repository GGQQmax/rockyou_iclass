import os
import asyncio
import threading
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Import main rollcall runner
from main import main

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Track active rollcall stop_events per user_id: {user_id: threading.Event}
active_rollcalls: dict[int, threading.Event] = {}

class RollcallView(discord.ui.View):
    def __init__(self, stop_event: threading.Event, user_id: int):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.stop_event = stop_event
        self.user_id = user_id

    @discord.ui.button(label="Cancel Rollcall", style=discord.ButtonStyle.danger, emoji="🛑")
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Only allow the user who started the rollcall to cancel it
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ You cannot cancel someone else's rollcall monitor.", ephemeral=True)
            return

        # Signal background thread to stop immediately
        self.stop_event.set()
        button.disabled = True
        button.label = "Cancelling..."
        await interaction.response.edit_message(content="🛑 **Cancelling rollcall monitoring...**", view=self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

@bot.event
async def on_ready():
    print(f"🤖 Bot logged in as {bot.user.name} ({bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

@bot.tree.command(name="start_rollcall", description="Start monitoring and answering rollcalls")
async def start_rollcall(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id in active_rollcalls and not active_rollcalls[user_id].is_set():
        await interaction.response.send_message(
            "⚠️ You already have a rollcall monitor running! Use the **Cancel Rollcall** button or `/cancel_rollcall` to stop it first.",
            ephemeral=True
        )
        return

    # 1. Defer response because wait_for_rollcall() can take up to several minutes
    await interaction.response.defer(ephemeral=True)

    stop_event = threading.Event()
    active_rollcalls[user_id] = stop_event
    view = RollcallView(stop_event, user_id)

    # Send the initial message with the Cancel button
    await interaction.followup.send(
        "🔍 **Monitoring for rollcall...**\nClick the button below at any time to cancel.",
        view=view,
        ephemeral=True
    )

    try:
        # 2. Run synchronous blocking main() in a background thread with cancellation support
        result = await asyncio.to_thread(main, stop_event)

        # 3. Notify the user based on outcome
        if stop_event.is_set() or (result and result.get("cancelled")):
            await interaction.edit_original_response(
                content="🛑 **Rollcall monitoring cancelled.**",
                view=None
            )
        elif result is None:
            await interaction.edit_original_response(
                content="⏱️ **Rollcall polling timed out:** No active rollcall found.",
                view=None
            )
        elif result.get("success"):
            source = result.get("source", "unknown")
            rollcall_id = result.get("rollcall_id", "N/A")
            data = result.get("data", "N/A")
            await interaction.edit_original_response(
                content=(
                    f"✅ **Rollcall answered successfully!**\n"
                    f"- **Type**: `{source}`\n"
                    f"- **Rollcall ID**: `{rollcall_id}`\n"
                    f"- **Result**: `{data}`"
                ),
                view=None
            )
        else:
            await interaction.edit_original_response(
                content=f"⚠️ **Rollcall error:** {result.get('error', 'Unknown error')}",
                view=None
            )

    except Exception as e:
        await interaction.edit_original_response(
            content=f"❌ **An error occurred during rollcall execution:** {e}",
            view=None
        )
    finally:
        # Clean up active tasks tracker
        active_rollcalls.pop(user_id, None)

@bot.tree.command(name="cancel_rollcall", description="Cancel your currently running rollcall monitor")
async def cancel_rollcall(interaction: discord.Interaction):
    user_id = interaction.user.id
    stop_event = active_rollcalls.get(user_id)

    if stop_event and not stop_event.is_set():
        stop_event.set()
        await interaction.response.send_message("🛑 **Cancellation signal sent.** Stopping rollcall monitor...", ephemeral=True)
    else:
        await interaction.response.send_message("ℹ️ You don't have an active rollcall monitor running.", ephemeral=True)

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("DISCORD_TOKEN")
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: DISCORD_BOT_TOKEN is not set.")
        print("Please add DISCORD_BOT_TOKEN=your_token to your .env file or set it as an environment variable.")
        exit(1)
    bot.run(token)
