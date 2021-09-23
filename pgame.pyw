import pygame
import sys
import random


White = (255,255,255) 
score = 0
highscore = 100

hato = []
check = []
for i in range(10):
    hato.append([0,0,0,0,0,0,0,0])
    check.append([0,0,0,0,0,0,0,0])

def dis_hato():
    screen.blit(bg,[0,0])
    for y in range(10):
        for x in range(8):
            if hato[y][x]>0:
                screen.blit(img_hato[hato[y][x]],[x*60+62,y*60+77])

def drop_hato():
    flag = False
    for y in range(8,-1,-1):
        for x in range(8):
            if hato[y][x] != 0 and hato[y+1][x] == 0:
                hato[y+1][x] = hato[y][x]
                hato[y][x] = 0
                flag = True
    return flag

def check_hato():
    for y in range(10):
        for x in range(8):
            check[y][x] = hato[y][x]

#縦
    for y in range(1,9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    hato[y-1][x] = 5
                    hato[y][x] = 5
                    hato[y+1][x] = 5
#横
    for y in range(10):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    hato[y][x-1] = 5  
                    hato[y][x] = 5
                    hato[y][x+1] = 5
#斜め/
    for y in range(1,9):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    hato[y+1][x-1] = 5  
                    hato[y][x] = 5
                    hato[y-1][x+1] = 5
#斜め\
                if check[y+1][x+1] == check[y][x] and check[y-1][x-1] == check[y][x]:
                    hato[y+1][x+1] = 5  
                    hato[y][x] = 5
                    hato[y-1][x-1] = 5         


#揃ったら消す
def delete_hato():
    num = 0
    for y in range(10):
        for x in range(8):
            if hato[y][x] == 5:
                hato[y][x] = 0
                num += 1
    return num

#ハートが最上位をこえる
def over_hato():
    for x in range(8):
        if hato[0][x]>0:
            return True
    return False

#最上位にハートセット
def set_hato():
    for x in range(8):
        hato[0][x] = random.randint(0,4)

#スコア
def dis_score():
    global score,highscore
    txt = font.render(str(score),True,White)
    screen.blit(txt,[630,294])
    txt2 = font.render(str(highscore),True,White)
    screen.blit(txt2,[630,388])




#ゲームメイン処理
def main():
    cursor_x=0
    cursor_y=0
    global score,highscore

    state = 0
    next_hato = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        mouse_x,mouse_y = pygame.mouse.get_pos() #マウスの位置を取得
        mouse_click = pygame.mouse.get_pressed()
        mouse_c = mouse_click[0] #左クリック状態をリスト0へ

        #state0
        if state==0:
            screen.blit(bg,[0,0])
            screen.blit(title,[62,70])
            
            screen.blit(click_start,[60,70])
            state = 1
            mouse_c = False

        #state1
        elif state==1:
            if mouse_c == True:
                for y in range(10):
                    for x in range(8):
                        hato[y][x] = 0
                        se2.play()
                mouse_c = False
                score = 0
                next_hato = 0
                cursor_x = 0
                cursor_y = 0
                set_hato()
                state = 2
                
           
        #state2
        elif state == 2:
            if drop_hato() == False:
                state = 3
            dis_hato()

        #state3
        elif state == 3:
            check_hato()
            state = 4
            dis_hato()

        #state4
        elif state == 4:
            q = delete_hato()
            score = score + q*1
            if score > highscore:
                highscore = score
            if q > 0:
                state = 2
                se1.play()
            else:
                if over_hato() == False:
                    next_hato = random.randint(1,4)
                    state = 5
                else:
                    state = 6
            dis_hato()


        #state5
        elif state == 5:
            if 62 <= mouse_x and mouse_x < 62+60*8 and 78 <= mouse_y and mouse_y < 78+60*10:
                cursor_x = int((mouse_x-62)/60) #マス上の位置に変換
                cursor_y = int((mouse_y-78)/60)
                if mouse_c == True and hato[cursor_y][cursor_x] == 0:
                    mouse_c = False
                    set_hato()
                    hato[cursor_y][cursor_x] = next_hato
                    next_hato = 0
                    state = 2
            dis_hato()
            screen.blit(cursor,[cursor_x*60+62,cursor_y*60+78])   #カーソル表示

         #state6
        elif state==6:
            screen.blit(game_over,[60,70]) #ゲームオーバー画面
            se3.play()
            
            if mouse_c == True:
                 state = 0

        dis_score()    #スコア表示        
        
        if next_hato > 0: #次のハート表示
            screen.blit(img_hato[next_hato],[642,119])

        pygame.display.update()
        clock.tick(10)        



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('pgame')
    screen = pygame.display.set_mode((800,750))
    font = pygame.font.Font(None,40)
    clock = pygame.time.Clock()
  

    bg = pygame.image.load('background.png')
    cursor = pygame.image.load('cursor2.png')
    img_hato = [
        None,
        pygame.image.load('yellow.png'),
        pygame.image.load('red.png'),
        pygame.image.load('green.png'),
        pygame.image.load('brue.png'),
        pygame.image.load("kuro.png")
    ]
    title = pygame.image.load('lole2.png')
    click_start = pygame.image.load('click.png')
    game_over = pygame.image.load('over.png')

    try:
        pygame.mixer.music.load('lost love.mp3')
        se1 = pygame.mixer.Sound('next.mp3')
        se2 = pygame.mixer.Sound('mizu.mp3')
        se3 = pygame.mixer.Sound('negative.mp3')
    except:
        print("ファイルなし")
    pygame.mixer.music.play(-1)
    
    main() #ゲームメイン処理

