from boot import add_money
def messages(bot):
    @bot.message_handler(chat_types=['supergroup','group'])
    async def mes(message):
        match message.content_type:
            case "text":
                if message.text=="/start@WoIlFbOt":
                    await bot.send_message(message.chat.id,'Бот успешно добавлен в группу. Задайте правила для группы с помощью команды "Задать правило <Правила>"\nДля ознакомления с функционалом используйте команду "Команды"',reply_to_message_id=message.id)
                elif message.text[0:7]=="/start":
                    pass
                elif message.from_user.first_name=="Telegram":
                    pass
                elif message.from_user.is_bot==True:
                    pass
                else:
                    add_money(message.from_user.id,message.chat.id,5)