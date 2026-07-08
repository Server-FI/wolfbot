from telebot import types
from boot import *
from funcs import *
def guild(bot):
    @bot.message_handler(regexp='Список гильдий|Guilds',chat_types=["supergroup","group"])
    async def list_guilds(message):
        guilds=search_guilds(message.chat.id)
        list=""
        if guilds==None or str(guilds)=="[]":
            await bot.send_message(message.chat.id,f"Список гильдий\nПока никакие гильдии не появились",reply_to_message_id=message.id)
        else:
            for i in guilds:
                owner_id=search_userid(i[4])
                owner=await bot.get_chat_member(message.chat.id,owner_id)
                ind=1
                list+=f"Гильдия №{ind}. Название: {i[1]}. Тип: {i[2]}. Количество: {i[4]}/{i[5]}. Владелец: [{owner.user.first_name}](https://t.me/{owner.user.username})\n"
                ind+=1
            await bot.send_message(message.chat.id,f"Список гильдий\n{list}",parse_mode='Markdown',disable_web_page_preview = True,reply_to_message_id=message.id)
    @bot.message_handler(regexp='Присоединиться к гильдии|Join the guild',chat_types=["supergroup","group"])
    async def join_guild(message):
        name=""
        for i in message.text.split()[3::]:
            name+=i+" "
        guild=search_guild(name,message.chat.id)
        match guild:
            case None:
                await bot.send_message(message.chat.id,"Вы не можете вступить в несуществующую гильдию",reply_to_message_id=message.id)
            case _:
                match guild[2]:
                    case "Открытый":
                        if int(guild[5])<int(guild[6]):
                            member=check_user_guild(message.from_user.id,message.chat.id)
                            if member==None:
                                join_ex_guild(message.from_user.id,message.chat.id,name)
                                await bot.send_message(message.chat.id,f"Вы вступили в гильдию {name}",reply_to_message_id=message.id)
                            else:
                                await bot.send_message(message.chat.id,"Вы не можете вступить в гильдию находясь в другой",reply_to_message_id=message.id)
                        else:
                            await bot.send_message(message.chat.id,"В гильдии нет свободных мест",reply_to_message_id=message.id)
                    case "По заявкам":
                        if int(guild[5])<int(guild[6]):
                            member=check_user_guild(message.from_user.id,message.chat.id)
                            if member==None:
                                owner_id=search_userid(guild[4])
                                owner=await bot.get_chat_member(message.chat.id,owner_id)
                                markup=types.InlineKeyboardMarkup()
                                btn1=types.InlineKeyboardButton(text='Одобрить',callback_data="req_approve")
                                btn2=types.InlineKeyboardButton(text='Отклонить',callback_data="req_reject")
                                markup.add(btn1,btn2)
                                join_request=await bot.send_message(message.chat.id,f"@{owner.user.username}. Пользователь [{message.from_user.first_name}](https://t.me/{message.from_user.username}) хочет присоединиться к вашей гильдии",parse_mode="Markdown",reply_markup=markup, disable_web_page_preview = True)
                                @bot.callback_query_handler(lambda call: call.data.startswith('req_'))
                                async def handle_callback(call):
                                    match call.data:
                                        case "req_approve":
                                            if call.from_user.id==owner_id:
                                               join_ex_guild(message.from_user.id,message.chat.id,name)
                                               await bot.delete_message(message.chat.id,join_request.id)
                                               await bot.send_message(message.chat.id,"Ваша заявка принята",reply_to_message_id=message.id)
                                        case "req_reject":
                                            if call.from_user.id==owner_id:
                                                await bot.delete_message(message.chat.id,join_request.id)
                                                await bot.send_message(message.chat.id,"Ваша заявка отклонена",reply_to_message_id=message.id)
                            else:
                                await bot.send_message(message.chat.id,"Вы не можете вступить в гильдию находясь в другой",reply_to_message_id=message.id)
                        else:
                            await bot.send_message(message.chat.id,"В гильдии нет свободных мест",reply_to_message_id=message.id)
                    case "Закрытый":
                        await bot.send_message(message.chat.id,"Тип гильдии закрытый. Обратитесь к владельцу гильдии для вступления",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Пригласить в гильдию|Invite in guild',chat_types=["supergroup","group"])
    async def invite_guild(message):
        match message.reply_to_message:
            case None:
                user=search_username(message.text.split()[3][1::],message.chat.id)
                member=check_user_guild(user,message.chat.id)
                guild_id=check_user_guild(message.from_user.id,message.chat.id)
                user1=search_user(message.from_user.id,message.chat.id)
                owner=search_owner(guild_id)
                if owner==user1:
                    if member==None:
                        new_member=await bot.get_chat_member(message.chat.id,user)
                        guild_name=search_info_guild(guild_id)[0][1]
                        markup=types.InlineKeyboardMarkup()
                        btn1=types.InlineKeyboardButton(text='Согласиться',callback_data="req_accept")
                        btn2=types.InlineKeyboardButton(text='Отказаться',callback_data="req_decline")
                        markup.add(btn1,btn2)
                        join_request=await bot.send_message(message.chat.id,f"@{new_member.user.username}. Пользователь [{message.from_user.first_name}](https://t.me/{message.from_user.username}) приглашает вас вступить в свою гильдию",parse_mode="Markdown",reply_markup=markup, disable_web_page_preview = True)
                        @bot.callback_query_handler(lambda call: call.data.startswith('req_'))
                        async def handle_callback(call):
                            match call.data:
                                case "req_accept":
                                    if call.from_user.id==user:
                                        join_ex_guild(user,message.chat.id,guild_name)
                                        await bot.delete_message(message.chat.id,join_request.id)
                                        await bot.send_message(message.chat.id,"Пользователь принял вашу заявку",reply_to_message_id=message.id)
                                case "req_decline":
                                    if call.from_user.id==user:
                                        await bot.delete_message(message.chat.id,join_request.id)
                                        await bot.send_message(message.chat.id,"Пользователь отказался от вашей заявки",reply_to_message_id=message.id)
                    else:
                        await bot.send_message(message.chat.id,"Данный пользователь уже состоит в другой гильдии",reply_to_message_id=message.id)
                else:
                    await bot.send_message(message.chat.id,"Вы не можете приглашать в гильдию не имея прав владельца",reply_to_message_id=message.id)
            case _:
                member=check_user_guild(message.reply_to_message.from_user.id,message.chat.id)
                user=search_user(message.from_user.id,message.chat.id)
                guild_id=check_user_guild(message.from_user.id,message.chat.id)
                owner=search_owner(guild_id)
                if owner==user:
                    if member==None:
                        guild_name=search_info_guild(guild_id)[0][1]
                        markup=types.InlineKeyboardMarkup()
                        btn1=types.InlineKeyboardButton(text='Согласиться',callback_data="req_accept")
                        btn2=types.InlineKeyboardButton(text='Отказаться',callback_data="req_decline")
                        markup.add(btn1,btn2)
                        join_request=await bot.send_message(message.chat.id,f"@{message.reply_to_message.from_user.username}. Пользователь [{message.from_user.first_name}](https://t.me/{message.from_user.username}) приглашает вас вступить в свою гильдию",parse_mode="Markdown",reply_markup=markup, disable_web_page_preview = True)
                        @bot.callback_query_handler(lambda call: call.data.startswith('req_'))
                        async def handle_callback(call):
                            match call.data:
                                case "req_accept":
                                    if call.from_user.id==message.reply_to_message.from_user.id:
                                        join_ex_guild(message.reply_to_message.from_user.id,message.chat.id,guild_name)
                                        await bot.delete_message(message.chat.id,join_request.id)
                                        await bot.send_message(message.chat.id,"Пользователь принял вашу заявку",reply_to_message_id=message.id)
                                case "req_decline":
                                    if call.from_user.id==message.reply_to_message.from_user.id:
                                        await bot.delete_message(message.chat.id,join_request.id)
                                        await bot.send_message(message.chat.id,"Пользователь отказался от вашей заявки",reply_to_message_id=message.id)
                    else:
                        await bot.send_message(message.chat.id,"Данный пользователь уже состоит в другой гильдии",reply_to_message_id=message.id)
                else:
                    await bot.send_message(message.chat.id,"Вы не можете приглашать в гильдию не имея прав владельца",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Создать гильдию|Create Guild',chat_types=["supergroup","group"])
    async def create_guild(message):
        name=""
        for i in message.text.split()[2:-1]:
            name+=i+" "
        guild=search_guild(name,message.chat.id)
        match guild:
            case None:
                match message.text.split()[-1].lower():
                    case "закрытый":
                        member=check_user_guild(message.from_user.id,message.chat.id)
                        if member==None:
                            type=message.text.split()[-1].lower()
                            create_new_guild(message.from_user.id,message.chat.id,name,type.capitalize())
                            await bot.send_message(message.chat.id,f"Гильдия {name} создана",reply_to_message_id=message.id)
                        else:
                            await bot.send_message(message.chat.id,"Вы не можете создать гильдию находясь в другой",reply_to_message_id=message.id)
                    case "открытый":
                        member=check_user_guild(message.from_user.id,message.chat.id)
                        if member==None:
                            type=message.text.split()[-1].lower()
                            create_new_guild(message.from_user.id,message.chat.id,name.capitalize(),type.capitalize())
                            await bot.send_message(message.chat.id,f"Гильдия {name} создана",reply_to_message_id=message.id)
                        else:
                            await bot.send_message(message.chat.id,"Вы не можете создать гильдию находясь в другой",reply_to_message_id=message.id)
                    case "заявки":
                        member=check_user_guild(message.from_user.id,message.chat.id)
                        if member==None:
                            create_new_guild(message.from_user.id,message.chat.id,name,"По заявкам")
                            await bot.send_message(message.chat.id,f"Гильдия {name} создана",reply_to_message_id=message.id)
                        else:
                            await bot.send_message(message.chat.id,"Вы не можете создать гильдию находясь в другой",reply_to_message_id=message.id)
                    case _:
                        await bot.send_message(message.chat.id,"Тип гильдии может быть только Открытый, Закрытый или Заявки",reply_to_message_id=message.id)
            case _:
                await bot.send_message(message.chat.id,"Вы не можете создать гильдию с чужим названием",reply_to_message_id=message.id)
                        
    @bot.message_handler(regexp='Покинуть гильдию|Leave guild',chat_types=["supergroup","group"])
    async def leave_guild(message):
        member=check_user_guild(message.from_user.id,message.chat.id)
        match member:
            case None:
                await bot.send_message(message.chat.id,"Вы не являетесь членом гильдии",reply_to_message_id=message.id)
            case _:
                user=search_user(message.from_user.id,message.chat.id)
                owner=search_owner(member)
                if user==owner:
                    await bot.send_message(message.chat.id,"Вы не покинуть гильдию являясь владельцем. Передайте права любому члену",reply_to_message_id=message.id)
                else:
                    leave_ex_guild(message.from_user.id,message.chat.id,member)
                    await bot.send_message(message.chat.id,"Вы покинули гильдию",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Передать права гильдии|Transfer rights guild',chat_types=["supergroup","group"])
    async def transfer_rights(message):
        match message.reply_to_message:
            case None:
                user=search_username(message.text.split()[3][1::],message.chat.id)
                member=check_user_guild(user,message.chat.id)
                member1=check_user_guild(message.from_user.id,message.chat.id)
                user1=search_user(message.from_user.id,message.chat.id)
                owner=search_owner(member1)
                if owner==user1:
                    if member1==member:
                        change_rights(search_user(user,message.chat.id),member)
                        await bot.send_message(message.chat.id,"Вы передали права на гильдию",reply_to_message_id=message.id)
                    else:
                        await bot.send_message(message.chat.id,"Вы не можете передать права на гильдию члену другой гильдии",reply_to_message_id=message.id)
                else:
                    await bot.send_message(message.chat.id,"Вы не можете передать права на гильдию в которой не являетесь владельцем",reply_to_message_id=message.id)
            case _:
                member=check_user_guild(message.reply_to_message.from_user.id,message.chat.id)
                member1=check_user_guild(message.from_user.id,message.chat.id)
                user=search_user(message.from_user.id,message.chat.id)
                owner=search_owner(member1)
                if owner==user:
                    if member1==member:
                        change_rights(search_user(message.reply_to_message.from_user.id,message.chat.id),member)
                        await bot.send_message(message.chat.id,"Вы передали права на гильдию",reply_to_message_id=message.id)
                    else:
                        await bot.send_message(message.chat.id,"Вы не можете передать права на гильдию члену другой гильдии",reply_to_message_id=message.id)
                else:
                    await bot.send_message(message.chat.id,"Вы не можете передать права на гильдию в которой не являетесь владельцем",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Моя гильдия|My Guild',chat_types=["supergroup","group"])
    async def info_guild(message):
        id_guild=check_user_guild(message.from_user.id,message.chat.id)
        if id_guild==None:
            await bot.send_message(message.chat.id,"Вы не можете просматривать информацию о гильдии пока не будете в ней состоять",reply_to_message_id=message.id)
        else:
            members=""
            guild=search_info_guild(id_guild)
            for i in guild[1]:
                user=await bot.get_chat_member(message.chat.id,i[1])
                if i[0]==guild[0][4]:
                    owner=f"[{user.user.first_name}](https://t.me/{user.user.username})"
                members+=f"[{user.user.first_name}](https://t.me/{user.user.username})\n"
                if guild[0][7]==None:
                    inv="Пусто"
                else:
                    inv=guild[0][7]
        await bot.send_message(message.chat.id,f"Информация о гильдии\nНазвание: {guild[0][1]}\nТип: {guild[0][2]}\nВладелец: {owner}\nУчастники:\n{members}Количество участников: {guild[0][5]}\nМаксимальное количество: {guild[0][6]}\nИнвентарь: {inv}",parse_mode='Markdown',disable_web_page_preview = True,reply_to_message_id=message.id)
    @bot.message_handler(regexp='Передать предмет гильдии|Transfer item guild',chat_types=["supergroup","group"])
    async def transfer_item_guild(message):
        items=check_items(str(message.text.split()[3]).lower())
        id_guild=check_user_guild(message.from_user.id,message.chat.id)
        match id_guild:
            case None:
                await bot.send_message(message.chat.id,"Вы не можете передавать вещи в гильдию пока не будете в ней состоять",reply_to_message_id=message.id)
            case _:
                user_inv=search_items(message.from_user.id,message.chat.id)
                if user_inv==None:
                    await bot.send_message(message.chat.id,"Вы не можете передавать вещи которых у вас нет",reply_to_message_id=message.id)
                else:
                    user_inv=str(user_inv).lower().split(",")
                    match re.search(",",items):
                        case None:
                            item=items.split(":")
                            for i in user_inv:
                                user_item=i.split(":")
                                if item[0]==user_item[0]:
                                    if int(item[1])>int(user_item[1]):
                                        await bot.send_message(message.chat.id,"Вы не можете передавать больше чем у вас есть",reply_to_message_id=message.id)
                                    else:
                                        add_guild_item(id_guild,item[0].capitalize(),int(item[1]))
                                        minus_user_item(message.from_user.id,message.chat.id,item[0].capitalize(),int(item[1]))
                                        await bot.send_message(message.chat.id,f"Вы передали в гильдию {item[0].capitalize()} в количестве {item[1]}",reply_to_message_id=message.id)
                        case _:
                            stop=False
                            transfer_items=""
                            items=items.split(",")
                            for i in items:
                                item=i.split(":")
                                for j in user_inv:
                                    user_item=j.split(":")
                                    if item[0]==user_item[0]:
                                        if int(item[1])>int(user_item[1]):
                                            await bot.send_message(message.chat.id,"Вы не можете передавать больше чем у вас есть",reply_to_message_id=message.id)
                                            stop=True
                                            break
                                        else:
                                            add_guild_item(id_guild,item[0].capitalize(),int(item[1]))
                                            minus_user_item(message.from_user.id,message.chat.id,item[0].capitalize(),int(item[1]))
                                            transfer_items+=f"{item[0].capitalize()} в количестве {item[1]}\n"
                                match stop:
                                    case True:
                                        break
                            match len(transfer_items):
                                case 0:
                                    pass
                                case _:
                                    await bot.send_message(message.chat.id,f"Вы передали в гильдию:\n{transfer_items}",reply_to_message_id=message.id)