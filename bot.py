import discord
from discord.ext import commands
from discord import app_commands
import random
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Get the token from the .env file

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Mapping from die result to Discord keycap emoji
DICE_EMOJI = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟"
}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")

@bot.tree.command(name="roll", description="Rolls dice for Werewolf 20th Anniversary Edition")
async def roll(
    interaction: discord.Interaction,
    pool: int,
    difficulty: int,
    specialty: str = None,
    character: str = None,
    notes: str = None,
    willpower: bool = False
):
    # Validate difficulty input range
    if difficulty < 3 or difficulty > 10:
        await interaction.response.send_message("Difficulty must be between 3 and 10.", ephemeral=True)
        return

    # Roll dice pool
    rolls = [random.randint(1, 10) for _ in range(pool)]
    rolls_sorted = sorted(rolls, reverse=True)  # Sort descending for better readability

    successes = 0
    ones = 0
    formatted_rolls = []

    # Count successes and format dice output
    for r in rolls_sorted:
        if r == 1:
            ones += 1
            # Failures are wrapped in curly braces
            formatted_rolls.append(f"{{{DICE_EMOJI[r]}}}")
        elif r == 10:
            # Specialty 10s count double successes, but display same as other successes
            if specialty:
                successes += 2
            else:
                successes += 1
            # Success dice wrapped in square brackets
            formatted_rolls.append(f"[{DICE_EMOJI[r]}]")
        elif r >= difficulty:
            successes += 1
            formatted_rolls.append(f"[{DICE_EMOJI[r]}]")  # Success dice in brackets
        else:
            formatted_rolls.append(DICE_EMOJI[r])  # Neutral dice without brackets

    # Willpower adds 1 automatic success
    if willpower:
        successes += 1

    # Calculate net successes after subtracting ones (failures)
    net_successes = max(successes - ones, 0)

    # Raw successes before subtracting ones, needed for botch check
    raw_successes = successes

    # Determine if the roll is a botch
    botch = raw_successes == 0 and ones > 0 and not willpower

    # Compose the result message
    result_message = (
        f"User: {interaction.user.name}    Character: {character or 'N/A'}\n\n"
        f"Rules: Pool {pool} | Diff {difficulty} | WP: {'Yes' if willpower else 'No'} | Specialty: {specialty or 'N/A'}\n\n"
        f"Dice: {', '.join(formatted_rolls)}\n\n"
    )
    if specialty:
        result_message += f"Specialty: {specialty}\n"
    if notes:
        result_message += f"Notes: {notes}\n"
    result_message += f"Outcome: {net_successes} Success{'es' if net_successes != 1 else ''}\n"
    result_message += f"Result: {'Botch' if botch else 'Success' if net_successes > 0 else 'Failure'}"

    # Send the response
    await interaction.response.send_message(result_message)

# Run the bot
bot.run(DISCORD_TOKEN)
