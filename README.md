# Telegram Combo & Proxy Processor Bot

A powerful Telegram bot for processing email:password combinations (combos) and checking proxy servers. Built with Python and python-telegram-bot library.

## 📋 Features

### 🔐 Combo Processing
- **Email:Password Extraction** - Automatically detects and extracts email:password pairs from various formats
- **Duplicate Removal** - Removes duplicate entries automatically
- **Provider Categorization** - Groups combos by email provider (Gmail, Yahoo, Outlook, etc.)
- **Provider Extraction** - Extract specific provider combos as separate files
- **Detailed Statistics** - Shows total combos, duplicates removed, and counts per provider
- **30MB File Limit** - Combo files limited to 30MB
- **Persistent Storage** - Extracted combo files do NOT auto-delete

### 🌐 Proxy Management
- **Proxy Extraction** - Extracts IP:port format proxies from any text file
- **Live Checking** - Tests proxy connectivity with 3-second timeout
- **No File Size Limit** - Upload and check proxy files of any size
- **Progress Tracking** - Real-time progress updates during checking
- **Concurrent Checking** - Checks up to 400 proxies simultaneously
- **Auto-Delete** - Proxy files automatically delete after 30 minutes

### 🚀 Proxy Scraping
- **Multi-Source Scraping** - Scrapes proxies from multiple public sources
- **Protocol Categorization** - Automatically sorts proxies by protocol (HTTP, SOCKS4, SOCKS5)
- **Live Filtering** - Tests scraped proxies and returns only working ones
- **Unchecked Lists** - Always provides the raw scraped list alongside live results
- **30-Minute Auto-Delete** - All scraped proxy files auto-delete after 30 minutes

### 👥 User Management
- **User Tracking** - Automatically saves user IDs
- **Broadcast System** - Owner can broadcast messages to all users
- **Concurrent Processing** - Multiple users can use the bot simultaneously without blocking

## 📦 Installation

### Prerequisites
- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/telegram-combo-proxy-bot.git
cd telegram-combo-proxy-bot
```

2. **Install dependencies**
```bash
pip install python-telegram-bot httpx
```

3. **Configure the bot**

Edit `bot.py` and replace these values:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
OWNER_ID = 1234567890              # Your Telegram ID
```

4. **Run the bot**
```bash
python bot.py
```

## 🎮 Usage

### Commands

| Command | Description | Access |
|---------|-------------|--------|
| `/start` | Display main menu | All users |
| `/broadcast <message>` | Send message to all users | Owner only |

### Main Menu Options

#### 📊 Process Combo
1. Click "📊 Process Combo" button
2. Upload a text file containing email:password combinations
3. Bot processes and displays statistics
4. Click on any provider button to extract specific combos

**Supported formats:**
```
email:password
email|password
email;password
password:email
password|email
password;email
```

**Example:**
```
john.doe@gmail.com:pass123
jane@yahoo.com|secure456
admin@outlook.com;adminpass
```

#### 🌐 Upload Proxies
1. Click "🌐 Upload Proxies" button
2. Upload any text file containing proxies (IP:port format)
3. Bot checks connectivity and returns working proxies
4. No file size limit - upload GB-sized files

**Proxy format:**
```
192.168.1.1:8080
10.0.0.1:3128
172.16.0.1:1080
```

#### 🚀 Scrape & Filter Protocols
1. Click "🚀 Scrape & Filter Protocols" button
2. Bot scrapes proxies from multiple public sources
3. Checks each proxy for connectivity
4. Returns:
   - **Live proxies** per protocol (working)
   - **Raw scraped lists** per protocol (unchecked)
5. All files auto-delete after 30 minutes

## 🔧 Technical Details

### Proxy Sources

| Protocol | Sources |
|----------|---------|
| **HTTP** | proxyscrape.com, TheSpeedX, ShiftyTR, monosans |
| **SOCKS4** | proxyscrape.com, TheSpeedX, ShiftyTR, monosans |
| **SOCKS5** | proxyscrape.com, TheSpeedX, ShiftyTR, monosans, geonode |

### Email Providers Detected

