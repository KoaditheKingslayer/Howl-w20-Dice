import discord
from discord.ext import commands
from discord import app_commands
import random
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Get the token from the .env file

DICE_EMOJIS = {
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
    6: ":six:",
    7: ":seven:",
    8: ":eight:",
    9: ":nine:",
    10: ":keycap_ten:",
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands: {[cmd.name for cmd in synced]}")
    print(f"We have logged in as {bot.user}")

@bot.tree.command(name="roll", description="Rolls dice for Werewolf 20th Anniversary Edition")
async def roll(interaction: discord.Interaction,
               pool: int,
               difficulty: int,
               specialty: str = None,
               character: str = None,
               notes: str = None,
               willpower: bool = False):
    if difficulty < 3 or difficulty > 10:
        await interaction.response.send_message("Difficulty must be between 3 and 10.", ephemeral=True)
        return

    rolls = [random.randint(1, 10) for _ in range(pool)]
    rolls_sorted = sorted(rolls, reverse=True)

    successes = 0
    formatted_rolls = []
    ones = 0

    for r in rolls_sorted:
        emoji = DICE_EMOJIS[r]
        if r == 1:
            ones += 1
            formatted_rolls.append(f"{{{emoji}}}")
        elif r == 10:
            if specialty:
                successes += 2
            else:
                successes += 1
            formatted_rolls.append(f"[{emoji}]")
        elif r >= difficulty:
            successes += 1
            formatted_rolls.append(f"[{emoji}]")
        else:
            formatted_rolls.append(emoji)

    if willpower:
        successes += 1
        formatted_rolls.insert(0, "[\U0001F1FC]")  # Regional Indicator Symbol Letter W in brackets

    raw_successes = successes
    net_successes = max(successes - ones, 0)
    botch = raw_successes == 0 and ones > 0 and not willpower

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

    await interaction.response.send_message(result_message)

@bot.tree.command(name="initiative", description="Roll initiative for Werewolf 20th Anniversary Edition")
@app_commands.describe(
    dexterity="Dexterity (0-20)",
    wits="Wits (0-20)",
    sotf="Spirit of the Fray (adds +10)",
    sotf_gnosis="Spirit of the Fray Gnosis (adds +10, requires SotF)",
    character="Character name"
)
async def initiative(
    interaction: discord.Interaction,
    dexterity: app_commands.Range[int, 0, 20],
    wits: app_commands.Range[int, 0, 20],
    sotf: bool = False,
    sotf_gnosis: bool = False,
    character: str = None
):
    roll = random.randint(1, 10)
    bonus = dexterity + wits

    if sotf:
        bonus += 10
        if sotf_gnosis:
            bonus += 10
    else:
        sotf_gnosis = False

    bonus_components = ["Dex", "Wits"]
    if sotf:
        bonus_components.append("SotF")
    if sotf_gnosis:
        bonus_components.append("SotF Gnosis")
    bonus_label = " + ".join(bonus_components)

    total = roll + bonus

    stat_parts = [
        f"Dexterity: {dexterity}",
        f"Wits: {wits}"
    ]
    if sotf:
        stat_parts.append("SotF: Yes")
    if sotf_gnosis:
        stat_parts.append("SotF Gnosis: Yes")
    stat_line = " | ".join(stat_parts)

    message = (
        f"User: {interaction.user.name}    Character: {character or 'N/A'}\n\n"
        f"{stat_line}\n\n"
        f"Roll (d10): {roll}\n"
        f"Bonus ({bonus_label}): {bonus}\n"
        f"**Initiative Total: {total}**"
    )

    await interaction.response.send_message(message)

bot.run(DISCORD_TOKEN)
