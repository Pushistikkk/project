import pygame
from copy import deepcopy
from random import choice, randrange

#создаем окно
pygame.init()
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Tetris")
FPS = 60  # число кадров в секунду

# задаем окно заднего фона игры и окно игры
bg = pygame.image.load("img/background.jpg").convert()  # загружаем изображение
background = pygame.transform.smoothscale(bg, screen.get_size())
bg_game = pygame.image.load("img/background.jpg").convert()

# задаем параметры для дальнейшего использования в окне игры
width, High = 10, 20
T = 30
GAME_RES = width * T, High * T
# для получения рандомного цвета
get_color = lambda: (randrange(100, 255), randrange(100, 255), randrange(100, 255))

# создаем прямоугольники фигур
figures_pos = [[(-1, -1), (-2, -1), (0, -1), (1, -1)], [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],[(0, 0), (0, -1), (0, 1), (-1, 0)], [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],[(0, 0), (-1, 0), (0, 1), (-1, -1)]]
figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, T - 2, T - 2)

# оформляем шрифт надписей сбоку на экранах
fontObj, fontObj2 = pygame.font.SysFont('Aharoni', 80), pygame.font.SysFont('Aharoni', 140)  # задаем шрифт и его размер
font1, font2, font3, font4 = pygame.font.SysFont('Aharoni', 70), pygame.font.SysFont('Aharoni', 45), pygame.font.SysFont('Aharoni', 30), pygame.font.SysFont('Aharoni', 50)

def pause():

    """Останавливает игру.

    Параметры
    ------
    when_pause_text: str
    when_pause2_text: str
            две части фразы,сообщающей пользователю, что игра остановлена
    keys = pygame.key.get_pressed()
            отслеживает действия

    """

    # ЗАИМСТВОВАННЫЙ КУСОК КОДА
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  # ЗАИМСТВОВАННЫЙ КУСОК КОДА ЗАКОНЧИЛСЯ
        # НЕ ЗАИМСТВОВАННЫЙ КУСОК КОДА
        when_pause_text, when_pause2_text = font2.render('To continue the game,', True, (255, 255, 255)), font2.render('press "ENTER"', True, (255, 255, 255))
        screen.blit(when_pause_text, [225, 200]), screen.blit(when_pause2_text, [310, 300])
        # ЗАИМСТВОВАННЫЙ КУСОК КОДА
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # привязываем клавишу enter
            paused = False
        pygame.display.update()  # ЗАИМСТВОВАННЫЙ КУСОК КОДА ЗАКОНЧИЛСЯ
def get_record():

    """Считывает значение рекорд из файла "record", в случае отсутствия этого файла он создается с изначальным значением 0
    open - метод, который открывает файл
        as f -для прочтения
        as w - для замены содержимого
    """

    try:
        with open('record') as f:  # открываем файл и считываем оттуда значение
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:  # если файла нет, то мы его создаем и записываем туда начальное значение 0
            f.write('0')
def set_record(record, score):

    """функция для замены рекорда новым  в случае, если количество набранных очков больше, чем значение рекорда в файле "record"

    Параметры
    ------
    record: str
        значение рекорда, взятое из файла "record"
    score: int
        количество очков, набраных пользователем в процессе игры

    Методы
    ------
    rec = max(int(record), score): определяет наибольшее  из двух значений параметров
    """

    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))
