# 🚀 Astroneer Server Status Discord Bot

A Discord bot that monitors and displays the status of your Astroneer dedicated server using the AstroLauncher API.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🔄 Real-time server status monitoring
- 👥 Player count tracking
- 📊 Global Astroneer network statistics
- ⏱️ Server uptime display
- 🔒 Password protection indicator
- ✅ Version status checking
- 🤖 Slash commands support
- ⚡ Automatic status updates every 5 minutes

## 📋 Requirements

- Python 3.8 or higher
- A Discord Bot Token
- An Astroneer dedicated server (AstroLauncher)

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Astroserver-Status-discord-bot.git
cd Astroserver-Status-discord-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install discord.py aiohttp certifi
```

### 3. macOS SSL Certificate Fix (if needed)

If you're on macOS and encounter SSL errors, run:

```bash
pip install --upgrade certifi
/Applications/Python\ 3.XX/Install\ Certificates.command
```

*(Replace 3.XX with your Python version)*

## ⚙️ Configuration

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the bot token (you'll need this later)
6. Enable these Privileged Gateway Intents:
   - ✅ Message Content Intent

### 2. Invite the Bot to Your Server

1. Go to "OAuth2" → "URL Generator"
2. Select these scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select these bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Messages/View Channels
   - ✅ Use Slash Commands
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 3. Configure the Bot

Open `TOKEN.py` and modify these lines:

```python
# Line 1: Add your Discord bot token
TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
```

Open `main.py` and modify these lines:
```python
# Line 12: Add your channel ID for automatic updates
CHANNEL_ID = 1234567890  # Replace with your Discord channel ID

# Line 13: Add your Astroneer server address
API_URL = "https://astroservercheck.joejoetv.de/api/check?url=YOURSERVERIPHERE:YOURSERVERPORTHERE"

```

#### How to get your Channel ID:

1. Enable Developer Mode in Discord:
   - Settings → Advanced → Developer Mode (ON)
2. Right-click on the channel where you want updates
3. Click "Copy Channel ID"
4. Paste it in the `CHANNEL_ID` variable

#### How to format your server URL:

Replace `YOUR_SERVER_IP:PORT` with your server's address:
```python
# Example:
API_URL = "https://astroservercheck.joejoetv.de/api/check?url=192.168.0.1:7777"
```

## 🚀 Usage

### Start the bot

```bash
python3 main.py
```

You should see:
```
🚀 Starting Astroneer Status Bot...
---
YOUR_BOT_NAME is connected and ready!
Bot ID: 123456789
---
✅ Synced 3 slash command(s)
✅ Automatic status updates started (every 5 minutes)
```

### Available Commands

Once the bot is running, you can use these slash commands in your Discord server:

| Command | Description |
|---------|-------------|
| `/ask` | Display the current server status |
| `/server` | Display detailed server information |
| `/stats` | Display global Astroneer network statistics |

### Example Output

When you use `/ask` or `/server`, the bot will display:

- 🟢/🔴 Server online/offline status
- 👥 Current players / Max players
- 📋 Server version (with up-to-date indicator)
- 🏷️ Server name
- 📂 Server category
- 🔒/🔓 Password protection status
- ⏱️ Server uptime
- 🌐 Server IP address
- 📊 Global network statistics

## 🔄 Automatic Updates

The bot automatically sends server status updates to the configured channel every **5 minutes**.

To change the update interval, modify line 253:

```python
@tasks.loop(minutes=5)  # Change 5 to your desired interval
```

## 📁 Project Structure

```
Astroserver-Status-discord-bot/
│
├── main.py              # Main bot file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── TOKEN.py            # Store your token here
```

## 🐛 Troubleshooting

### Bot doesn't respond to commands

1. Make sure the bot has the required permissions
2. Check if slash commands are synced (bot should log this on startup)
3. Try kicking and re-inviting the bot with the correct permissions

### SSL Certificate Errors (macOS)

```bash
pip install --upgrade certifi
/Applications/Python\ 3.XX/Install\ Certificates.command
```

### "Channel not found" error

- Make sure `CHANNEL_ID` is correct
- Verify the bot has access to that channel
- Right-click the channel → "Copy Channel ID" (Developer Mode must be enabled)

### Bot offline/not starting

- Verify your `DISCORD_TOKEN` is correct
- Check your internet connection
- Make sure all dependencies are installed

## 🤝 Contributing & Contributors

Thanks to [JoeJoeTV](https://github.com/JoeJoeTV) for giving me acces to his project API and contributing to this project !

Go see the server that we work with : [AstroLauncher from ricky davis ! ](https://github.com/ricky-davis/AstroLauncher)

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [AstroLauncher](https://github.com/ricky-davis/AstroLauncher) - Astroneer dedicated server launcher
- [AstroServerCheck API](https://astroservercheck.joejoetv.de/) - Server status API

## 📧 Support

If you have any questions or issues, please open an issue on GitHub.

---

Made with ❤️ for the Astroneer community
