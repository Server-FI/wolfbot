import asyncio
from telebot import types
from boot import *
from funcs import *
from datetime import datetime, timedelta
def coms(bot):
    @bot.message_handler(commands=['start'],chat_types=['private'])
    async def start(message):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://wolfbot.ru')
        btn2 = types.InlineKeyboardButton(text="Добавить бота",url="https://t.me/WoIlFbOt?startgroup=wolfbot&admin=change_info+restrict_members+delete_messages+pin_messages+invite_users")
        btn3 = types.InlineKeyboardButton(text="Команды")
        markup.add(btn1,btn2,btn3)
        sup=""
        for i in support():
            info=await bot.get_chat(i)
            if info.username==None:
                sup+=f"{info.first_name}\n"
            else:
                sup+=f"[{info.first_name}](https://t.me/{info.username})\n"
        await bot.send_message(message.chat.id,f"Помощь по работе бота wolfbot.\nТехническая поддержка:\n{sup}",reply_markup=markup, parse_mode='Markdown',disable_web_page_preview = True)
        @bot.callback_query_handler(lambda call: call.data.startswith('Команды'))
        async def handle_callback(call):
            match call.data:
                case "Команды":
                    await list_commands(message)
    @bot.message_handler(regexp="Кто я|I'm",chat_types=["supergroup","group"])
    async def info_user(message):
        match message.from_user.is_bot:
            case True:
                pass
            case False:
                info=search_info_user(message.from_user.id,message.chat.id)
                if info[5]==None:
                    guild="Не состоит"
                else:
                    guild=search_info_guild(info[5])[0][1]
                status=await bot.get_chat_member(message.chat.id,message.from_user.id)
                if info[6]==None:
                    inv="Пусто"
                else:
                    inv=info[6]
                if info[-1]==0:
                    vip="Нет"
                else:
                    vip="Есть"
                await bot.send_message(message.chat.id, f"Информация о пользователе {status.user.first_name}\nСтатус: {status.status}\nМонеты: {info[4]}\nКоличество предупреждений: {info[7]}\nГильдия: {guild}\nИнвентарь: {inv}\nVIP-статус: {vip}",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Кто админы|Admins',chat_types=["supergroup","group"])
    async def admins(message):
        admins_chat=""
        info=await bot.get_chat_administrators(message.chat.id)
        for i in info:
            if i.user.username==None:
                admins_chat+=f"{i.user.first_name}\n"
            else:
                admins_chat+=f"[{i.user.first_name}](https://t.me/{i.user.username})\n"
        await bot.send_message(message.chat.id, f"Список администраторов:\n{admins_chat}",parse_mode='Markdown', reply_to_message_id=message.id, disable_web_page_preview = True)
    @bot.message_handler(content_types=['new_chat_members'])
    async def nu(message):
        name=await bot.get_me()
        if name.id==message.json["new_chat_member"]["id"]:
            add_group(message.chat.id,message.chat.title)
        elif message.json["new_chat_member"]["is_bot"]==True:
            pass
        else:
            check=search_filter(message.from_user.id,message.from_user.username)
            if check==None:
                await bot.restrict_chat_member(message.chat.id,message.from_user.id, can_send_messages=False)
                markup = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton(text='Да',callback_data="Ответ_Да")
                btn2 = types.InlineKeyboardButton(text='Нет',callback_data="Ответ_Нет")
                markup.add(btn1,btn2)
                mes_test=await bot.send_message(message.chat.id, f"@{message.from_user.username}, Ты атеист? На ответ две минуты", reply_markup = markup, parse_mode='Markdown', disable_web_page_preview = True)
                time_test=datetime.now()+timedelta(minutes=2)
                answer=0
                while datetime.now()<time_test and answer==0:
                    @bot.callback_query_handler(lambda call: call.data.startswith('Ответ_'))
                    async def handle_callback(call):
                        global answer
                        info=await bot.get_chat(message.chat.id)
                        match call.data:
                            case 'Ответ_Да':
                                if call.from_user.id==message.from_user.id:
                                    answer=1
                                    await bot.restrict_chat_member(message.chat.id,message.from_user.id,permissions=info.permissions)
                                    role=await bot.get_chat_member(message.chat.id,message.from_user.id)
                                    add_user(message.from_user.id,message.from_user.username,message.chat.id,role)
                                    await bot.delete_message(message.chat.id, mes_test.message_id)
                                    await bot.delete_message(message.chat.id, message.id)
                            case 'Ответ_Нет':
                                if call.from_user.id==message.from_user.id:
                                    answer=1
                                    await bot.restrict_chat_member(message.chat.id,message.from_user.id,permissions=info.permissions)
                                    role=await bot.get_chat_member(message.chat.id,message.from_user.id)
                                    add_user(message.from_user.id,message.from_user.username,message.chat.id,role)
                                    await bot.delete_message(message.chat.id, mes_test.message_id)
                                    await bot.delete_message(message.chat.id, message.id)
                    await asyncio.sleep(10)
                if answer==0:
                    await bot.delete_message(message.chat.id, mes_test.message_id)
                    await bot.kick_chat_member(message.chat.id,message.from_user.id)
                    await bot.delete_message(message.chat.id, message.id)
                else:
                    pass
            else:
                await bot.ban_chat_member(message.chat.id,message.from_user.id)
                await bot.delete_message(message.chat.id, message.id)
    @bot.message_handler(regexp="Инвентарь|Items",chat_types=['supergroup','group'])
    async def invent(message):
        match message.from_user.is_bot:
            case True:
                pass
            case False:
                inv=search_items(message.from_user.id,message.chat.id)
                if inv==None:
                    await bot.send_message(message.chat.id,f"Инвентарь:\nНичего нет",reply_to_message_id=message.id)
                else:
                    inv=inv.replace(",","\n")
                    inv=inv.replace(":",". Количество: ")
                    await bot.send_message(message.chat.id,f"Инвентарь:\n{inv}",reply_to_message_id=message.id)
    @bot.message_handler(regexp="Магазин|Magazin",chat_types=['supergroup','group'])
    async def magazin(message):
        match message.from_user.is_bot:
            case True:
                pass
            case False:
                mag=search_magazin()
                if mag==None or str(mag)=="[]":
                    await bot.send_message(message.chat.id,f"Ассортимент магазина:\nВсё разобрали",reply_to_message_id=message.id)
                else:
                    assort=""
                    for i in mag:
                        assort+=f"{i[1]}. Количество: {i[2]}/{i[3]}. Цена: {i[4]} монет\n"
                    await bot.send_message(message.chat.id,f"Ассортимент магазина:\n{assort}",reply_to_message_id=message.id)
    @bot.message_handler(regexp="Купить предмет|Buy item",chat_types=['supergroup','group'])
    async def buy_item(message):
        match message.from_user.is_bot:
            case True:
                pass
            case False:
                item=""
                for i in message.text.split()[2:-1]:
                    item+=i+""
                item=item.capitalize()
                sell_count=search_item(item)
                match sell_count:
                    case None:
                        await bot.send_message(message.chat.id,f"Данного товара нет в магазине",reply_to_message_id=message.id)
                    case _:
                        count=int(message.text.split()[-1])
                        if count>int(sell_count[2]):
                            await bot.send_message(message.chat.id,f"Вы не можете купить больше остатка",reply_to_message_id=message.id)
                        elif count==0:
                            await bot.send_message(message.chat.id,f"Вы не можете купить 0 единиц товара",reply_to_message_id=message.id)
                        else:
                            money=search_money(message.from_user.id,message.chat.id)
                            if money>=count*int(sell_count[4]):
                                minus_money(message.from_user.id,message.chat.id,count*int(sell_count[4]))
                                minus_item(item,count)
                                add_item(message.from_user.id,message.chat.id,item,count)
                                await bot.send_message(message.chat.id,f"Вы успешно купили {item} в количестве {count} за {count*int(sell_count[4])} монет",reply_to_message_id=message.id)
                            else:
                                await bot.send_message(message.chat.id,f"У вас недостаточно монет для покупки",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Передать предмет|Transfer item',chat_types=["supergroup","group"])
    async def transfer_item(message):
        match message.from_user.is_bot:
            case True:
                pass
            case False:
                match message.reply_to_message:
                    case None:
                        items=check_items(str(message.text.split()[3]).lower())
                        user=search_username(message.text.split()[2][1::],message.chat.id)
                    case _:
                        items=check_items(str(message.text.split()[2]).lower())
                        user=message.reply_to_message.from_user.id
                user_inv=search_items(message.from_user.id,message.chat.id)
                if user_inv==None:
                    await bot.send_message(message.chat.id,"Вы не можете передавать вещи которых у вас нет",reply_to_message_id=message.id)
                else:
                    user_inv=str(user_inv).lower().split(",")
                    match re.search(",",items):
                        case None:
                            item=items.split(":")
                            match re.search(item[0],user_inv):
                                case None:
                                    await bot.send_message(message.chat.id,f"У вас в инвентаре нет {item[0].capitalize()}",reply_to_message_id=message.id)
                                case _:
                                    for i in user_inv:
                                        user_item=i.split(":")
                                        if item[0]==user_item[0]:
                                            if int(item[1])>int(user_item[1]):
                                                await bot.send_message(message.chat.id,"Вы не можете передавать больше чем у вас есть",reply_to_message_id=message.id)
                                            else:
                                                add_item(user,message.chat.id,item[0].capitalize(),int(item[1]))
                                                minus_user_item(message.from_user.id,message.chat.id,item[0].capitalize(),int(item[1]))
                                                await bot.send_message(message.chat.id,f"Вы передали пользователю {item[0].capitalize()} в количестве {item[1]}",reply_to_message_id=message.id)
                        case _:
                            stop=False
                            transfer_items=""
                            items=items.split(",")
                            for i in items:
                                item=i.split(":")
                                for j in user_inv:
                                    user_item=j.split(":")
                                    match re.search(item[0],user_inv):
                                        case None:
                                            await bot.send_message(message.chat.id,f"У вас в инвентаре нет {item[0].capitalize()}",reply_to_message_id=message.id)
                                            stop=True
                                            break
                                        case _:
                                            if item[0]==user_item[0]:
                                                if int(item[1])>int(user_item[1]):
                                                    await bot.send_message(message.chat.id,"Вы не можете передавать больше чем у вас есть",reply_to_message_id=message.id)
                                                    stop=True
                                                    break
                                                else:
                                                    add_item(user,message.chat.id,item[0].capitalize(),int(item[1]))
                                                    minus_user_item(message.from_user.id,message.chat.id,item[0].capitalize(),int(item[1]))
                                                    transfer_items+=f"{item[0].capitalize()} в количестве {item[1]}\n"
                                match stop:
                                    case True:
                                        break
                            match len(transfer_items):
                                case 0:
                                    pass
                                case _:
                                    await bot.send_message(message.chat.id,f"Вы передали пользователю:\n{transfer_items}",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Команды|Commands')
    async def list_commands(message):
        if message.from_user.first_name=="Telegram":
            pass
        else:
            markup_list=types.InlineKeyboardMarkup()
            btn_list1=types.InlineKeyboardButton(text="Основные",callback_data="Команды_Основые")
            btn_list2=types.InlineKeyboardButton(text="Модераторские",callback_data="Команды_Модераторские")
            btn_list3=types.InlineKeyboardButton(text="Гильдийские",callback_data="Команды_Гильдийские")
            btn_list4=types.InlineKeyboardButton(text="Выйти",callback_data="Команды_Выйти")
            markup_list.add(btn_list1,btn_list2,btn_list3,btn_list4)
            list_com="Список всех команд:\n<b><u>Основные</u></b> - команды, которые доступны всем\n<b><u>Модераторские</u></b> - команды для модерации группы\n<b><u>Гильдийские</u></b> - команды, отвечающие за гильдии"
            mes=await bot.send_message(message.chat.id,list_com,parse_mode="HTML",reply_markup=markup_list,reply_to_message_id=message.id)
            @bot.callback_query_handler(lambda call: call.data.startswith('Команды_'))
            async def handle_callback(call):
                match call.data:
                    case "Команды_Основые":
                        if call.from_user.id==message.from_user.id:
                            main="<b><u>Основные:</u></b>\nКто я(I'm) - информация о пользователе использовавшем данную команду\nКто админы(Admins) - выводит список администраторов чата\nИнвентарь(Items) - выводит инвентарь пользователя использовавшего данную команду\n"
                            main1="Магазин(Magazin) - показывает ассортимент магазина\nКупить предмет <u>название</u> <u>количество</u>(Buy item <u>название</u> <u>количество</u>) - купить предмет в магазине\n"
                            main2="Передать предмет <u>юзернейм или ответ на сообщение</u> <u>название</u>:<u>количество</u>(Transfer item <u>юзернейм или ответ на сообщение</u> <u>название</u>:<u>количество</u>) - передача предмета(-ов) из инвентаря другому пользователю. Если хотите передать больше одного предмета, то указывайте передаваемые предметы следующим образом: <u>Название</u>:<u>количество</u>,<u>Название</u>:<u>количество</u>\n"
                            main3="Правила(Rules) - выводит правила чата\nПромокод <u>промокод</u>(Promocode <u>промокод</u>) - выдаёт награду указанную для промокода. Для использования более одного промокода надо писать их через запятую. Пример: Промокод <u>промокод1,промокод2</u>\n"
                            markup_main=types.InlineKeyboardMarkup()
                            btn_main1=types.InlineKeyboardButton(text="Назад",callback_data="Команды_Назад")
                            markup_main.add(btn_main1)
                            await bot.edit_message_text(main+main1+main2+main3,message.chat.id,mes.id,reply_markup=markup_main,parse_mode="HTML")
                        else:
                            pass
                    case "Команды_Модераторские":
                        if call.from_user.id==message.from_user.id:
                            mod="<b><u>Модераторские:</u></b>\nВарны <u>юзернейм или ответ на сообщение</u>(Warns <u>юзернейм или ответ на сообщение</u>) - выводит количество варнов пользователя. Если хотите просмотреть количесто своих варнов, то просто напишите команду без ответа и юзернейма\n"
                            mod1="Бан <u>юзернейм или ответ на сообщение</u>(Ban <u>юзернейм или ответ на сообщение</u>) - забанить пользователя в чате. Для бана по причине спама указывать причину в которой будет использовано слово 'бот'\n"
                            mod2="Мут <u>юзернейм или ответ на сообщение</u> <u>время в с/s или м/m или ч/h</u>(Mute <u>юзернейм или ответ на сообщение</u> <u>время в с/s или м/m или ч/h</u>) - замутить пользователя на определённое время\n"
                            mod3="Варн <u>юзернейм или ответ на сообщение</u>(Warn <u>юзернейм или ответ на сообщение</u>) - выдать предупреждение пользователю\nИзменить максимум <u>новое количество</u>(Change warns <u>новое количество</u>) - изменить максимум предупреждений необходимый для бана\n"
                            mod4="Задать правило <u>каждая строка и пункт правила писать на следующей строке</u>(Settings Rule <u>каждую строку и пункт правила писать на следующей строке</u>) - задаёт правила для чата\n"
                            mod5="Добавить правило  <u>новые правила без нумерации</u>(Add Rule  <u>новые правила без нумерации</u>) - добавляет новые пункты в правила чата. Для корректного внесения обязателен двойной пробел между командой и добавляемыми пунктами. Если добавляете больше одного пункта, то ставьте запятые между пунктами\nУдалить правило <u>номера пунктов</u>(Remove Rule <u>номера пунктов</u>) - удаляет пункты в правилах чата. Если удаляете больше одного пункта, то ставьте запятые между номерами\n"
                            mod6="Снять запрет <u>юзернейм или ответ на сообщение</u>(Remove zapret <u>юзернейм или ответ на сообщение</u>) - снять мут с пользователя\nСнять предупреждение <u>юзернейм или ответ на сообщение</u>(Remove wurn <u>юзернейм или ответ на сообщение</u>) - снять варн с пользователя\nСнять блокировку <u>юзернейм или ответ на сообщение</u>(Remove block <u>юзернейм или ответ на сообщение</u>) - снять бан с пользователя(если пользователь добавлен в фильтр, то обращайтесь в поддержку бота)\n"
                            #mod7="Журнал <u>юзернейм или ответ на сообщение</u> (Journal <u>юзернейм или ответ на сообщение</u>) - выводит журнал со всеми наказаниями в данной группе. Если хотите просмотреть свой журнал,то просто напишите команду без ответа и юзернейма\n"
                            markup_mod=types.InlineKeyboardMarkup()
                            btn_mod1=types.InlineKeyboardButton(text="Назад",callback_data="Команды_Назад")
                            markup_mod.add(btn_mod1)
                            await bot.edit_message_text(mod+mod1+mod2+mod3+mod4+mod5+mod6,message.chat.id,mes.id,reply_markup=markup_mod,parse_mode="HTML")
                        else:
                            pass
                    case "Команды_Гильдийские":
                        if call.from_user.id==message.from_user.id:
                            gu="<b><u>Гильдийские:</u></b>\nСписок гильдий(Guilds) - показывает список гильдий созданных в группе\nПрисоединиться к гильдии <u>название</u> (Join the guild <u>название</u>) - присоединиться к гильдии\n"
                            gu1="Пригласить в гильдию <u>юзернейм или ответ на сообщение</u>(Invite in guild <u>юзернейм или ответ на сообщение</u>) - пригласить участника чата в гильдию. Доступно владельцу гильдии\n"
                            gu2="Создать гильдию <u>название</u> <u>тип гильдии</u>(Create Guild <u>название</u> <u>тип гильдии</u>) - создать гильдию в группе. Доступны типы: закрытый, открытый, заявки\n"
                            gu3="Покинуть гильдию(Leave guild) - выйти из гильдии\nПередать права гильдии <u>юзернейм или ответ на сообщение</u>(Transfer rights guild <u>юзернейм или ответ на сообщение</u>) - передать права участнику гильдии. Доступно владельцу гильдии\n"
                            gu4="Моя гильдия(My Guild) - выводит информацию о гильдии в которой состоит пользователь\nПередать предмет гильдии <u>название</u>:<u>количество</u>(Transfer item guild <u>название</u>:<u>количество</u>) - передача предмета(-ов) в гильдию. Если хотите передать больше одного предмета, то указывайте передаваемые предметы следующим образом: <u>Название</u>:<u>количество</u>,<u>Название</u>:<u>количество</u>\n"
                            gu5="Удалить гильдию(Delete Guild) - удалить гильдию"
                            markup_gu=types.InlineKeyboardMarkup()
                            btn_gu1=types.InlineKeyboardButton(text="Назад",callback_data="Команды_Назад")
                            markup_gu.add(btn_gu1)
                            await bot.edit_message_text(gu+gu1+gu2+gu3+gu4+gu5,message.chat.id,mes.id,reply_markup=markup_gu,parse_mode="HTML")
                        else:
                            pass
                    case "Команды_Назад":
                        if call.from_user.id==message.from_user.id:
                            await bot.edit_message_text(list_com,message.chat.id,mes.id,reply_markup=markup_list,parse_mode="HTML")
                        else:
                            pass
                    case "Команды_Выйти":
                        if call.from_user.id==message.from_user.id:
                            await bot.delete_messages(message.chat.id,[mes.id,message.id])
                        else:
                            pass
    @bot.message_handler(regexp='Правила|Rules',chat_types=['supergroup','group'])
    async def rules(message):
        if message.from_user.first_name=="Telegram":
            pass
        else:
            rules=group_rules(message.chat.id)
            match rules:
                case None:
                    await bot.send_message(message.chat.id,"Правила чата отсутствуют",reply_to_message_id=message.id)
                case _:
                    rules=rules.replace("|","\n")
                    await bot.send_message(message.chat.id,f"Правила чата:\n{rules}",reply_to_message_id=message.id)
    @bot.message_handler(regexp='Промокод|Promocode',chat_types=["private"])
    async def use_promocode(message):
        author_mes=message.id
        promos=message.text.split(" ")[1]
        match re.search(",",promos):
            case None:
                res=search_promocode(promos)
                if res==None:
                    await bot.send_message(message.chat.id,"Данный промокод уже был использован",reply_to_message_id=message.id)
                else:
                    if len(res)==1 or len(res)==3:
                        match res[1]:
                            case True:
                                groups=search_guid(message.from_user.id)
                                groups_split=groups.split("\n")
                                markup=types.InlineKeyboardMarkup()
                                if len(groups_split)==1:
                                    btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                    markup.add(btn1)
                                    mes=await bot.send_message(message.chat.id,f"Вы получили {res[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                    @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                    async def handle_callback(call):
                                        match call.data:
                                            case btn1.callback_data:
                                                add_money(message.from_user.id,groups_split[0].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                elif len(groups_split)==2:
                                    btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                    btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                                    markup.add(btn1,btn2)
                                    mes=await bot.send_message(message.chat.id,f"Вы получили {res[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                    @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                    async def handle_callback(call):
                                        match call.data:
                                            case btn1.callback_data:
                                                add_money(message.from_user.id,groups_split[0].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                            case btn2.callback_data:
                                                add_money(message.from_user.id,groups_split[1].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[1].split(" ")[0]}")
                                elif len(groups_split)==3:
                                    btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                    btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                                    btn3=types.InlineKeyboardButton(text=groups_split[2].split(" ")[0],callback_data=f"Деньги_{groups_split[2].split(" ")[0]}")
                                    markup.add(btn1,btn2,btn3)
                                    mes=await bot.send_message(message.chat.id,f"Вы получили {res[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                    @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                    async def handle_callback(call):
                                        match call.data:
                                            case btn1.callback_data:
                                                add_money(message.from_user.id,groups_split[0].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                            case btn2.callback_data:
                                                add_money(message.from_user.id,groups_split[1].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[1].split(" ")[0]}")
                                            case btn3.callback_data:
                                                add_money(message.from_user.id,groups_split[2].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[2].split(" ")[0]}")
                                else:
                                    btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                    btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                                    btn3=types.InlineKeyboardButton(text=groups_split[2].split(" ")[0],callback_data=f"Деньги_{groups_split[2].split(" ")[0]}")
                                    btn4=types.InlineKeyboardButton(text="Другая",callback_data="Деньги_Другая")
                                    markup.add(btn1,btn2,btn3,btn4)
                                    mes=await bot.send_message(message.chat.id,f"Вы получили {res[2]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                    @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                    async def handle_callback(call):
                                        match call.data:
                                            case btn1.callback_data:
                                                add_money(message.from_user.id,groups_split[0].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                            case btn2.callback_data:
                                                add_money(message.from_user.id,groups_split[1].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[1].split(" ")[0]}")
                                            case btn3.callback_data:
                                                add_money(message.from_user.id,groups_split[2].split(" ")[0],res[2])
                                                await bot.delete_message(message.chat.id,mes.id)
                                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {groups_split[2].split(" ")[0]}")
                                            case btn4.callback_data:
                                                await bot.edit_message_text("Введите номер группы в которую зачислите монеты",message.chat.id,mes.id)
                                                @bot.message_handler(chat_types=['private'])
                                                async def another_group(message):
                                                    add_money(message.from_user.id,message.text,res[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=author_mes)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]} на счёт в группе {message.text}")
                            case False:
                                update_vip(message.from_user.id,res[2])
                                await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0]}",reply_to_message_id=message.id)
                                write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {res[0]}")
                    else:
                        for i in res:
                            match i[1]:
                                case True:
                                    groups=search_guid(message.from_user.id)
                                    groups_split=groups.split("\n")
                                    markup=types.InlineKeyboardMarkup()
                                    if len(groups_split)==1:
                                        btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                        markup.add(btn1)
                                        mes=await bot.send_message(message.chat.id,f"Вы получили {i[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                        @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                        async def handle_callback(call):
                                            match call.data:
                                                case btn1.callback_data:
                                                    add_money(message.from_user.id,groups_split[0].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                    elif len(groups_split)==2:
                                        btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                        btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                                        markup.add(btn1,btn2)
                                        mes=await bot.send_message(message.chat.id,f"Вы получили {i[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                        @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                        async def handle_callback(call):
                                            match call.data:
                                                case btn1.callback_data:
                                                    add_money(message.from_user.id,groups_split[0].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                                case btn2.callback_data:
                                                    add_money(message.from_user.id,groups_split[1].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[1].split(" ")[0]}")
                                    elif len(groups_split)==3:
                                        btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                        btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                                        btn3=types.InlineKeyboardButton(text=groups_split[2].split(" ")[0],callback_data=f"Деньги_{groups_split[2].split(" ")[0]}")
                                        markup.add(btn1,btn2,btn3)
                                        mes=await bot.send_message(message.chat.id,f"Вы получили {i[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                        @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                        async def handle_callback(call):
                                            match call.data:
                                                case btn1.callback_data:
                                                    add_money(message.from_user.id,groups_split[0].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                                case btn2.callback_data:
                                                    add_money(message.from_user.id,groups_split[1].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[1].split(" ")[0]}")
                                                case btn3.callback_data:
                                                    add_money(message.from_user.id,groups_split[2].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[2].split(" ")[0]}")
                                    else:
                                        btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                                        btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                                        btn3=types.InlineKeyboardButton(text=groups_split[2].split(" ")[0],callback_data=f"Деньги_{groups_split[2].split(" ")[0]}")
                                        btn4=types.InlineKeyboardButton(text="Другая",callback_data="Деньги_Другая")
                                        markup.add(btn1,btn2,btn3,btn4)
                                        mes=await bot.send_message(message.chat.id,f"Вы получили {i[0]}. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                                        @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                                        async def handle_callback(call):
                                            match call.data:
                                                case btn1.callback_data:
                                                    add_money(message.from_user.id,groups_split[0].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[0].split(" ")[0]}")
                                                case btn2.callback_data:
                                                    add_money(message.from_user.id,groups_split[1].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[1].split(" ")[0]}")
                                                case btn3.callback_data:
                                                    add_money(message.from_user.id,groups_split[2].split(" ")[0],i[2])
                                                    await bot.delete_message(message.chat.id,mes.id)
                                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {groups_split[2].split(" ")[0]}")
                                                case btn4.callback_data:
                                                    await bot.edit_message_text("Введите номер группы в которую зачислите монеты",message.chat.id,mes.id)
                                                    @bot.message_handler(chat_types=['private'])
                                                    async def another_group(message):
                                                        add_money(message.from_user.id,message.text,i[2])
                                                        await bot.delete_message(message.chat.id,mes.id)
                                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]} на счёт в группе {message.text}")
                                case False:
                                    update_vip(message.from_user.id,i[2])
                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {promos} и получил {i[0]}")
                        await bot.send_message(message.chat.id,f"Вы успешно активировали промокод {promos} и получили {res[0][0]},{res[1][0]}",reply_to_message_id=message.id)
            case _:
                use_promos=""
                money=0
                for i in promos.split(","):
                    res=search_promocode(i)
                    if res==None:
                        use_promos+=f"Промокод {i} уже был использован\n"
                    else:
                        if len(res)==1 or len(res)==3:
                            match res[1]:
                                case True:
                                    money+=int(res[2])
                                    use_promos+=f"Вы успешно активировали промокод {i} и получили {res[0]}\n"
                                case False:
                                    update_vip(message.from_user.id,res[2])
                                    use_promos+=f"Вы успешно активировали промокод {i} и получили {res[0]}\n"
                                    write_log(f"Пользователь под id {message.from_user.id} активировал промокод {i} и получил {res[0]}")
                        else:
                            for j in res:
                                match j[1]:
                                    case True:
                                        money+=int(j[2])
                                        use_promos+=f"Вы успешно активировали промокод {i} и получили {j[0]}\n"
                                    case False:
                                        update_vip(message.from_user.id,j[2])
                                        use_promos+=f"Вы успешно активировали промокод {i} и получили {j[0]}\n"
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокод {i} и получил {j[0]}")
                match money:
                    case 0:
                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                    case _:
                        groups=search_guid(message.from_user.id)
                        groups_split=groups.split("\n")
                        markup=types.InlineKeyboardMarkup()
                        if len(groups_split)==1:
                            btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                            markup.add(btn1)
                            mes=await bot.send_message(message.chat.id,f"Вы получили {money} монет. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                            @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                            async def handle_callback(call):
                                match call.data:
                                    case btn1.callback_data:
                                        add_money(message.from_user.id,groups_split[0].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[0].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                        elif len(groups_split)==2:
                            btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                            btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                            markup.add(btn1,btn2)
                            mes=await bot.send_message(message.chat.id,f"Вы получили {money} монет. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                            @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                            async def handle_callback(call):
                                match call.data:
                                    case btn1.callback_data:
                                        add_money(message.from_user.id,groups_split[0].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[0].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                                    case btn2.callback_data:
                                        add_money(message.from_user.id,groups_split[1].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[1].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                        elif len(groups_split)==3:
                            btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                            btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                            btn3=types.InlineKeyboardButton(text=groups_split[2].split(" ")[0],callback_data=f"Деньги_{groups_split[2].split(" ")[0]}")
                            markup.add(btn1,btn2,btn3)
                            mes=await bot.send_message(message.chat.id,f"Вы получили {money} монет. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                            @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                            async def handle_callback(call):
                                match call.data:
                                    case btn1.callback_data:
                                        add_money(message.from_user.id,groups_split[0].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[0].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                                    case btn2.callback_data:
                                        add_money(message.from_user.id,groups_split[1].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[1].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                                    case btn3.callback_data:
                                        add_money(message.from_user.id,groups_split[2].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[2].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                        else:
                            btn1=types.InlineKeyboardButton(text=groups_split[0].split(" ")[0],callback_data=f"Деньги_{groups_split[0].split(" ")[0]}")
                            btn2=types.InlineKeyboardButton(text=groups_split[1].split(" ")[0],callback_data=f"Деньги_{groups_split[1].split(" ")[0]}")
                            btn3=types.InlineKeyboardButton(text=groups_split[2].split(" ")[0],callback_data=f"Деньги_{groups_split[2].split(" ")[0]}")
                            btn4=types.InlineKeyboardButton(text="Другая",callback_data="Деньги_Другая")
                            markup.add(btn1,btn2,btn3,btn4)
                            mes=await bot.send_message(message.chat.id,f"Вы получили {money} монет. Выберите группу в которую будет зачислена награда:\n{groups}",reply_markup=markup,reply_to_message_id=message.id)
                            @bot.callback_query_handler(lambda call: call.data.startswith('Деньги_'))
                            async def handle_callback(call):
                                match call.data:
                                    case btn1.callback_data:
                                        add_money(message.from_user.id,groups_split[0].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[0].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                                    case btn2.callback_data:
                                        add_money(message.from_user.id,groups_split[1].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[1].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                                    case btn3.callback_data:
                                        add_money(message.from_user.id,groups_split[2].split(" ")[0],money)
                                        await bot.delete_message(message.chat.id,mes.id)
                                        write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {groups_split[2].split(" ")[0]}")
                                        await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)
                                    case btn4.callback_data:
                                        await bot.edit_message_text("Введите номер группы в которую зачислите монеты",message.chat.id,mes.id)
                                        @bot.message_handler(chat_types=['private'])
                                        async def another_group(message):
                                            add_money(message.from_user.id,message.text,money)
                                            await bot.delete_message(message.chat.id,mes.id)
                                            write_log(f"Пользователь под id {message.from_user.id} активировал промокоды {promos} и получил {money} монет на счёт в группе {message.text}")
                                            await bot.send_message(message.chat.id,use_promos,reply_to_message_id=message.id)