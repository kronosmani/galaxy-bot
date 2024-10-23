import logging
import time
import aiohttp
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevelname)s',
    level=logging.INFO
)

error_log = []
last_scan_time = time.time()
api_keys = ["c3bc52f3a84cf4a861fd3f9787c1ef3c"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я твой бот для Галакси онлайн.')

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global last_scan_time
    current_time = time.time()
    if current_time - last_scan_time < 5:
        await update.message.reply_text('Подождите немного перед следующим сканированием.')
        return

    last_scan_time = current_time
    await update.message.reply_text('Запуск сканирования. Пожалуйста, подождите...')
    data = None

    for api_key in api_keys:
        data = await get_warnings(api_key)
        if data:
            break

    if data:
        await update.message.reply_text(f'Получены данные: {data}')
    else:
        error_msg = 'Ошибка при сканировании планет.'
        error_log.append(error_msg)
        await update.message.reply_text(error_msg)

async def get_errors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if error_log:
        await update.message.reply_text('\n'.join(error_log))
    else:
        await update.message.reply_text('Ошибок пока нет.')

async def get_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("http://ipinfo.io/ip") as response:
            ip = await response.text()
            await update.message.reply_text(f"Your external IP is {ip.strip()}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

async def get_warnings(api_key):
    url = f"https://galaxyonline.io/api/galaxy-users/get-warnings?key={api_key}"
    try:
        logging.info(f'Fetching data from {url}')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logging.info(f'API response status: {response.status}')
                if response.status == 200:
                    data = await response.json()
                    logging.info(f'API Response: {data}')
                    return data
                else:
                    error_msg = f'API Error: {response.status}'
                    logging.error(error_msg)
                    error_log.append(error_msg)
                    return None
    except Exception as e:
        error_msg = f'Request failed: {e}'
        logging.error(error_msg)
        error_log.append(error_msg)
        return None

def main() -> None:
    application = Application.builder().token("8126429611:AAEwRzmiwBsL6fpqSX2n3WhiibDVwtM8Hf0").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scan", scan))
    application.add_handler(CommandHandler("errors", get_errors))
    application.add_handler(CommandHandler("get_ip", get_ip))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())