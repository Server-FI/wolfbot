from datetime import datetime, timedelta
from boot import *
from funcs import *
def mods(bot):
    @bot.message_handler(regexp="Варны|Warns",chat_types=['supergroup','group'])
    async def warns(message):
        match message.reply_to_message:
            case None:
                if len(message.text.strip().split(" "))==1:
                    match message.from_user.is_bot:
                        case True:
                            pass
                        case False:
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
                                add_read(banner,message.chat.id,message.from_user.id,"Бан",message.text[4::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                if re.search("бот",message.text.lower())!=None:
                                    add_filter(status_banner.user.id,status_banner.user.username,message.text[4::])
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {message.text[4::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                add_read(banner,message.chat.id,message.from_user.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                add_read(banner,message.chat.id,message.from_user.id,"Бан",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                if re.search("бот",reason.lower())!=None:
                                    add_filter(status_banner.user.id,status_banner.user.username,reason)
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                add_read(banner,message.chat.id,message.from_user.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                add_read(banner,message.chat.id,message.from_user.id,"Бан",message.text[4::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                if re.search("бот",message.text.lower())!=None:
                                    add_filter(status_banner.user.id,status_banner.user.username,message.text[4::])
                                await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {message.text[4::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                add_read(banner,message.chat.id,message.from_user.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                    add_read(banner,message.chat.id,message.from_user.id,"Бан",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    if re.search("бот",reason.lower())!=None:
                                        add_filter(status_banner.user.id,status_banner.user.username,reason)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(banner,message.chat.id,message.from_user.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                    add_read(banner,message.chat.id,message.from_user.id,"Бан",message.text[4::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    if re.search("бот",message.text.lower())!=None:
                                        add_filter(status_banner.user.id,status_banner.user.username,message.text[4::])
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {message.text[4::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(banner,message.chat.id,message.from_user.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                    add_read(banner,message.chat.id,message.from_user.id,"Бан",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    if re.search("бот",reason.lower())!=None:
                                        add_filter(status_banner.user.id,status_banner.user.username,reason)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(banner,message.chat.id,message.from_user.id,"Бан","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_banner.user.first_name}](https://t.me/{status_banner.user.username}) забанен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)
    @bot.message_handler(regexp='Снять блокировку|Remove block',chat_types=["supergroup","group"])
    async def unban_user(message):
        admin=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match admin.status:
            case "administrator":
                if message.reply_to_message!=None:
                    unbaner=message.reply_to_message.from_user.id
                    status_unbaner=await bot.get_chat_member(message.chat.id,unbaner)
                    match(message.text.split()):
                        case 2:
                            add_read(status_unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unbaner=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unbaner=await bot.get_chat_member(message.chat.id,unbaner)
                    match(message.text.split()):
                        case 3:
                            add_read(status_unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.unban_chat_member(message.chat.id,unbaner)
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.unban_chat_member(message.chat.id,unbaner)
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "creator":
                if message.reply_to_message!=None:
                    unbaner=message.reply_to_message.from_user.id
                    status_unbaner=await bot.get_chat_member(message.chat.id,unbaner)
                    match(message.text.split()):
                        case 2:
                            add_read(status_unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unbaner=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unbaner=await bot.get_chat_member(message.chat.id,unbaner)
                    match(message.text.split()):
                        case 3:
                            add_read(status_unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.unban_chat_member(message.chat.id,unbaner)
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.unban_chat_member(message.chat.id,unbaner)
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "left":
                if message.reply_to_message!=None:
                    unbaner=message.reply_to_message.from_user.id
                    status_unbaner=await bot.get_chat_member(message.chat.id,unbaner)
                    match(message.text.split()):
                        case 2:
                            add_read(status_unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unbaner=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unbaner=await bot.get_chat_member(message.chat.id,unbaner)
                    match(message.text.split()):
                        case 3:
                            add_read(status_unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.unban_chat_member(message.chat.id,unbaner)
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(unbaner.user.id,message.chat.id,message.from_user.id,"Снятие бана",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.unban_chat_member(message.chat.id,unbaner)
                            await bot.send_message(message.chat.id, f"С пользователя [{unbaner.user.first_name}](https://t.me/{unbaner.user.username}) снят бан\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[1][-1]=="с" or message.text.lower().split()[1][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[1][-1]=="м" or message.text.lower().split()[1][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[1]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[1][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[1]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if message.text.lower().split()[2][-1]=="с" or message.text.lower().split()[2][-1]=="s":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(seconds=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                elif message.text.lower().split()[2][-1]=="м" or message.text.lower().split()[2][-1]=="m":
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(minutes=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(status_muter.user.id,message.chat.id,message.from_user.id,f"Мут {message.text.lower().split()[2]}","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.restrict_chat_member(message.chat.id,muter,until_date=datetime.now()+timedelta(hours=int(message.text.split()[2][0:-1])),can_send_messages=False)
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_muter.user.first_name}](https://t.me/{status_muter.user.username}) замучен на {message.text.split()[2]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)
    @bot.message_handler(regexp='Снять запрет|Remove zapret',chat_types=["supergroup","group"])
    async def unmute_user(message):
        admin=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match admin.status:
            case "administrator":
                info=await bot.get_chat(message.chat.id)
                if message.reply_to_message!=None:
                    unmuter=message.reply_to_message.from_user.id
                    status_unmuter=await bot.get_chat_member(message.chat.id,unmuter)
                    match len(message.text.split()):
                        case 2:
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unmuter=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unmuter=await bot.get_chat_member(message.chat.id,unmuter)
                    match len(message.text.split()):
                        case 3:
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "creator":
                info=await bot.get_chat(message.chat.id)
                if message.reply_to_message!=None:
                    unmuter=message.reply_to_message.from_user.id
                    status_unmuter=await bot.get_chat_member(message.chat.id,unmuter)
                    match len(message.text.split()):
                        case 2:
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unmuter=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unmuter=await bot.get_chat_member(message.chat.id,unmuter)
                    match len(message.text.split()):
                        case 3:
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "left":
                info=await bot.get_chat(message.chat.id)
                if message.reply_to_message!=None:
                    unmuter=message.reply_to_message.from_user.id
                    status_unmuter=await bot.get_chat_member(message.chat.id,unmuter)
                    match len(message.text.split()):
                        case 2:
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unmuter=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unmuter=await bot.get_chat_member(message.chat.id,unmuter)
                    match len(message.text.split()):
                        case 3:
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(status_unmuter.user.id,message.chat.id,message.from_user.id,"Снятие мута",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.restrict_chat_member(message.chat.id,unmuter,permissions=info.permissions)
                            await bot.send_message(message.chat.id, f"Пользователь [{status_unmuter.user.first_name}](https://t.me/{status_unmuter.user.username}) размучен\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
                                add_read(user,message.chat.id,message.from_user.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение",message.text[5::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {message.text[5::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                add_read(user,message.chat.id,message.from_user.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    reason=""
                                    for i in message.text.split()[2::]:
                                        reason+=i+" "
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                    add_read(user,message.chat.id,message.from_user.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    if len(message.text.split())>=2:
                                        add_read(user,message.chat.id,message.from_user.id,"Предупреждение",message.text[5::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {message.text[5::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                    else:
                                        add_read(user,message.chat.id,message.from_user.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                    add_read(user,message.chat.id,message.from_user.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    if len(message.text.split())>=2:
                                        reason=""
                                        for i in message.text.split()[2::]:
                                            reason+=i+" "
                                        add_read(user,message.chat.id,message.from_user.id,"Предупреждение",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                        await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                    else:
                                        add_read(user,message.chat.id,message.from_user.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
                                add_read(user,message.chat.id,message.from_user.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение",message.text[5::],datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {message.text[5::]}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    user=search_username(message.text.split()[1][1::],message.chat.id)
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
                                add_read(user,message.chat.id,message.from_user.id,"Бан","Максимальное количество предупреждений",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) забанен\nПричина: максимальное количество предупреждений\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                            else:
                                if len(message.text.split())>=2:
                                    reason=""
                                    for i in message.text.split()[2::]:
                                        reason+=i+" "
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                                else:
                                    add_read(user,message.chat.id,message.from_user.id,"Предупреждение","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    await bot.send_message(message.chat.id, f"Пользователь [{status_user.user.first_name}](https://t.me/{status_user.user.username}) получил предупреждение\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case _:
                await bot.send_message(message.chat.id, "Данная команда доступна только администрации и модерации", reply_to_message_id=message.id)
    @bot.message_handler(regexp='Снять предупреждение|Remove wurn',chat_types=["supergroup","group"])
    async def unwarn_user(message):
        admin=await bot.get_chat_member(message.chat.id,message.from_user.id)
        match admin.status:
            case "administrator":
                if message.reply_to_message!=None:
                    unwarner=message.reply_to_message.from_user.id
                    status_unwarner=await bot.get_chat_member(message.chat.id,unwarner)
                    match(message.text.split()):
                        case 2:
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unwarner=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unwarner=await bot.get_chat_member(message.chat.id,unwarner)
                    match(message.text.split()):
                        case 3:
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "creator":
                if message.reply_to_message!=None:
                    unwarner=message.reply_to_message.from_user.id
                    status_unwarner=await bot.get_chat_member(message.chat.id,unwarner)
                    match(message.text.split()):
                        case 2:
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unwarner=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unwarner=await bot.get_chat_member(message.chat.id,unwarner)
                    match(message.text.split()):
                        case 3:
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
            case "left":
                if message.reply_to_message!=None:
                    unwarner=message.reply_to_message.from_user.id
                    status_unwarner=await bot.get_chat_member(message.chat.id,unwarner)
                    match(message.text.split()):
                        case 2:
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[2::]:
                                reason+=i+" "
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                else:
                    unwarner=search_username(message.text.split()[2][1::],message.chat.id)
                    status_unwarner=await bot.get_chat_member(message.chat.id,unwarner)
                    match(message.text.split()):
                        case 3:
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна","Не указана",datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
                        case _:
                            reason=""
                            for i in message.text.split()[3::]:
                                reason+=i+" "
                            add_read(status_unwarner.user.id,message.chat.id,message.from_user.id,"Снятие варна",reason,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            await bot.send_message(message.chat.id, f"С пользователя [{status_unwarner.user.first_name}](https://t.me/{status_unwarner.user.username}) снят варн\nПричина: {reason}\nИнициатор: [{message.from_user.first_name}](https://t.me/{message.from_user.username})", parse_mode="Markdown", reply_to_message_id=message.id, disable_web_page_preview = True)
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
    @bot.message_handler(regexp='Задать правило|Settings Rule',chat_types=['supergroup','group'])
    async def settings_rule(message):
        if message.from_user.first_name=="Telegram":
            pass
        else:
            role=await bot.get_chat_member(message.chat.id,message.from_user.id)
            match role.status:
                case "administrator":
                    rules=""
                    for i in message.text.split("\n")[1::]:
                        rules+=i+"  "
                    rules=rules.strip().replace("  ","|")
                    settings_group_rules(message.chat.id,rules)
                    await bot.send_message(message.chat.id,"Правила чата заданы",reply_to_message_id=message.id)
                case "creator":
                    rules=""
                    for i in message.text.split("\n")[1::]:
                        rules+=i+"  "
                    rules=rules.strip().replace("  ","|")
                    settings_group_rules(message.chat.id,rules)
                    await bot.send_message(message.chat.id,"Правила чата заданы",reply_to_message_id=message.id)
                case "left":
                    rules=""
                    for i in message.text.split("\n")[1::]:
                        rules+=i+"  "
                    rules=rules.strip().replace("  ","|")
                    settings_group_rules(message.chat.id,rules)
                    await bot.send_message(message.chat.id,"Правила чата заданы",reply_to_message_id=message.id)
                case _:
                    await bot.send_message(message.chat.id,"Вы не можете задавать правила чата не являясь модератором",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Добавить правило|Add Rule',chat_types=['supergroup','group'])
    async def add_rule(message):
        if message.from_user.first_name=="Telegram":
            pass
        else:
            role=await bot.get_chat_member(message.chat.id,message.from_user.id)
            match role.status:
                case "administrator":
                    rules=group_rules(message.chat.id)
                    new_rules=message.text.split("  ")[2]
                    if re.search(",",new_rules)==None:
                        new_rules1=add_rule_in_list(rules,new_rules)
                    else:
                        new_rules2=rules
                        for i in new_rules.split(","):
                            new_rules1=add_rule_in_list(new_rules2,i)
                            new_rules2=new_rules1
                    settings_group_rules(message.chat.id,new_rules1)
                    await bot.send_message(message.chat.id,"Правило чата добавлено",reply_to_message_id=message.id)
                case "creator":
                    rules=group_rules(message.chat.id)
                    new_rules=message.text.split("  ")[2]
                    if re.search(",",new_rules)==None:
                        new_rules1=add_rule_in_list(rules,new_rules)
                    else:
                        new_rules2=rules
                        for i in new_rules.split(","):
                            new_rules1=add_rule_in_list(new_rules2,i)
                            new_rules2=new_rules1
                    settings_group_rules(message.chat.id,new_rules1)
                    await bot.send_message(message.chat.id,"Правило чата добавлено",reply_to_message_id=message.id)
                case "left":
                    rules=group_rules(message.chat.id)
                    new_rules=message.text.split("  ")[2]
                    if re.search(",",new_rules)==None:
                        new_rules1=add_rule_in_list(rules,new_rules)
                    else:
                        new_rules2=rules
                        for i in new_rules.split(","):
                            new_rules1=add_rule_in_list(new_rules2,i)
                            new_rules2=new_rules1
                    settings_group_rules(message.chat.id,new_rules1)
                    await bot.send_message(message.chat.id,"Правило чата добавлено",reply_to_message_id=message.id)
                case _:
                    await bot.send_message(message.chat.id,"Вы не можете добавлять правило не являясь модератором",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Удалить правило|Remove Rule',chat_types=['supergroup','group'])
    async def remove_rule(message):
        if message.from_user.first_name=="Telegram":
            pass
        else:
            role=await bot.get_chat_member(message.chat.id,message.from_user.id)
            match role.status:
                case "administrator":
                    rules=group_rules(message.chat.id)
                    new_rules=message.text.split(" ")[2]
                    if re.search(",",new_rules)==None:
                        new_rules1=remove_rule_in_list(rules,new_rules)
                    else:
                        ind=0
                        new_rules2=rules
                        for i in new_rules.split(","):
                            new_rules1=remove_rule_in_list(new_rules2,int(i)-ind)
                            new_rules2=new_rules1
                            ind+=1
                    settings_group_rules(message.chat.id,new_rules1)
                    await bot.send_message(message.chat.id,"Правило чата удалено",reply_to_message_id=message.id)
                case "creator":
                    rules=group_rules(message.chat.id)
                    new_rules=message.text.split(" ")[2]
                    if re.search(",",new_rules)==None:
                        new_rules1=remove_rule_in_list(rules,new_rules)
                    else:
                        ind=0
                        new_rules2=rules
                        for i in new_rules.split(","):
                            new_rules1=remove_rule_in_list(new_rules2,int(i)-ind)
                            new_rules2=new_rules1
                            ind+=1
                    settings_group_rules(message.chat.id,new_rules1)
                    await bot.send_message(message.chat.id,"Правило чата удалено",reply_to_message_id=message.id)
                case "left":
                    rules=group_rules(message.chat.id)
                    new_rules=message.text.split(" ")[2]
                    if re.search(",",new_rules)==None:
                        new_rules1=remove_rule_in_list(rules,new_rules)
                    else:
                        ind=0
                        new_rules2=rules
                        for i in new_rules.split(","):
                            new_rules1=remove_rule_in_list(new_rules2,int(i)-ind)
                            new_rules2=new_rules1
                            ind+=1
                    settings_group_rules(message.chat.id,new_rules1)
                    await bot.send_message(message.chat.id,"Правило чата удалено",reply_to_message_id=message.id)
                case _:
                    await bot.send_message(message.chat.id,"Вы не можете удалять правило не являясь модератором",reply_to_message_id=message.id)