| Category | Providers |
|----------|-----------|
| **Google** | Gmail |
| **Microsoft** | Hotmail, Outlook, Live, MSN |
| **Yahoo** | Yahoo |
| **Apple** | iCloud |
| **AOL** | AOL |
| **Secure** | ProtonMail, PM.me |
| **Other** | Mail.com, GMX, Verizon, Zoho, Yandex, Others |

### Performance Specifications

| Operation | Specification |
|-----------|---------------|
| **Proxy Checking Concurrency** | Up to 450 simultaneous checks |
| **Proxy Timeout** | 3 seconds per proxy |
| **Scraping Timeout** | 15 seconds per source |
| **Auto-Delete Delay** | 30 minutes (1800 seconds) |
| **Combo File Size Limit** | 30MB |
| **Proxy File Size Limit** | No limit |

## 📁 File Structure

```
telegram-combo-proxy-bot/
│
├── bot.py                 # Main bot code
├── bot_users.txt          # Auto-generated user database
├── README.md              # This file
└── requirements.txt       # Dependencies
```

### requirements.txt
```
python-telegram-bot>=20.0
httpx>=0.24.0
```

## ⚙️ Configuration Options

You can modify these settings in `bot.py`:

```python
# File size limits
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB for combo files

# Proxy checking
PROXY_TIMEOUT = 3                  # Seconds to wait for connection
SEMAPHORE_LIMIT = 450              # Maximum concurrent proxy checks

# Auto-delete
AUTO_DELETE_DELAY = 1800          # 30 minutes in seconds
```

## 🔒 Security Features

- **Owner-only Broadcast** - Prevents unauthorized mass messaging
- **User Tracking** - Monitors bot users in `bot_users.txt`
- **File Auto-Delete** - Prevents file clutter in Telegram (proxies only)
- **Size Limits** - Prevents abuse of combo processing
- **Concurrent Protection** - Semaphore limits prevent resource exhaustion

## 🚨 Troubleshooting

### Bot not responding?
- ✅ Check if BOT_TOKEN is correct
- ✅ Ensure internet connectivity
- ✅ Verify Python version (3.7+ required)
- ✅ Check if bot is running (`python bot.py`)

### Proxy checking slow?
- ⚡ Reduce `SEMAPHORE_LIMIT` if experiencing timeouts
- ⚡ Decrease `PROXY_TIMEOUT` for faster checking
- ⚡ Check your internet connection speed

### Combo not processing?
- 📁 Ensure file is under 30MB
- 📁 Check file encoding (UTF-8 recommended)
- 📁 Verify email:password format
- 📁 Try with a small test file first

### Scraping not working?
- 🌐 Check internet connection
- 🌐 Some sources may be temporarily down
- 🌐 Try again in a few minutes

## 📝 Important Notes

- **Combo files** are NOT auto-deleted - they persist permanently
- **All proxy files** auto-delete after 30 minutes
- **Multiple users** can use the bot simultaneously
- **Scraped lists** are ALWAYS provided even if no live proxies found
- **User database** auto-creates when first user starts the bot

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Ideas
- Add more proxy sources
- Support additional combo formats
- Add proxy anonymity checking
- Implement proxy geolocation
- Add combo validation
- Improve performance

## ⚖️ Legal Disclaimer

This tool is for **educational purposes only**. Users are responsible for:

- Complying with all applicable local, state, federal, and international laws
- Respecting terms of service of all websites and services
- Using proxies and combos ethically and legally
- Obtaining proper authorization before testing any systems

**The developer assumes no liability** and is not responsible for any misuse or damage caused by this program. By using this software, you agree to use it responsibly and legally.

## 📄 License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Telegram: [@yourusername](https://t.me/yourusername)

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Excellent Telegram Bot framework
- [httpx](https://github.com/encode/httpx) - Modern HTTP client for Python
- [TheSpeedX](https://github.com/TheSpeedX/SOCKS-List) - Proxy list repository
- [ShiftyTR](https://github.com/ShiftyTR/Proxy-List) - Proxy list repository
- [monosans](https://github.com/monosans/proxy-list) - Proxy list repository
- [geonode](https://geonode.com/) - Proxy API

## 📊 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/telegram-combo-proxy-bot&type=Date)](https://star-history.com/#yourusername/telegram-combo-proxy-bot&Date)

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Python-Telegram-Bot Version**: 20.x  
**Status**: Active Development

⭐ **If you find this bot useful, please consider giving it a star!** ⭐
