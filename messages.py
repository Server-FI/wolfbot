from boot import add_money
def messages(bot):
    @bot.message_handler(chat_types=['supergroup','group'])
    async def mes(message):
        if message.text[0:7]!="/start@":
            add_money(message.from_user.id,message.chat.id)