import asyncio
import telegram
token = 1 
chat_id = 2
message = 'Hello Lao.'

async def main():
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text=message, chat_id=chat_id)

if __name__ == '__main__':
    asyncio.run(main())
