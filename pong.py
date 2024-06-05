import pygame
from time import sleep
import os
import sys
import json

pygame.init()

szerokosc = 950
wysokosc = 500
window = pygame.display.set_mode((szerokosc, wysokosc))
bc = pygame.transform.scale(pygame.image.load("background.png"), (szerokosc, wysokosc))
ico = pygame.image.load(os.path.join("IKONA.png"))

pygame.display.set_caption("Pong")
pygame.display.set_icon(ico)


class Button:
    def __init__(self, x_cord, y_cord, file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.hovered_button_image = pygame.image.load(f"{file_name}_hovered.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self, window):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.hovered_button_image, (self.x_cord, self.y_cord))
        else:
            window.blit(self.button_image, (self.x_cord, self.y_cord))


def main():
    main_run = True
    clock = 0
    btn_exit = Button((szerokosc / 2) - (pygame.image.load("btn_play.png").get_width() / 2), (wysokosc / 2) - (pygame.image.load("btn_play.png").get_height() / 2) , "btn_exit")
    btn_play = Button((szerokosc / 2) - (pygame.image.load("btn_play.png").get_width() / 2), (wysokosc / 2) - (pygame.image.load("btn_play.png").get_height() / 2) - 100, "btn_play")
    while main_run:
        clock += pygame.time.Clock().tick(30) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT or btn_exit.tick():
                sys.exit()
            if btn_play.tick():
                Game()
        
        window.blit(bc, (0,0))
        btn_play.draw(window)
        btn_exit.draw(window)
        pygame.display.update()


def napisz(tekst, x, y, rozmiar, end=False):
    cz = pygame.font.SysFont("Arial", rozmiar)
    if end:
        rend = cz.render(tekst, 1, (255, 0, 0))
    else:
        rend = cz.render(tekst, 1, (255, 255, 100))
    window.blit(rend, (x,y))

def gameover(punkty_1, punkty_2):
    window.fill((0,0,0))
    napisz("GAME OVER", szerokosc // 2 - 300, wysokosc // 2 - 200, 100, True)
    if punkty_1 == 15:
        napisz("Gracz 1 wygrał", szerokosc // 2 - 150, wysokosc // 2 + 200, 50, True)
    else:
        napisz("Gracz 2 wygrał", szerokosc // 2 - 150, wysokosc // 2 + 200, 50, True)

    pygame.display.update()
    
    sleep(4)
    sys.exit()



def Game(): 
    punkty_1 = 0
    punkty_2 = 0

    clock = 0
    pause = False

    pause_txt = pygame.font.Font.render(pygame.font.SysFont("", 96), "PAUSE", True, (115, 115, 115))


    paletka_szerokosc = 35
    paletka_wysokosc = 180
    paletka_predkosc = 15

    whait_time = 0

    pilka_szerokosc = 20
    pilka_wysokosc = 20
    pilka_predkosc_x = 4.5
    pilka_predkosc_y = 4.5

    paletka1_x = 50
    paletka1_y = wysokosc // 2 - paletka_wysokosc // 2
    paletka2_x = szerokosc - 50 - paletka_szerokosc
    paletka2_y = wysokosc // 2 - paletka_wysokosc // 2
    pilka_x = szerokosc // 2 - pilka_szerokosc // 2
    pilka_y = wysokosc // 2 - pilka_wysokosc // 2

    gra_aktywna = True
    while gra_aktywna:
        keys = pygame.key.get_pressed()
        clock += pygame.time.Clock().tick(120) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if keys[pygame.K_ESCAPE]:
                pause = not pause
        
        if pause:
            window.blit(pause_txt ,(szerokosc / 2 - 111, wysokosc / 2 - 29))
            pygame.display.update()
            continue
        
        window.fill((0, 0, 0))

        napisz(f"{punkty_1}:{punkty_2}", szerokosc / 2, 100, 25)
        
        
        if keys[pygame.K_w] and paletka1_y > 0:
            paletka1_y -= paletka_predkosc
        if keys[pygame.K_s] and paletka1_y < wysokosc - paletka_wysokosc:
            paletka1_y += paletka_predkosc
        if keys[pygame.K_UP] and paletka2_y > 0:
            paletka2_y -= paletka_predkosc
        if keys[pygame.K_DOWN] and paletka2_y < wysokosc - paletka_wysokosc:
            paletka2_y += paletka_predkosc

        if whait_time <= 0:
            
            whait_time = 0
            pilka_x += pilka_predkosc_x
            pilka_y += pilka_predkosc_y
        else:
            sleep(0.001)
            whait_time -= 0.001

        if pilka_y <= 0 or pilka_y >= wysokosc - pilka_wysokosc:
            pilka_predkosc_y *= -1

        
        if pilka_x <= paletka1_x + paletka_szerokosc and paletka1_y <= pilka_y <= paletka1_y + paletka_wysokosc:
            pilka_predkosc_x *= -1
        if pilka_x >= paletka2_x - pilka_szerokosc and paletka2_y <= pilka_y <= paletka2_y + paletka_wysokosc:
            pilka_predkosc_x *= -1
        
        pygame.draw.rect(window, (255, 255, 255), (paletka1_x, paletka1_y, paletka_szerokosc, paletka_wysokosc))
        pygame.draw.rect(window, (255, 255, 255), (paletka2_x, paletka2_y, paletka_szerokosc, paletka_wysokosc))
        
        if pilka_x <= paletka1_x:
            punkty_2 += 1
            pilka_x = szerokosc // 2 - pilka_szerokosc // 2
            pilka_y = wysokosc // 2 - pilka_wysokosc // 2
            pygame.draw.ellipse(window, (255, 255, 255), (pilka_x, pilka_y, pilka_szerokosc, pilka_wysokosc)) 
            pygame.display.update()
            whait_time = 0.2
        if pilka_x >= paletka2_x :
            punkty_1 += 1
            pilka_x = szerokosc // 2 - pilka_szerokosc // 2
            pilka_y = wysokosc // 2 - pilka_wysokosc // 2
            pygame.draw.ellipse(window, (255, 255, 255), (pilka_x, pilka_y, pilka_szerokosc, pilka_wysokosc)) 
            pygame.display.update()
            whait_time = 0.2
            
        else:
            pygame.draw.ellipse(window, (255, 255, 255), (pilka_x, pilka_y, pilka_szerokosc, pilka_wysokosc)) 


        if punkty_1 == 15 or punkty_2 == 15:
            gameover(punkty_1, punkty_2) 
        
        
        pygame.display.update()


if __name__ == "__main__":
    main()
    
    
    
    
#json
    
    
    
    
    
data = {
    "user": "Gracz1",
    "user": 1,
    
}

with open('data.json', 'w') as json_file:
    json.dump(data, json_file)
    
with open('data.json', 'r') as json_file:
    data = json.load(json_file)
print(data)


data = {
    "user": "Gracz2",
    "user": 2,
    "city": "New York"
}


with open('data.json', 'w') as json_file:
    json.dump(data, json_file)
    
    
with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    print(data)
    
    
with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
try:
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Plik nie został znaleziony.")
except json.JSONDecodeError:
    print("Błąd dekodowania pliku JSON.")  
    