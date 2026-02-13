import re
import time
import asyncio
import socket
import httpx
import os
from collections import Counter, defaultdict
from telegram import (
    Update,
    InputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
import io

BOT_TOKEN = "ENTER_YOUR_BOT_TOKEN"
OWNER_ID = 123456789  # <--- REPLACE THIS WITH YOUR TELEGRAM ID
USER_DATA_FILE = "bot_users.txt"
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB (Still applies to combo files)

# ==========================================================
# ================== USER TRACKING SYSTEM ==================
# ==========================================================

def save_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        with open(USER_DATA_FILE, "a") as f:
            f.write(f"{user_id}\n")

def get_users():
    if not os.path.exists(USER_DATA_FILE): return []
    with open(USER_DATA_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

# ==========================================================
# ================== ADMIN BROADCAST =======================
# ==========================================================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage:\n/broadcast Your message here")
        return

    message_text = " ".join(context.args)
    users = get_users()

    if not users:
        await update.message.reply_text("No users found.")
        return

    sent = 0
    failed = 0

    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message_text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast Completed\n\n"
        f"👥 Total Users: {len(users)}\n"
        f"📤 Sent: {sent}\n"
        f"❌ Failed: {failed}"
    )

# ==========================================================
# ================== COMBO SYSTEM (UNCHANGED) ==============
# ==========================================================

KNOWN_PROVIDERS = {
    "gmail": ["gmail.com"], "hotmail": ["hotmail.com"], "outlook": ["outlook.com"],
    "yahoo": ["yahoo.com"], "icloud": ["icloud.com"], "aol": ["aol.com"],
    "protonmail": ["protonmail.com"], "mail": ["mail.com"], "gmx": ["gmx.com"],
    "live": ["live.com"], "msn": ["msn.com"], "verizon": ["verizon.net"],
    "zoho": ["zoho.com"], "yandex": ["yandex.com"], "pm": ["pm.me"],
}
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def clean_combo_line(line):
    email_match = re.search(EMAIL_REGEX, line)
    if not email_match: return None, None
    email = email_match.group().lower()
    separators = [":", "|", ";"]
    for sep in separators:
        parts = line.strip().split(sep)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) < 2: continue
        for i, part in enumerate(parts):
            if email in part.lower():
                if i + 1 < len(parts):
                    password = parts[i + 1].strip()
                    if "@" not in password and len(password) > 1: return f"{email}:{password}", email
                if i - 1 >= 0:
                    password = parts[i - 1].strip()
                    if "@" not in password and len(password) > 1: return f"{password}:{email}", email
    return None, None

def detect_provider(email):
    domain = email.split("@")[1].lower()
    base = domain.split(".")[0]
    if base in KNOWN_PROVIDERS: return base.capitalize()
    for provider, domains in KNOWN_PROVIDERS.items():
        for d in domains:
            if domain.endswith(d): return provider.capitalize()
    return "Others"

def process_list(text):
    start_time = time.time()
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        cleaned, email = clean_combo_line(line)
        if cleaned: cleaned_lines.append(cleaned)
    total = len(cleaned_lines)
    unique_lines = list(set(cleaned_lines))
    dups_removed = total - len(unique_lines)
    provider_groups = defaultdict(list)
    for line in unique_lines:
        email = re.search(EMAIL_REGEX, line).group()
        provider = detect_provider(email)
        provider_groups[provider].append(line)
    result = [f"Total: {total:,}", f"Dups Removed: {dups_removed:,}", "— — — — — — — —"]
    counter = Counter({p: len(lst) for p, lst in provider_groups.items()})
    for p in sorted(counter): result.append(f"{p}: {counter[p]:,}")
    result.extend(["— — — — — — — —", f"Time: {round(time.time() - start_time, 2)}s"])
    return "\n".join(result), provider_groups

# ==========================================================
# ================== PROXY SYSTEM ==========================
# ==========================================================

def clean_proxies(text):
    found = re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})\b", text)
    return list(set(found))

async def scrape_proxies_categorized():
    sources = {
        "HTTP": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ],
        "SOCKS4": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt"
        ],
        "SOCKS5": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
        ]
    }
    categorized_proxies = defaultdict(list)
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        for protocol, urls in sources.items():
            tasks = [client.get(url) for url in urls]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for res in responses:
                if isinstance(res, httpx.Response) and res.status_code == 200:
                    categorized_proxies[protocol].extend(clean_proxies(res.text))
    return {p: list(set(l)) for p, l in categorized_proxies.items()}

async def check_proxy(proxy, timeout=3):
    try:
        host, port = proxy.split(":")[0], int(proxy.split(":")[1])
        loop = asyncio.get_event_loop()
        await asyncio.wait_for(loop.run_in_executor(
            None, lambda: socket.create_connection((host, port), timeout)
        ), timeout=timeout)
        return True
    except: return False

async def check_proxies_async_categorized(categorized_proxies, message):
    working_data = defaultdict(list)
    total_to_check = sum(len(v) for v in categorized_proxies.values())
    checked = 0
    semaphore = asyncio.Semaphore(450)

    async def sem_task(proxy, protocol):
        nonlocal checked
        async with semaphore:
            result = await check_proxy(proxy)
            checked += 1
            if result: working_data[protocol].append(proxy)
            if checked % 200 == 0 or checked == total_to_check:
                try:
                    await message.edit_text(
                        f"⚡️ Progress: {checked:,}/{total_to_check:,}\n"
                        f"✅ Live (HTTP): {len(working_data['HTTP']):,}\n"
                        f"✅ Live (SOCKS4): {len(working_data['SOCKS4']):,}\n"
                        f"✅ Live (SOCKS5): {len(working_data['SOCKS5']):,}"
                    )
                except: pass

    tasks = [sem_task(p, proto) for proto, p_list in categorized_proxies.items() for p in p_list]
    await asyncio.gather(*tasks)
    return working_data

