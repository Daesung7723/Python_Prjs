#asyncio_tco_echo_server.py
import asyncio

async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))
            
        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()
        #print("Close the client socket")
        #writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 2500, loop=loop) #client가 연결되면

task = loop.create_task(coro)

print('Serving...')
loop.run_forever()
