import asyncio
import pygame, pickle
from game_player import Player

# 플레이어 객체를 이용하여 도형을 다시 그린다
def redrawWindow(win, player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

# 서버에 연결하고 플레이어 객체를 송수신하여 도형을 다시 그리는 무한 코루틴
async def conn_handler(run, host="localhost"):
    reader, writer = await asyncio.open_connection(host, 5555) #서버 연결
    pos = await reader.read(2048) # 자신의 플레이어 객체를 수신한다
    pos1 = pickle.loads(pos)
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        writer.write(pickle.dumps(pos1)) # 자신의 플레이어 객체를 전송한다
        await writer.drain()
        pos2 = await reader.read(2048) # 상대방 플레이어 객체를 수신한다

        # 윈도우 종료 버트(X)를 누르면 게임을 종료한다
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pos1.move() # 방향키에 따라 자신의 위치 수정
        pos2 = pickle.loads(pos2)
        redrawWindow(win, pos1, pos2) # 수정된 위치에 자신과 상대방의 도형을 다시 그린다

# 게임 화면 설정
width = 500
height = 500
win = pygame.display.set_mode((width, height))
name = input("Your name: ")
pygame.display.set_caption(name)

host = "localhost" # 서버 주소
run = True

asyncio.run(conn_handler(run, host))