import asyncio,signal,sys
from telebot.async_telebot import AsyncTeleBot
from boot import *
from commands import coms
from mods import mods
from messages import messages
from guilds import guild
t=access()["tg"]
bot=AsyncTeleBot(t)
con()
coms(bot)
mods(bot)
guild(bot)
messages(bot)
def signal_handler(sig,frame):
    write_log("Бот был отключён")
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)
async def start():
    write_log("Бот запущен")
    name=await bot.get_me()
    print(f"Logged in as {name.first_name}")
    await bot.polling(non_stop=True, interval=0, skip_pending=True)
code=input("Введите код: ")
if code=="1010":
    asyncio.run(start())