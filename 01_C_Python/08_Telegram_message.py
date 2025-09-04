import asyncio
import telegram
# token = 
# chat_id = 
message = 'Hello Lao.'

async def main():
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text=message, chat_id=chat_id)

if __name__ == '__main__':
    asyncio.run(main())
