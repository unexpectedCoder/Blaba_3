import numpy as np
import pygame
import random

pygame.init()                    # Запустили пайгейм
fpsClock = pygame.time.Clock()   # Функция для ФПС




""" Объявлем константы
"""
DIS_SIZE = (600, 600)
#DIS_SIZE = (400, 400)
FPS = 60


DISPLAY = pygame.display.set_mode(DIS_SIZE)         # Поверхность для отрисовки
pygame.display.set_caption('Lab. number 3')         # Название экрана 


class Particle:
    """ Класс, который создает частицу

        Arguments:
            radius  {int} -- радиус частицы
            posx {int} -- начальная координата Х
            posy {int} -- начальная координата Y
            color {tuple} -- цвет частицы в RGB 
    """

    def __init__(self, radius, posx, posy, color):
        self.radius = radius
        self.posx = posx
        self.posy = posy
        self.r = np.array([self.posx, self.posy])
        self.color = color
        self.speed = np.array([float(random.choice([-5, 5])), float(random.choice([-5, 5]))])
        self.pygame = pygame
         
    def render(self):
        """ Отрисовывает частицу
        """
        self.pygame.draw.circle(DISPLAY, center = (self.r[0], self.r[1]), color = self.color, radius = self.radius)

    def collision(self, particles):    
        parts = self.neighbours(particles)
        if self.r[0] >= 600 - self.radius or self.r[0] <= 0 + self.radius:
            self.speed[0] *= -1
        elif self.r[1] >= 600 - self.radius or self.r[1] <= 0 + self.radius:
            self.speed[1] *= -1       
        for i in range(len(parts)):
            if self.interval(self.r[0], self.r[1], parts[i].r[0], parts[i].r[1]) <= 2*self.radius:
                self.speed = np.array([float(random.choice([-5, 5])), float(random.choice([-5, 5]))])
    
    def coord_update(self, particles):
        dt = 0.05

        # Пункт 4.1
        self.r += self.speed
        
        # Пункт 4.2
        #self.r += np.array([float(random.choice([-5, 5])), float(random.choice([-5, 5]))]) 

    def interval(self, x1, y1, x2, y2):
        interval = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return interval

    def neighbours(self, particles):       
        part = particles  
        check_rad = 4*self.radius
        neib_list = []
        for i in range(len(part)):      
            if self.interval(self.r[0], self.r[1], part[i].r[0], part[i].r[1]) <= check_rad and \
                self.interval(self.r[0], self.r[1], part[i].r[0], part[i].r[1]) != 0:
                neib_list.append(part[i])
        return neib_list

    def sumF(self):
        sumF = np.array([0, 0])
        return sumF
    
    def _is_it_me(self, x2, y2):
        # Если интервал 0, то выведи True, иначе False
        pass

    def _func(self): 
        pass


class Cell:
    def __init__(self, cell_id, x1, y1, particles, C1, C2):
        self.cell_id = cell_id
        self.particles = particles

        self.container = []
        self.p_num = len(self.particles)


        self.color = (255, 255, 255)
        self.changed_color = (0, 255, 0)
        self.dont_change_color = True
        self.pygame = pygame

        self.x1 = x1
        self.y1 = y1
        self.C1 = C1
        self.C2 = C2
        self.top_left = (self.x1, self.y1)
        self.top_right = (self.x1 + self.C1, self.y1)
        self.bottom_right = (self.x1 + self.C1, self.y1 + self.C2)
        self.bottom_left = (self.x1, self.y1 + self.C2)

    def cell_render(self):
        #print('Starting cell render...')
        if self.dont_change_color:
            #print('Coloring cell in white...')
            self.pygame.draw.polygon(DISPLAY, self.color, [self.top_left, self.top_right, self.bottom_right, self.bottom_left])
        else:
            self.pygame.draw.polygon(DISPLAY, self.changed_color, [self.top_left, self.top_right, self.bottom_right, self.bottom_left])

    def color_changing(self):
        if self.dont_change_color == False:
            return None
        particles_in_cell = []
        for particle in self.particles:
            if (particle.r[0]>=self.top_left[0]) and (particle.r[0]<=self.top_right[0]) and (particle.r[1]<=self.bottom_left[1]) and (particle.r[1]>=self.top_left[1]):
                self.dont_change_color = False


# Цикл который создает лист p с экзеплярами класса частиц (то есть сами частицы)
num = 50

N, M = 60, 60
All_cell = N * M 
R = 0.8
C1, C2 = DIS_SIZE[0]//M, DIS_SIZE[1]//N

p = [] 
c = []


for particles in range(num):
    p.append(Particle(2, float(random.randint(20, 500)), float(random.randint(20, 500)), (255, 0, 0)))

for x in range(0, DIS_SIZE[0], C1):
    for y in range(0, DIS_SIZE[1], C2):
        c.append(Cell(1, x, y, p, C1, C2))


def main():
    """ Главный цикл

    """
    explored, unexplored = 0, 0
    t = 0
    not_done = True
    
    while not_done:
        """ 1. Обновляем лист 
            2. Проверяем на нажатие Х
            3. Отрисовываем круг
            4. Меням позицию Х
            5. Меняем позицию У
            6. Обновляем весь лист
        """
        # Чистим лист
        DISPLAY.fill((0, 0, 0))
        # Проверка на то, что мы нажали на крестик    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Проверка на стенку
        for particle in range(num):
            p[particle].collision(p)
            p[particle].coord_update(p)

        # Отрисовка клеток
        for cell in c:
            cell.color_changing()
            cell.cell_render()

        # Отрисовка объекта
        for particle in range(num):
            p[particle].render()

        for cell in c:
            if cell.dont_change_color == True:
                unexplored += 1
            else:
                explored += 1

        t += 1
        print('num of explored cells =', explored,'>>>>', 'num of unexplored cells =', unexplored,'....', 't =', t)

        if All_cell * R - explored < 0:
            print('Final velocity = ', explored / t)
            not_done = False

        explored, unexplored = 0, 0

        # Обновить лист
        pygame.display.flip() 
    
        # Вывод каждого 30 кадра
        fpsClock.tick(FPS)

    

if __name__ == '__main__':    # PEP-8
    main()
    

