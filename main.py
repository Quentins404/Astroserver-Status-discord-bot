import discord
from discord.ext import commands, tasks
import aiohttp
import json
from datetime import datetime
import ssl
import certifi
from TOKEN import TOKEN

# Configuration
DISCORD_TOKEN = TOKEN
CHANNEL_ID = YOURCHANNELID  # Default channel (can be changed with /start_monitor)
API_URL = "https://astroservercheck.joejoetv.de/api/check?url=IP:PORT"

# Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Variable to store the message to edit
status_message = None


# ===============================
# Fetch API
# ===============================
async def fetch_server_status():
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data, None
                else:
                    return None, f"API error: {response.status}"
    except Exception as e:
        return None, f"Connection error: {str(e)}"


# ===============================
# Create Embed
# ===============================
def create_status_embed(data):
    embed = discord.Embed(
        title="🚀 Astroneer Server Status",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )

    if isinstance(data, dict) and 'server' in data:
        server = data['server']

        network_status = server.get('network', False)
        playfab_status = server.get('playfab', False)
        is_online = network_status and playfab_status

        status_emoji = "🟢" if is_online else "🔴"
        status_text = "Online" if is_online else "Offline"

        embed.add_field(name=f"{status_emoji} Status", value=status_text, inline=True)

        current_players = server.get('onlinePlayers', 0)
        max_players = server.get('maxPlayers', 8)

        player_emoji = "👥"
        if current_players == 0:
            player_emoji = "💤"
        elif current_players >= max_players * 0.75:
            player_emoji = "🔥"

        embed.add_field(name=f"{player_emoji} Players", value=f"{current_players}/{max_players}", inline=True)

        version = server.get('version', 'Unknown')
        up_to_date = server.get('upToDate', False)
        version_status = "✅" if up_to_date else "⚠️"

        embed.add_field(name="📋 Version", value=f"{version_status} {version}", inline=True)

        server_name = server.get('serverName', 'Astroneer Server')
        embed.add_field(name="🏷️ Server Name", value=server_name, inline=False)

        category = server.get('fullCategory', 'Unknown')
        embed.add_field(name="📂 Category", value=category, inline=True)

        requires_password = server.get('requiresPassword', False)
        password_emoji = "🔒" if requires_password else "🔓"
        password_text = "Protected" if requires_password else "Open"

        embed.add_field(name=f"{password_emoji} Access", value=password_text, inline=True)

        runtime = server.get('runTime', 0)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60

        embed.add_field(name="⏱️ Uptime", value=f"{hours}h {minutes}m", inline=True)

        server_url = server.get('url', 'N/A')
        embed.add_field(name="🌐 Server Address", value=f"`{server_url}`", inline=False)

    else:
        embed.description = "❌ Unable to retrieve server information"
        embed.color = discord.Color.red()

    embed.set_footer(text="AstroLauncher Status Bot • Made with ❤️")
    return embed


# ===============================
# Find existing message on reboot
# ===============================
async def find_existing_status_message(channel):
    async for message in channel.history(limit=100):
        if message.author == bot.user and message.embeds:
            embed = message.embeds[0]
            if embed.title == "🚀 Astroneer Server Status":
                print("✅ Existing status message found!")
                return message
    return None


# ===============================
# Bot Ready
# ===============================
@bot.event
async def on_ready():
    global status_message

    print(f'{bot.user} is connected and ready!')
    print(f'Bot ID: {bot.user.id}')
    print('---')

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

    # Try to find previous message
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        status_message = await find_existing_status_message(channel)

    if not update_status.is_running():
        update_status.start()

    print("✅ Automatic status updates started (every 1 minute)")


# ===============================
# Slash Commands
# ===============================
@bot.tree.command(name="ask", description="Display the current Astroneer server status")
async def ask_command(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    data, error = await fetch_server_status()
    if error:
        await interaction.followup.send(f"❌ Error: {error}")
        return

    embed = create_status_embed(data)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="start_monitor", description="Start automatic monitoring in this channel")
async def start_monitor_command(interaction: discord.Interaction):
    global status_message, CHANNEL_ID

    await interaction.response.defer(thinking=True)

    CHANNEL_ID = interaction.channel_id
    channel = bot.get_channel(CHANNEL_ID)

    status_message = await find_existing_status_message(channel)

    data, error = await fetch_server_status()
    if error:
        await interaction.followup.send(f"❌ Error: {error}")
        return

    embed = create_status_embed(data)

    if status_message:
        await status_message.edit(embed=embed)
        await interaction.followup.send("✅ Monitoring resumed and existing message updated.")
    else:
        status_message = await channel.send(embed=embed)
        await interaction.followup.send("✅ Monitoring started and new message created.")

    if not update_status.is_running():
        update_status.start()


# ===============================
# Auto Update Loop
# ===============================
@tasks.loop(minutes=1)
async def update_status():
    global status_message

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("⚠️ Channel not found")
        return

    if status_message is None:
        print("🔍 Searching for existing message...")
        status_message = await find_existing_status_message(channel)

    data, error = await fetch_server_status()
    if error:
        print(f"❌ Error during update: {error}")
        return

    embed = create_status_embed(data)

    try:
        if status_message:
            await status_message.edit(embed=embed)
            print("✅ Status message updated")
        else:
            status_message = await channel.send(embed=embed)
            print("🆕 No message found, created new one")
    except Exception as e:
        print(f"❌ Update error: {e}")


@update_status.before_loop
async def before_update_status():
    await bot.wait_until_ready()


# ===============================
# Error Handling
# ===============================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Error: {error}")


# ===============================
# Run Bot
# ===============================
if __name__ == "__main__":
    print("🚀 Starting Astroneer Status Bot...")
    print("---")
    bot.run(DISCORD_TOKEN)
