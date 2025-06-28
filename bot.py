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

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")

# Slash command setup
@bot.tree.command(name="roll", description="Rolls dice for Werewolf 20th Anniversary Edition")
async def roll(interaction: discord.Interaction,
               pool: int,
               difficulty: int,
               specialty: str = None,
               character: str = None,
               notes: str = None,
               willpower: bool = False):
    # Ensure valid difficulty range
    if difficulty < 3 or difficulty > 10:
        await interaction.response.send_message("Difficulty must be between 3 and 10.", ephemeral=True)
        return

    # Roll the dice
    rolls = [random.randint(1, 10) for _ in range(pool)]
    rolls_sorted = sorted(rolls, reverse=True)  # Sort rolls from greatest to least

    successes = sum(1 for r in rolls if r >= difficulty)
    gross_successes = successes
    gross_failures = rolls.count(1)

    # Specialty rule (10 counts as 2 successes)
    if specialty:
        successes += rolls.count(10)

    # Willpower rule (add 1 success if willpower is used)
    if willpower:
        successes += 1

    # Handle Botch conditions
    net_successes = max(successes - gross_failures, 0)
    botch = gross_successes == 0 and gross_failures > 0 and not willpower

    # Count the number of failures for strikeout handling
    strikeouts = gross_failures

    # Format each die based on the success and failure rules
    formatted_rolls = []

    for roll in rolls_sorted:
        if roll == 1:
            formatted_rolls.append(f"~~{roll}~~")  # Strike out 1's
        elif roll >= difficulty:
            if roll == 10:
                if specialty:
                    if strikeouts > 0:
                        formatted_rolls.append(f"~~**{roll}**~~")
                        strikeouts -= 1
                        # Bonus 10 with Strikeout or normal based on remaining Strikeouts
                        if strikeouts > 0:
                            formatted_rolls.append(f"[~~**{roll}**~~]")
                            strikeouts -= 1
                        else:
                            formatted_rolls.append(f"[**{roll}**]")  # Bonus 10 without Strikeout
                    else:
                        formatted_rolls.append(f"**{roll}**")
                        formatted_rolls.append(f"[**{roll}**]")
                else:
                    if strikeouts > 0:
                        formatted_rolls.append(f"~~**{roll}**~~")
                        strikeouts -= 1
                    else:
                        formatted_rolls.append(f"**{roll}**")  # Only one 10 if not specialty
            else:
                if strikeouts > 0:
                    formatted_rolls.append(f"~~{roll}~~")
                    strikeouts -= 1
                else:
                    formatted_rolls.append(f"{roll}")
        else:
            formatted_rolls.append(f"*{roll}*")

    # Create the result message
    result_message = (
        f"User: {interaction.user.name}    Character: {character or 'N/A'}\n\n"
        f"Rules: Pool {pool} | Diff {difficulty} | WP: {'Yes' if willpower else 'No'} | Specialty: {specialty or 'N/A'}\n\n"
        f"Dice: {', '.join(formatted_rolls)}\n\n"
    )
    if specialty:
        result_message += f"Specialty: {specialty}\n"
    if notes:
        result_message += f"Notes: {notes}\n"
    result_message += f"Outcome: {net_successes} Successes\n"
    result_message += f"Result: {'Botch' if botch else 'Success' if net_successes > 0 else 'Failure'}"

    # Send response
    await interaction.response.send_message(result_message)

# Run bot
bot.run(DISCORD_TOKEN)
