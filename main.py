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
CHANNEL_ID =  YOURIDHERE # Replace with your channel ID for auto-updates
API_URL = "https://astroservercheck.joejoetv.de/api/check?url=YOURIPHERE:YOURPORTHERE"

# Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Variable to store the message to edit
status_message = None

async def fetch_server_status():
    """Fetches server status from API"""
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

def create_status_embed(data):
    """Creates a Discord embed with server information"""
    embed = discord.Embed(
        title="🚀 Astroneer Server Status",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    if isinstance(data, dict) and 'server' in data:
        server = data['server']
        
        # Online status
        network_status = server.get('network', False)
        playfab_status = server.get('playfab', False)
        is_online = network_status and playfab_status
        
        status_emoji = "🟢" if is_online else "🔴"
        status_text = "Online" if is_online else "Offline"
        
        embed.add_field(
            name=f"{status_emoji} Status",
            value=status_text,
            inline=True
        )
        
        # Players
        current_players = server.get('onlinePlayers', 0)
        max_players = server.get('maxPlayers', 8)
        
        player_emoji = "👥"
        if current_players == 0:
            player_emoji = "💤"
        elif current_players >= max_players * 0.75:
            player_emoji = "🔥"
        
        embed.add_field(
            name=f"{player_emoji} Players",
            value=f"{current_players}/{max_players}",
            inline=True
        )
        
        # Server version
        version = server.get('version', 'Unknown')
        up_to_date = server.get('upToDate', False)
        version_status = "✅" if up_to_date else "⚠️"
        
        embed.add_field(
            name="📋 Version",
            value=f"{version_status} {version}",
            inline=True
        )
        
        # Server name
        server_name = server.get('serverName', 'Astroneer Server')
        embed.add_field(
            name="🏷️ Server Name",
            value=server_name,
            inline=False
        )
        
        # Category
        category = server.get('fullCategory', 'Unknown')
        embed.add_field(
            name="📂 Category",
            value=category,
            inline=True
        )
        
        # Password protected
        requires_password = server.get('requiresPassword', False)
        password_emoji = "🔒" if requires_password else "🔓"
        password_text = "Protected" if requires_password else "Open"
        
        embed.add_field(
            name=f"{password_emoji} Access",
            value=password_text,
            inline=True
        )
        
        # Runtime (uptime)
        runtime = server.get('runTime', 0)
        hours = runtime // 3600
        minutes = (runtime % 3600) // 60
        
        embed.add_field(
            name="⏱️ Uptime",
            value=f"{hours}h {minutes}m",
            inline=True
        )
        
        # Server URL
        server_url = server.get('url', 'N/A')
        embed.add_field(
            name="🌐 Server Address",
            value=f"`{server_url}`",
            inline=False
        )
        
        # Global stats if available
        if 'stats' in data:
            stats = data['stats']
            total_stats = stats.get('total', {})
            
            stats_text = (
                f"**Global Network Stats:**\n"
                f"• Total Servers: {total_stats.get('serverCount', 'N/A')}\n"
                f"• Total Players: {total_stats.get('playerCount', 'N/A')}\n"
                f"• Latest Version: {stats.get('latestVersion', 'N/A')}"
            )
            
            embed.add_field(
                name="📊 Network Statistics",
                value=stats_text,
                inline=False
            )
    else:
        embed.description = "❌ Unable to retrieve server information"
        embed.color = discord.Color.red()
    
    embed.set_footer(text="AstroLauncher Status Bot • Made with ❤️ for the Astroneer community ")
    return embed

@bot.event
async def on_ready():
    """Event triggered when the bot is ready"""
    print(f'{bot.user} is connected and ready!')
    print(f'Bot ID: {bot.user.id}')
    print('---')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
    
    # Start automatic status updates
    update_status.start()
    print("✅ Automatic status updates started (every 1 minute)")

@bot.tree.command(name="ask", description="Display the current Astroneer server status")
async def ask_command(interaction: discord.Interaction):
    """Command /ask to display server status"""
    await interaction.response.defer(thinking=True)
    
    data, error = await fetch_server_status()
    
    if error:
        await interaction.followup.send(f"❌ Error: {error}")
        return
    
    embed = create_status_embed(data)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="server", description="Display detailed server information")
