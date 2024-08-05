import asyncio
import telegram
token = '7071117312:AAGswfTHRzbsZTuRCE7nI9-2rSLhbLGq_MA'
chat_id = '7388700699'
message = 'Hello Lao.'

async def main():
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text=message, chat_id=chat_id)

if __name__ == '__main__':
    asyncio.run(main())
