import signal,sys,asyncio
from telethon import TelegramClient, events, utils
from telethon.tl.types import UpdateUserName, PeerChannel
from boot import *
from tele import bot
api_id="Для получения необходимо создать приложение на https://my.telegram.org"
api_hash="Для получения необходимо создать приложение на https://my.telegram.org"
token=access()["tg"]
parser=TelegramClient("parse",api_id,api_hash)
@parser.on(events.ChatAction)
async def parse_chat(event):
    name=await parser.get_me()
    if event.user_id==name.id and event.action_message==None:
        users=await parser.get_participants(event.original_update.channel_id)
        ids=[]
        usernames=[]
        print(users)
        for i in users:
            if i.bot!=True:
                ids.append(i.id)
                usernames.append(i.username)
        chat=utils.get_peer_id(PeerChannel(channel_id=event.original_update.channel_id))
        roles=[]
        for i in ids:
            user=await bot.get_chat_member(chat,i)
            roles.append(user.status)
        for i in ids:
            for j in usernames:
                for n in roles:
                    add_user(i,j,chat,n)
    elif event.new_title!=None:
        update_group(utils.get_peer_id(event.action_message.peer_id),event.new_title)
@parser.on(events.Raw)
async def raw_handler(event):
    if isinstance(event, UpdateUserName):
        user_id=event.user_id
        new_username=event.usernames[0].username
        update_username(user_id,new_username)
def signal_handler(sig,frame):
    write_log("Telethon был отключён")
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)
async def start_telethon():
    try:
        print("Telethon работает")
        write_log("Telethon запущен")
        await parser.start(bot_token=token)
        await parser.run_until_disconnected()
    except Exception as e:
        print(f"Ошибка: {e}")
code=input("Введите код: ")
if code=="1011":
    asyncio.run(start_telethon())