async def server_command(interaction: discord.Interaction):
    """Alternative command to display server status"""
    await interaction.response.defer(thinking=True)
    
    data, error = await fetch_server_status()
    
    if error:
        await interaction.followup.send(f"❌ Error: {error}")
        return
    
    embed = create_status_embed(data)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="stats", description="Display global Astroneer network statistics")
async def stats_command(interaction: discord.Interaction):
    """Command to display global network stats"""
    await interaction.response.defer(thinking=True)
    
    data, error = await fetch_server_status()
    
    if error:
        await interaction.followup.send(f"❌ Error: {error}")
        return
    
    if 'stats' in data:
        stats = data['stats']
        total = stats.get('total', {})
        
        embed = discord.Embed(
            title="📊 Global Astroneer Network Statistics",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🌍 Total Servers",
            value=f"{total.get('serverCount', 'N/A')}",
            inline=True
        )
        
        embed.add_field(
            name="👥 Total Players",
            value=f"{total.get('playerCount', 'N/A')}",
            inline=True
        )
        
        embed.add_field(
            name="✅ Up-to-date Servers",
            value=f"{total.get('upToDate', 'N/A')}",
            inline=True
        )
        
        embed.add_field(
            name="🔒 Password Protected",
            value=f"{total.get('requiresPassword', 'N/A')}",
            inline=True
        )
        
        embed.add_field(
            name="💤 Empty Servers",
            value=f"{total.get('emptyServers', 'N/A')}",
            inline=True
        )
        
        embed.add_field(
            name="🌐 Unique IPs",
            value=f"{total.get('uniqueIPs', 'N/A')}",
            inline=True
        )
        
        embed.add_field(
            name="📋 Latest Version",
            value=f"{stats.get('latestVersion', 'N/A')}",
            inline=False
        )
        
        embed.set_footer(text="AstroLauncher Network Stats")
        
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("❌ Unable to retrieve global statistics")

@bot.tree.command(name="start_monitor", description="Start automatic status monitoring in this channel")
async def start_monitor_command(interaction: discord.Interaction):
    """Command to start monitoring in the current channel"""
    global status_message, CHANNEL_ID
    
    await interaction.response.defer(thinking=True)
    
    CHANNEL_ID = interaction.channel_id
    
    data, error = await fetch_server_status()
    
    if error:
        await interaction.followup.send(f"❌ Error: {error}")
        return
    
    embed = create_status_embed(data)
    
    # Send initial message
    msg = await interaction.followup.send(embed=embed)
    status_message = msg
    
    # Restart the update task
    if not update_status.is_running():
        update_status.start()
    
    await interaction.channel.send("✅ Automatic monitoring started in this channel! Updates every minute.")

@tasks.loop(minutes=1)
async def update_status():
    """Automatically update status every 1 minute by editing the last message"""
    global status_message
    
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("⚠️ Channel not found for auto-updates")
        return
    
    data, error = await fetch_server_status()
    
    if error:
        print(f"❌ Error during automatic update: {error}")
        return
    
    embed = create_status_embed(data)
    
    try:
        if status_message is None:
            # If no message exists, send a new one
            status_message = await channel.send(embed=embed)
            print(f"✅ Initial status message sent to channel {CHANNEL_ID}")
        else:
            # Try to edit the existing message
            try:
                await status_message.edit(embed=embed)
                print(f"✅ Status message updated in channel {CHANNEL_ID}")
            except discord.NotFound:
                # If the message was deleted, send a new one
                print("⚠️ Previous message was deleted, sending a new one")
                status_message = await channel.send(embed=embed)
            except discord.Forbidden:
                print("❌ Bot doesn't have permission to edit messages")
            except Exception as e:
                print(f"❌ Error editing message: {e}")
                # Try to send a new message if editing fails
                status_message = await channel.send(embed=embed)
    except Exception as e:
        print(f"❌ Error sending/editing update: {e}")

@update_status.before_loop
async def before_update_status():
    """Wait for the bot to be ready before starting the loop"""
    await bot.wait_until_ready()
    print("⏳ Waiting before starting automatic updates...")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Error: {error}")

# Run the bot
if __name__ == "__main__":
    print("🚀 Starting Astroneer Status Bot...")
    print("---")
    bot.run(DISCORD_TOKEN)
