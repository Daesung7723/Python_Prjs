import asyncio

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
        
    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()
    print("Complete\r")
    writer.close()

async def main():
    host = '127.0.0.1'
    port = 2500
    
    svr = await asyncio.start_server(handle_echo, host, port)
    print(f'{svr.sockets[0].getsockname()}에서 서비스 중')

    #async with svr:
    await svr.serve_forever()
        
asyncio.run(main())