def game():

    """Игровой цикл, который продолжается, пока пользователь не закончит игру или не выйдет из нее."""

    # СОЗДАЕМ ОКНО ПРОГРАММЫ
    def check_borders():

        """функция проверки границ для движения фигуры по х и у
        figure[i].x - движение фигуры по х
        figure[i].y - движение фигуры по у
        """
        
        if figure[i].x < 0 or figure[i].x > width - 1:  # если фигура вышла за правый или левый бортик
            return False
        elif figure[i].y > High - 1 or map[figure[i].y][figure[i].x]:
            return False  # если фигура вышла за нижнюю границу или под ней лежит еще одна фигура
        return True

    # задаем на окне игры прямоугольник с сеткой
    grid = [pygame.Rect(x * T, y * T, T, T) for x in range(width) for y in range(High)]

    # карта прямоугольника с сеткой, на котором отмечается положение фигур, и выбор отрисовки фигур и их цвета
    map = [[0 for i in range(width)] for j in range(High)]
    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = get_color(), get_color()

    # параметры анимации
    anim_count, anim_speed, anim_limit = 0, 20, 2000

    # параметры очков и полных линий, для начисления очков от собранных линий
    score, lines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    # бесконечный цикл самой игры
    while True:
        # экран с игрой и фон, получаем рекорд из файла
        game_sc, record = pygame.Surface(GAME_RES), get_record()
        screen.blit(background, (0, 0))

        # отрисовываем прямоугольную сетку
        [pygame.draw.rect(game_sc, (255, 255, 255), i_rect, 1) for i_rect in grid]

        # изначальные параметры для движения фигур
        dx, rotate = 0, False

        # отслеживаем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  dx = -1
                elif event.key == pygame.K_RIGHT:  dx = 1
                elif event.key == pygame.K_UP: rotate = True
                elif event.key == pygame.K_DOWN:  anim_limit = 100

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pause()

        # поворот фигур
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        # движение по х
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            # если фигура заходит за границы, мы восстанавливаем первоначальное (до границы) положение фигуры
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        # движение фигуры по y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        map[figure_old[i].y][figure_old[i].x] = color   # красим клетки поля в цвет упавшей фигуры
                    figure, color = next_figure, next_color
                    next_color = get_color()
                    next_figure = deepcopy(choice(figures))
                    anim_limit = 2000
                    break

        # отображаем сгенерированные фигуры на экране игры
        for i in range(4):
            figure_rect.x = figure[i].x * T
            figure_rect.y = figure[i].y * T
            pygame.draw.rect(game_sc, color, figure_rect)

        # рисуем следующую фигуру на основном экране
        for i in range(4):
            figure_rect.x = next_figure[i].x * T + 600
            figure_rect.y = next_figure[i].y * T + 200
            pygame.draw.rect(screen, next_color, figure_rect)

        # отрисовка полей на экране игры, окрашенных в цвет упавшей фигуры
        for y, raw in enumerate(map):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * T, y * T
                    pygame.draw.rect(game_sc, col, figure_rect)

        # убираем полные линии
        line, lines = High - 1, 0  # последняя линия поля
        for row in range(High - 1, -1, -1):
            count = 0   # счетчик заполненных плиток
            for i in range(width):
                if map[row][i]:# будем переходить на другую линию только если счетчик не полный
                    count += 1
                map[line][i] = map[row][i]
            if count < width:  # если счетчик полный, то мы переписываем заполненную линию первой незаполненной
                line -= 1
            else:
                anim_speed += 1
                lines += 1 # подсчитываем количество полных линий

        # добавляем в счетчик очков очки по количеству собранных линий
        score += scores[lines]

        # создаем и отрисовываем на основном экране надписи
        tetris, score_text, record_text = font1.render('TETRIS', True, (255, 158, 0)), font2.render('Score:', True, (255, 100, 0)), font2.render('Record:', True, (255, 100, 0))
        pause_text, pause2_text = font3.render('To stop the game,', True, (255, 255, 255)), font3.render('press "ESCAPE"', True, (255, 255, 255))
        screen.blit(font1.render(str(score), True, pygame.Color('white')), (60, 200)), screen.blit(font1.render(record, True, pygame.Color('white')), (60, 500))
        screen.blit(tetris, [650, 50]), screen.blit(score_text, [50, 160]), screen.blit(record_text, [50, 450]), screen.blit(pause_text, [630, 350]), screen.blit(pause2_text, [630, 400])

        # концовка
        for i in range(width):
            if map[0][i]:  # если какая-либо фигура достигла конца игрового поля
                set_record(record, score) # проверяем рекорд
                map = [[0 for i in range(width)] for i in range(High)]  # снова очищаем игровое поле
                anim_count, anim_speed, anim_limit = 0, 20, 2000
                score = 0
                menu()

        # отображаем экран с игрой на основном экране
        screen.blit(game_sc, (300, 60)), pygame.display.flip()
def menu():

    """создаем экран меню
    Параметры
    ------
    record: str
        получает значение рекорда из файла record
    get_record - метод получения рекорда из файла record - одна из функций
    """

    # размещаем надписи
    bg = pygame.image.load("img/tetris.jpg").convert()  # загружаем изображение
    background = pygame.transform.smoothscale(bg, screen.get_size())  # подгоняем изображение под размер экрана, создаем поверхность изобр
    text1 = fontObj.render('Welcome', True, (255, 0, 0))  # задаем надпись,сглаженность и цвет
    text2 = fontObj.render('to ', True, (255, 100, 0))
    text3 = fontObj2.render('Tetris ', True, (255, 230, 0))
    menu1_text, menu2_text, menu3_text = font4.render('PRESS', True, (0, 0, 255)), font4.render('Record:', True, (255, 0, 255)), font4.render('"ENTER"', True, (0, 255, 0))

    record = get_record()

    while True:
        # отображаем текст на экране
        screen.blit(background, (0,0))  # на поверхности экрана отображаем поверхность с содержимым картинки,blit - оператор переноса на поверхность
        screen.blit(text1, [30, 20])  # размещаем текст на окне меню
        screen.blit(text2, [170, 110])
        screen.blit(text3, [30, 200])
        screen.blit(menu2_text, [70, 500]), screen.blit(menu3_text, [650, 410]), screen.blit(menu1_text, [665, 350])
        screen.blit(font1.render(record, True, pygame.Color('white')), (80, 550))

        # привязываем действия к кнопкам
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()

        pygame.display.flip()


if __name__ == "__main__":
    menu()