# ==========================================================
# ================== UI & UTILS ============================
# ==========================================================

async def auto_delete_file(message_obj, delay=1800):
    await asyncio.sleep(delay)
    try: await message_obj.delete()
    except: pass

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Process Combo", callback_data="combo")],
        [InlineKeyboardButton("📂 Extract Provider", callback_data="extract")],
        [InlineKeyboardButton("🌐 Upload Proxies", callback_data="proxy")],
        [InlineKeyboardButton("🚀 Scrape & Filter Protocols", callback_data="scrape_proxies")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    await update.message.reply_text("Main Menu:", reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "combo":
        context.user_data["mode"] = "combo"
        await query.edit_message_text("Upload combo file now (Max 30MB).")
    
    elif query.data == "proxy":
        context.user_data["mode"] = "proxy"
        await query.edit_message_text("Upload proxy file now (No size limit).")
    
    elif query.data == "scrape_proxies":
        msg = await query.edit_message_text("🔍 Scraping and sorting...")
        
        # Create async task for this user so bot remains responsive
        asyncio.create_task(process_scrape_request(query, msg, context))
    
    elif query.data == "extract":
        if "providers" not in context.user_data:
            await query.edit_message_text("No combo processed yet.")
            return
        buttons = [[InlineKeyboardButton(p, callback_data=f"ext_{p}")] for p in context.user_data["providers"]]
        await query.edit_message_text("Select provider:", reply_markup=InlineKeyboardMarkup(buttons))
    
    elif query.data.startswith("ext_"):
        provider = query.data.replace("ext_", "")
        data = "\n".join(context.user_data["providers"][provider])
        file = io.BytesIO(data.encode()); file.name = f"{provider}.txt"
        sent_msg = await query.message.reply_document(InputFile(file), caption=f"Extracted {provider}\n(Auto-deletes in 30m)")
        asyncio.create_task(auto_delete_file(sent_msg))

async def process_scrape_request(query, msg, context):
    """Separate function to handle scraping without blocking other users"""
    categorized = await scrape_proxies_categorized()
    working_map = await check_proxies_async_categorized(categorized, msg)
    
    found_any = False
    for proto, live_list in working_map.items():
        if live_list:
            found_any = True
            file = io.BytesIO("\n".join(live_list).encode()); file.name = f"{proto}_live.txt"
            sent_msg = await query.message.reply_document(InputFile(file), caption=f"✅ {proto} Live: {len(live_list):,}\n(Auto-deletes in 30m)")
            asyncio.create_task(auto_delete_file(sent_msg))
    
    # ALWAYS send the scraped proxy list, even if no live proxies found
    for proto, proxy_list in categorized.items():
        file = io.BytesIO("\n".join(proxy_list).encode()); file.name = f"{proto}_scraped.txt"
        sent_msg = await query.message.reply_document(
            InputFile(file), 
            caption=f"📦 {proto} Scraped: {len(proxy_list):,} proxies (unchecked)\n(Auto-deletes in 30m)"
        )
        asyncio.create_task(auto_delete_file(sent_msg))
    
    if not found_any:
        await query.message.reply_text("⚠️ No live proxies found. Sent scraped proxy lists instead.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document: return
    
    file = await update.message.document.get_file()
    content = await file.download_as_bytearray()
    text = content.decode("utf-8", errors="ignore")

    # Proxy mode - NO SIZE LIMIT
    if context.user_data.get("mode") == "proxy":
        # Create async task for this user so bot remains responsive
        asyncio.create_task(process_proxy_file(update, context, text))
        return

    # Combo mode - STILL HAS 30MB LIMIT
    if update.message.document.file_size > MAX_FILE_SIZE:
        await update.message.reply_text("❌ File too large. Max limit is 30MB.")
        return

    result, groups = process_list(text)
    context.user_data["providers"] = groups
    await update.message.reply_text(result)
    if groups:
        buttons = [[InlineKeyboardButton(p, callback_data=f"ext_{p}")] for p in sorted(groups.keys())]
        await update.message.reply_text("Select provider to extract:", reply_markup=InlineKeyboardMarkup(buttons))

async def process_proxy_file(update, context, text):
    """Separate function to handle proxy file processing without blocking other users"""
    proxies = clean_proxies(text)
    msg = await update.message.reply_text(f"Checking {len(proxies):,} proxies...")
    
    working = []
    checked = 0
    sem = asyncio.Semaphore(400)
    async def check_task(p):
        nonlocal checked
        async with sem:
            res = await check_proxy(p)
            checked += 1
            if res: working.append(p)
            if checked % 100 == 0 or checked == len(proxies):
                try: await msg.edit_text(f"⚡️ Progress: {checked:,}/{len(proxies):,}\n✅ Live: {len(working):,}")
                except: pass
    
    await asyncio.gather(*(check_task(p) for p in proxies))
    file_out = io.BytesIO("\n".join(working).encode()); file_out.name = "working.txt"
    sent_msg = await update.message.reply_document(InputFile(file_out), caption="Working proxies (Auto-deletes in 30m)")
    asyncio.create_task(auto_delete_file(sent_msg))

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    print("Bot is live...")
    app.run_polling()

if __name__ == "__main__":
    main()
