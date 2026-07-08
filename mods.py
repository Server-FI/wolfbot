from datetime import datetime, timedelta
from boot import *
def mods(bot):
    @bot.message_handler(regexp="Варны|Warns",chat_types=['supergroup','group'])
    async def warns(message):
        match message.reply_to_message:
            case None:
                if len(message.text.strip().split(" "))==1:
                    count_warns=search_warn(message.from_user.id,message.chat.id)
                    await bot.send_message(message.chat.id,f"Текущее количество варнов: {count_warns}",reply_to_message_id=message.id)
                elif len(message.text.strip().split(" "))==2:
                    status_author=await bot.get_chat_member(message.chat.id,message.from_user.id)
                    match status_author.status:
                        case "administrator":
                            user=search_username(message.text.split(" ")[1][1::],message.chat.id)
                            count_warns=search_warn(user,message.chat.id)
                            await bot.send_message(message.chat.id,f"Текущее количество варнов пользователя: {count_warns}",reply_to_message_id=message.id)
                        case "creator":
                            user=search_username(message.text.split(" ")[1][1::],message.chat.id)
                            count_warns=search_warn(user,message.chat.id)
                            await bot.send_message(message.chat.id,f"Текущее количество варнов пользователя: {count_warns}",reply_to_message_id=message.id)
                        case "left":
                            user=search_username(message.text.split(" ")[1][1::],message.chat.id)
                            count_warns=search_warn(user,message.chat.id)
                            await bot.send_message(message.chat.id,f"Текущее количество варнов пользователя: {count_warns}",reply_to_message_id=message.id)
                        case _:
                            await bot.send_message(message.chat.id,"Вы не можете просматривать чужие варны не являясь модератором",reply_to_message_id=message.id)
            case _:
                status_author=await bot.get_chat_member(message.chat.id,message.from_user.id)
                match status_author.status:
                    case "administrator":
                        count_warns=search_warn(message.reply_to_message.from_user.id,message.chat.id)
                        await bot.send_message(message.chat.id,f"Текущее количество варнов пользователя: {count_warns}",reply_to_message_id=message.id)
                    case "creator":
                        count_warns=search_warn(message.reply_to_message.from_user.id,message.chat.id)
                        await bot.send_message(message.chat.id,f"Текущее количество варнов пользователя: {count_warns}",reply_to_message_id=message.id)
                    case "left":
                        count_warns=search_warn(message.reply_to_message.from_user.id,message.chat.id)
                        await bot.send_message(message.chat.id,f"Текущее количество варнов пользователя: {count_warns}",reply_to_message_id=message.id)
                    case _:
                        await bot.send_message(message.chat.id,"Вы не можете просматривать чужие варны не являясь модератором",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Бан|Ban',chat_types=["supergroup","group"])
    async def ban(message):
        admin=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match admin.status:
            case "administrator":
                if message.reply_to_message!=None:
                    banner=message.reply_to_message.from_user.id
                    status_banner=await bot.get_chat_member(message.chat.id,banner)
                    match status_banner.status:
                        case "administrator":
                            await bot.send_message(message.chat.id, "Вы не можете забанить другого администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете забанить владельца", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете забанить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            await bot.ban_chat_member(message.chat.id,banner)
                            if len(message.text.split())>=2:
                                add_read(banner,message.chat.id,"Бан",message.text[4::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                if re.search("бот",message.text.lower())!=None:
                                    add_filter(status_banner.user.id,status_banner.user.username,message.text[4::])
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {message.text[4::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                add_read(banner,message.chat.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    banner=search_username(message.text.split()[1][1::],message.chat.id)
                    status_banner=await bot.get_chat_member(message.chat.id,banner)
                    match status_banner.status:
                        case "administrator":
                            await bot.send_message(message.chat.id, "Вы не можете забанить другого администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете забанить владельца", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете забанить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            await bot.ban_chat_member(message.chat.id,banner)
                            if len(message.text.split())>2:
                                reason=""
                                for i in message.text.split()[2::]:
                                    reason+=i+" "
                                add_read(banner,message.chat.id,"Бан",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                if re.search("бот",reason.lower())!=None:
                                    add_filter(status_banner.user.id,status_banner.user.username,reason)
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                add_read(banner,message.chat.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "creator":
                if message.reply_to_message!=None:
                    banner=message.reply_to_message.from_user.id
                    status_banner=await bot.get_chat_member(message.chat.id,banner)
                    match status_banner.status:
                        case "administrator":
                            var=await bot.get_me()
                            if banner==var.id:
                                await bot.send_message(message.chat.id, "Вы не можете забанить бота", reply_to_message_id=message.id)
                            else:
                                await bot.send_message(message.chat.id, "Вы не можете забанить администратора через API. Снимите его и затем повторите команду", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете забанить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете забанить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            await bot.ban_chat_member(message.chat.id,banner)
                            if len(message.text.split())>=2:
                                add_read(banner,message.chat.id,"Бан",message.text[4::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                if re.search("бот",message.text.lower())!=None:
                                    add_filter(status_banner.user.id,status_banner.user.username,message.text[4::])
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {message.text[4::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                add_read(banner,message.chat.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    var=await bot.get_me()
                    if message.text.split()[1][1::]==var.username:
                        await bot.send_message(message.chat.id, "Вы не можете забанить бота", reply_to_message_id=message.id)
                    else:
                        banner=search_username(message.text.split()[1][1::],message.chat.id)
                        status_banner=await bot.get_chat_member(message.chat.id,banner)
                        match status_banner.status:
                            case "administrator":
                                await bot.send_message(message.chat.id, "Вы не можете забанить администратора через API. Снимите его и затем повторите команду", reply_to_message_id=message.id)
                            case "creator":
                                await bot.send_message(message.chat.id, "Вы не можете забанить самого себя", reply_to_message_id=message.id)
                            case "left":
                                await bot.send_message(message.chat.id, "Вы не можете забанить анонимного администратора или самого себя", reply_to_message_id=message.id)
                            case _:
                                await bot.ban_chat_member(message.chat.id,banner)
                                if len(message.text.split())>2:
                                    reason=""
                                    for i in message.text.split()[2::]:
                                        reason+=i+" "
                                    add_read(banner,message.chat.id,"Бан",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    if re.search("бот",reason.lower())!=None:
                                        add_filter(status_banner.user.id,status_banner.user.username,reason)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(banner,message.chat.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "left":
                if message.reply_to_message!=None:
                    banner=message.reply_to_message.from_user.id
                    var=await bot.get_me()
                    if banner==var.id:
                        await bot.send_message(message.chat.id, "Вы не можете забанить бота", reply_to_message_id=message.id)
                    else:
                        status_banner=await bot.get_chat_member(message.chat.id,banner)
                        match status_banner.status:
                            case "administrator":
                                await bot.send_message(message.chat.id, "Вы не можете забанить другого администратора или самого себя", reply_to_message_id=message.id)
                            case "creator":
                                await bot.send_message(message.chat.id, "Вы не можете забанить владельца или самого себя", reply_to_message_id=message.id)
                            case "left":
                                await bot.send_message(message.chat.id, "Вы не можете забанить анонимного администратора или самого себя", reply_to_message_id=message.id)
                            case _:
                                await bot.ban_chat_member(message.chat.id,banner)
                                if len(message.text.split())>=2:
                                    add_read(banner,message.chat.id,"Бан",message.text[4::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    if re.search("бот",message.text.lower())!=None:
                                        add_filter(status_banner.user.id,status_banner.user.username,message.text[4::])
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {message.text[4::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(banner,message.chat.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    var=await bot.get_me()
                    if message.text.split()[1][1::]==var.username:
                        await bot.send_message(message.chat.id, "Вы не можете забанить бота", reply_to_message_id=message.id)
                    else:
                        banner=search_username(message.text.split()[1][1::],message.chat.id)
                        status_banner=await bot.get_chat_member(message.chat.id,banner)
                        match status_banner.status:
                            case "administrator":
                                await bot.send_message(message.chat.id, "Вы не можете забанить другого администратора или самого себя", reply_to_message_id=message.id)
                            case "creator":
                                await bot.send_message(message.chat.id, "Вы не можете забанить владельца или самого себя", reply_to_message_id=message.id)
                            case "left":
                                await bot.send_message(message.chat.id, "Вы не можете забанить анонимного администратора или самого себя", reply_to_message_id=message.id)
                            case _:
                                await bot.ban_chat_member(message.chat.id,banner)
                                if len(message.text.split())>2:
                                    reason=""
                                    for i in message.text.split()[2::]:
                                        reason+=i+" "
                                    add_read(banner,message.chat.id,"Бан",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    if re.search("бот",reason.lower())!=None:
                                        add_filter(status_banner.user.id,status_banner.user.username,reason)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(banner,message.chat.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)
    @bot.message_handler(regexp='Мут|Mute',chat_types=["supergroup","group"])
    async def mute_user(message):
        admin=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match admin.status:
            case "administrator":
                if message.reply_to_message!=None:
                    muter=message.reply_to_message.from_user.id
                    status_muter=await bot.get_chat_member(message.chat.id,muter)
                    match status_muter.status:
                        case "administrator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id,"Вы не можете замутить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            if len(message.text.split())>=3:
                                reason=""
                                for i in message.text.split()[2::]:
                                    reason+=i+" "
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-2]} секунд\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} минут\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} часов\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} секунд\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} минут\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} часов\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    muter=search_username(message.text.split()[1][1::],message.chat.id)
                    status_muter=await bot.get_chat_member(message.chat.id,muter)
                    match status_muter.status:
                        case "administrator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id,"Вы не можете замутить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            if len(message.text.split())>=3:
                                reason=""
                                for i in message.text.split()[3::]:
                                    reason+=i+" "
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} секунд\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} минут\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} часов\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} секунд\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} минут\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} часов\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "creator":
                if message.reply_to_message!=None:
                    muter=message.reply_to_message.from_user.id
                    status_muter=await bot.get_chat_member(message.chat.id,muter)
                    match status_muter.status:
                        case "administrator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id,"Вы не можете замутить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            if len(message.text.split())>=3:
                                reason=""
                                for i in message.text.split()[2::]:
                                    reason+=i+" "
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-2]} секунд\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} минут\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} часов\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} секунд\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} минут\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} часов\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    muter=search_username(message.text.split()[1][1::],message.chat.id)
                    status_muter=await bot.get_chat_member(message.chat.id,muter)
                    match status_muter.status:
                        case "administrator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id,"Вы не можете замутить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            if len(message.text.split())>=3:
                                reason=""
                                for i in message.text.split()[3::]:
                                    reason+=i+" "
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} секунд\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} минут\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} часов\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} секунд\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} минут\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} часов\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "left":
                if message.reply_to_message!=None:
                    muter=message.reply_to_message.from_user.id
                    status_muter=await bot.get_chat_member(message.chat.id,muter)
                    match status_muter.status:
                        case "administrator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id,"Вы не можете замутить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            if len(message.text.split())>=3:
                                reason=""
                                for i in message.text.split()[2::]:
                                    reason+=i+" "
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-2]} секунд\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} минут\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} часов\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} секунд\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} минут\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1][0:-1]} часов\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    muter=search_username(message.text.split()[1][1::],message.chat.id)
                    status_muter=await bot.get_chat_member(message.chat.id,muter)
                    match status_muter.status:
                        case "administrator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить администратора или самого себя", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id,"Вы не можете замутить самого себя", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id,"Вы не можете замутить анонимного администратора или самого себя", reply_to_message_id=message.id)
                        case _:
                            if len(message.text.split())>=3:
                                reason=""
                                for i in message.text.split()[3::]:
                                    reason+=i+" "
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} секунд\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} минут\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} часов\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} секунд\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} минут\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,"Мут","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2][0:-1]} часов\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)
    @bot.message_handler(regexp='Варн|Warn',chat_types=["supergroup","group"])
    async def warn_user(message):
        admin=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match admin.status:
            case "administrator":
                if message.reply_to_message!=None:
                    user=message.reply_to_message.from_user.id
                    status_user=await bot.get_chat_member(message.chat.id,user)
                    match status_user.status:
                        case "administrator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение другому администратору или самому себе", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение владельцу", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение анонимному администратору или самому себе", reply_to_message_id=message.id)
                        case _:
                            add_warn(user,message.chat.id)
                            user_warns=search_warn(user,message.chat.id)
                            limit=search_warn_group(message.chat.id)
                            if user_warns==limit:
                                await bot.ban_chat_member(message.chat.id,user)
                                add_read(user,message.chat.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    add_read(user,message.chat.id,"Предупреждение",message.text[5::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {message.text[5::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    user=search_username(message.text.split()[1][1::],message.chat.id)
                    status_user=await bot.get_chat_member(message.chat.id,user)
                    match status_user.status:
                        case "administrator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение другому администратору или самому себе", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение владельцу")
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение анонимному администратору или самому себе", reply_to_message_id=message.id)
                        case _:
                            add_warn(user,message.chat.id)
                            user_warns=search_warn(user,message.chat.id)
                            limit=search_warn_group(message.chat.id)
                            if user_warns==limit:
                                await bot.ban_chat_member(message.chat.id,user)
                                add_read(user,message.chat.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    reason=""
                                    for i in message.text.split()[2::]:
                                        reason+=i+" "
                                    add_read(user,message.chat.id,"Предупреждение",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "creator":
                if message.reply_to_message!=None:
                    user=message.reply_to_message.from_user.id
                    status_user=await bot.get_chat_member(message.chat.id,user)
                    match status_user.status:
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение самому себе", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение анонимному администратору", reply_to_message_id=message.id)
                        case _:
                            var=await bot.get_me()
                            if user==var.id:
                                await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение боту", reply_to_message_id=message.id)
                            else:
                                add_warn(user,message.chat.id)
                                user_warns=search_warn(user,message.chat.id)
                                limit=search_warn_group(message.chat.id)
                                if user_warns==limit:
                                    await bot.ban_chat_member(message.chat.id,user)
                                    add_read(user,message.chat.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    if len(message.text.split())>=2:
                                        add_read(user,message.chat.id,"Предупреждение",message.text[5::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {message.text[5::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                    else:
                                        add_read(user,message.chat.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    var=await bot.get_me()
                    if message.text.split()[1][1::]==var.username:
                        await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение боту", reply_to_message_id=message.id)
                    else:
                        user=search_username(message.text.split()[1][1::],message.chat.id)
                        status_user=await bot.get_chat_member(message.chat.id,user)
                        match status_user.status:
                            case "creator":
                                await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение самому себе", reply_to_message_id=message.id)
                            case "left":
                                await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение анонимному администратору", reply_to_message_id=message.id)
                            case _:
                                add_warn(user,message.chat.id)
                                user_warns=search_warn(user,message.chat.id)
                                limit=search_warn_group(message.chat.id)
                                if user_warns==limit:
                                    await bot.ban_chat_member(message.chat.id,user)
                                    add_read(user,message.chat.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    if len(message.text.split())>=2:
                                        reason=""
                                        for i in message.text.split()[2::]:
                                            reason+=i+" "
                                        add_read(user,message.chat.id,"Предупреждение",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                    else:
                                        add_read(user,message.chat.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "left":
                if message.reply_to_message!=None:
                    user=message.reply_to_message.from_user.id
                    status_user=await bot.get_chat_member(message.chat.id,user)
                    match status_user.status:
                        case "administrator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение другому администратору или самому себе", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение владельцу или самому себе", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение анонимному администратору или самому себе", reply_to_message_id=message.id)
                        case _:
                            add_warn(user,message.chat.id)
                            user_warns=search_warn(user,message.chat.id)
                            limit=search_warn_group(message.chat.id)
                            if user_warns==limit:
                                await bot.ban_chat_member(message.chat.id,user)
                                add_read(user,message.chat.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    add_read(user,message.chat.id,"Предупреждение",message.text[5::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {message.text[5::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    user=search_username(message.split()[1][1::],message.chat.id)
                    status_user=await bot.get_chat_member(message.chat.id,user)
                    match status_user:
                        case "administrator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение другому администратору или самому себе", reply_to_message_id=message.id)
                        case "creator":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение владельцу", reply_to_message_id=message.id)
                        case "left":
                            await bot.send_message(message.chat.id, "Вы не можете выдать предупреждение анонимному администратору или самому себе", reply_to_message_id=message.id)
                        case _:
                            add_warn(user,message.chat.id)
                            user_warns=search_warn(user,message.chat.id)
                            limit=search_warn_group(message.chat.id)
                            if user_warns==limit:
                                await bot.ban_chat_member(message.chat.id,user)
                                add_read(user,message.chat.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    reason=""
                                    for i in message.text.split()[2::]:
                                        reason+=i+" "
                                    add_read(user,message.chat.id,"Предупреждение",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)
    @bot.message_handler(regexp='Изменить максимум|Change warns',chat_types=["supergroup","group"])
    async def change_warns(message):
        user=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match user.status:
            case "administrator":
                change_warn_group(message.chat.id,int(message.text.split()[2]))
                await bot.send_message(message.chat.id, f"Количество варнов для бана изменено до {message.text.split()[2]}", reply_to_message_id=message.id)
            case "creator":
                change_warn_group(message.chat.id,int(message.text.split()[2]))
                await bot.send_message(message.chat.id, f"Количество варнов для бана изменено до {message.text.split()[2]}", reply_to_message_id=message.id)
            case "left":
                change_warn_group(message.chat.id,int(message.text.split()[2]))
                await bot.send_message(message.chat.id, f"Количество варнов для бана изменено до {message.text.split()[2]}", reply_to_message_id=message.id)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)