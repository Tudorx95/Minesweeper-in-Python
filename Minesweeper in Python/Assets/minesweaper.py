import pygame
import os
import random
import pprint

pygame.display.set_caption("Minesweeper")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WORD_FONT = (229, 193, 49)
WORD_BACKGROUND = (175, 174, 167)  # GRAY

BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
DARK_BLUE = (0, 0, 139)
DARK_RED = (139, 0, 0)
TURQUOISE = (64, 224, 208)
VIOLET = (128, 0, 255)
GRAY = (128, 128, 128)

LEFT_CLICK = 1
RIGHT_CLICK = 3
CELL_SIZE = 50

FPS = 60
pygame.display.init()
pygame.font.init()

clock = pygame.time.Clock()


def start_menu():
    screen = pygame.display.set_mode((1190, 564))
    image = pygame.image.load(os.path.join("Hello_World.png"))
    image = pygame.transform.scale(image, (1190, 564))
    screen.blit(image, (0, 0))
    pygame.display.update()
    pygame.time.wait(1000)
    pygame.quit()


class cell:
    def __init__(self, value, visited, x, y, flag):
        self.value = value
        self.visited = visited
        self.x = x
        self.y = y
        self.flag = flag


def print_reset_button(screen, BOARD_WIDTH, BOARD_HEIGHT, filename):
    reset_box = pygame.Rect((BOARD_WIDTH/2-30, BOARD_HEIGHT/2-30), (60, 60))
    pygame.draw.rect(screen, BLACK, reset_box)
    image = pygame.image.load(os.path.join(filename))
    image = pygame.transform.scale(image, (50, 50))
    # where to insert image
    screen.blit(image, (BOARD_WIDTH/2-30+5, BOARD_HEIGHT/2-30+5))
    return reset_box


def generate_board(height, width, nr_bombs, mx, my):
    # declaring the board as independent collection of objects
    board = [[0 for _ in range(width)] for _ in range(height)]

    while nr_bombs:
        y = random.randint(0, width-1)  # col
        x = random.randint(0, height-1)  # lin
        if x != mx and y != my and board[x][y] >= 0:
            board[x][y] = -1
            nr_bombs -= 1
            if x-1 >= 0 and y-1 >= 0 and board[x-1][y-1] != -1:
                board[x-1][y-1] += 1
            if x-1 >= 0 and board[x-1][y] != -1:
                board[x-1][y] += 1
            if x-1 >= 0 and y+1 < width and board[x-1][y+1] != -1:
                board[x-1][y+1] += 1
            if y-1 >= 0 and board[x][y-1] != -1:
                board[x][y-1] += 1
            if y+1 < width and board[x][y+1] != -1:
                board[x][y+1] += 1
            if x+1 < height and y-1 >= 0 and board[x+1][y-1] != -1:
                board[x+1][y-1] += 1
            if x+1 < height and board[x+1][y] != -1:
                board[x+1][y] += 1
            if x+1 < height and y+1 < width and board[x+1][y+1] != -1:
                board[x+1][y+1] += 1
    # pprint.pprint(board)
    return board


def reveal_all_bombs(screen, grid, BOARD_WIDTH, BOARD_HEIGHT, mx, my):
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if grid[i][j].value == -1 and grid[i][j].flag == 0:
                if i != mx or j != my:
                    grid[i][j].visited = 1
                    cell_rect = pygame.Rect(
                        grid[i][j].x, grid[i][j].y, CELL_SIZE, CELL_SIZE)
                    bomb_image = pygame.image.load(
                        os.path.join("unclicked-bomb.png"))
                    bomb_image = pygame.transform.scale(
                        bomb_image, (CELL_SIZE-1, CELL_SIZE-1))
                    screen.blit(bomb_image, cell_rect)
                else:
                    cell_rect = pygame.Rect(
                        grid[i][j].x, grid[i][j].y, CELL_SIZE, CELL_SIZE)
                    bomb_image = pygame.image.load(
                        os.path.join("bomb-at-clicked-block.png"))
                    bomb_image = pygame.transform.scale(
                        bomb_image, (CELL_SIZE, CELL_SIZE))
                    screen.blit(bomb_image, cell_rect)
            elif grid[i][j].value == -1 and grid[i][j].flag != 0 and i != mx and j != my:
                grid[i][j].visited = 1
                cell_rect = pygame.Rect(
                    grid[i][j].x, grid[i][j].y, CELL_SIZE, CELL_SIZE)
                bomb_image = pygame.image.load(
                    os.path.join("wrong-flag.png"))
                bomb_image = pygame.transform.scale(
                    bomb_image, (CELL_SIZE-1, CELL_SIZE-1))
                screen.blit(bomb_image, cell_rect)


def update_block(mx, my, grid, BOARD_WIDTH, BOARD_HEIGHT):
    if mx < 0 or my < 0 or mx >= BOARD_HEIGHT or my >= BOARD_WIDTH or grid[mx][my].visited:
        return
    if grid[mx][my].value != -1:
        grid[mx][my].visited = 1
    if grid[mx][my].value or grid[mx][my].value == -1:
        return

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i or j:
                update_block(mx+i, my+j, grid, BOARD_WIDTH, BOARD_HEIGHT)


def winGame(grid, BOMBS, BOARD_WIDTH, BOARD_HEIGHT):
    nr_reveal = 0
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if grid[i][j].value != -1 and grid[i][j].visited == 1:
                nr_reveal += 1
    if BOARD_HEIGHT*BOARD_WIDTH == nr_reveal+BOMBS:
        return 1
    return 0


def print_win_message(screen, BOARD_WIDTH, BOARD_HEIGHT):
    pygame.Surface.convert_alpha(screen)
    pygame.font.init()
    font_type = pygame.font.SysFont("Arial", 50)
    text = font_type.render("YOU WIN!", True, BLACK)
    screen.blit(text, (BOARD_WIDTH/4-8, BOARD_HEIGHT/4-8))


def GameOver_message(screen, BOARD_WIDTH, BOARD_HEIGHT):
    pygame.Surface.convert_alpha(screen)
    pygame.font.init()
    font_type = pygame.font.SysFont("Arial", 50)
    text = font_type.render("Game Over!", True, BLACK)
    screen.blit(text, (BOARD_WIDTH/4-10, BOARD_HEIGHT/4-10))


def print_flag(screen, x, y):
    cell_rect = pygame.Rect(
        y, x, CELL_SIZE, CELL_SIZE)
    flag_img = pygame.image.load("flag.png")
    flag_img = pygame.transform.scale(
        flag_img, (CELL_SIZE, CELL_SIZE))
    screen.blit(flag_img, cell_rect)


def print_grid(screen, grid, BOARD_WIDTH, BOARD_HEIGHT):
    pygame.font.init()
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            # print(grid[i][j].x, grid[i][j].y)
            cell_rect = pygame.Rect(
                grid[i][j].x, grid[i][j].y, CELL_SIZE, CELL_SIZE)
            if grid[i][j].visited:
                pygame.draw.rect(screen, WHITE, cell_rect)
                if grid[i][j].value:
                    text = str(grid[i][j].value)
                    font = pygame.font.Font(None, 30)
                    text_surface = font.render(
                        text, True, select_color(grid[i][j].value))
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    screen.blit(text_surface, text_rect)
            elif grid[i][j].flag:
                flag_img = pygame.image.load("flag.png")
                flag_img = pygame.transform.scale(
                    flag_img, (CELL_SIZE, CELL_SIZE))
                screen.blit(flag_img, cell_rect)
            else:
                pygame.draw.rect(screen, WORD_BACKGROUND, cell_rect)
            pygame.draw.rect(screen, BLACK, cell_rect, 1)


def print_flagged_bombs(screen, BOMBS, BOARD_WIDTH, BOARD_HEIGHT):
    flag_box = pygame.Rect((BOARD_WIDTH/5, BOARD_HEIGHT/5), (40, 30))
    pygame.draw.rect(screen, WHITE, flag_box)
    text = str(BOMBS)
    pygame.font.init()
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(
        center=flag_box.center)
    screen.blit(text_surface, text_rect)
    pygame.draw.rect(screen, BLACK, flag_box, 1)


def initiate_grid(BOARD_WIDTH, BOARD_HEIGHT):
    grid = [[cell(None, 0, 0, 0, 0) for _ in range(BOARD_WIDTH)]
            for _ in range(BOARD_HEIGHT)]

    # populate struct coordinates
    x = 0
    y = 100
    for i in range(BOARD_HEIGHT):
        x = 0
        for j in range(BOARD_WIDTH):
            grid[i][j].x = x  # x= left -> width
            grid[i][j].y = y  # y= top -> height
            grid[i][j].visited = 0
            grid[i][j].flag = 0
            x += 50
        y += 50
    return grid


def select_color(value):
    if value == 1:
        return BLUE
    elif value == 2:
        return GREEN
    elif value == 3:
        return RED
    elif value == 4:
        return DARK_BLUE
    elif value == 5:
        return DARK_RED
    elif value == 6:
        return TURQUOISE
    elif value == 7:
        return VIOLET
    else:
        return GRAY


def start_game(BOARD_WIDTH, BOARD_HEIGHT, BOMBS):
    pygame.quit()

    screen = pygame.display.set_mode((BOARD_WIDTH*50, BOARD_HEIGHT*50+100))
    upper_box = pygame.Rect((0, 0), (BOARD_WIDTH*50, 100))
    pygame.draw.rect(screen, WORD_BACKGROUND, upper_box)
    reset_box = print_reset_button(
        screen, BOARD_WIDTH*50, 100, "smile-face.jpeg")

    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    grid = initiate_grid(BOARD_WIDTH, BOARD_HEIGHT)

    print_grid(screen, grid, BOARD_WIDTH, BOARD_HEIGHT)
    pygame.display.update()
    i = 0
    reset = 0
    nr_bombs = BOMBS
    run = True
    while run:
        choice = 0
        clock.tick(FPS)
        print_flagged_bombs(screen, nr_bombs, BOARD_WIDTH*50, 100)
        # quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT_CLICK:
                    choice = LEFT_CLICK
                if event.button == RIGHT_CLICK:
                    choice = RIGHT_CLICK
                break

        # CLICKS
        if event.type == pygame.MOUSEBUTTONDOWN:
            (my, mx) = pygame.mouse.get_pos()
            # mx=Height and my=Width
            # LEFT_CLICK
            if choice == LEFT_CLICK:
                # Verify reset button
                if reset_box.collidepoint((my, mx)):
                    run = False
                    reset = 1
                    break
                # Verify in the grid (lower box)
                if mx > 100:
                    my = my//CELL_SIZE
                    mx = (mx-100)//CELL_SIZE
                    # It is in the grid
                    if 0 <= mx < BOARD_HEIGHT and 0 <= my < BOARD_WIDTH:
                        # first Left click -> generate entire grid
                        if i == 0:
                            board = generate_board(
                                BOARD_HEIGHT, BOARD_WIDTH, BOMBS, mx, my)

                            for i in range(BOARD_HEIGHT):
                                for j in range(BOARD_WIDTH):
                                    grid[i][j].value = board[i][j]
                            i = 1

                        # If it is unflagged
                        if grid[mx][my].flag == 0:
                            # if it is a bomb
                            if grid[mx][my].value == -1:
                                run = False
                                reveal_all_bombs(
                                    screen, grid, BOARD_WIDTH, BOARD_HEIGHT, mx, my)  # modify the function as to print 'B' ch
                                print_reset_button(
                                    screen, BOARD_WIDTH*50, 100, "dizzy-face.png")
                                GameOver_message(
                                    screen, BOARD_WIDTH*50, BOARD_HEIGHT*50+100)
                                pygame.display.update()
                                pygame.time.wait(2000)
                                break
                                # if it is a number !=0
                            elif grid[mx][my].value != 0:
                                grid[mx][my].visited = 1
                                cell_rect = pygame.Rect(
                                    my*CELL_SIZE, mx*CELL_SIZE+100, CELL_SIZE, CELL_SIZE)
                                pygame.draw.rect(screen, WHITE, cell_rect)
                                text = str(grid[mx][my].value)
                                pygame.font.init()
                                font = pygame.font.Font(None, 30)
                                text_surface = font.render(
                                    text, True, select_color(grid[mx][my].value))
                                text_rect = text_surface.get_rect(
                                    center=cell_rect.center)
                                screen.blit(text_surface, text_rect)
                                pygame.draw.rect(screen, BLACK, cell_rect, 1)
                            else:  # if it is 0
                                update_block(
                                    mx, my, grid, BOARD_WIDTH, BOARD_HEIGHT)  # possible loss of data
                                print_grid(
                                    screen, grid, BOARD_WIDTH, BOARD_HEIGHT)

                    # RIGHT_CLICK
            elif choice == RIGHT_CLICK:
                if mx > 100:
                    my = my//CELL_SIZE
                    mx = (mx-100)//CELL_SIZE
                    # If it is not visited and it is in the grid
                    if 0 <= mx < BOARD_HEIGHT and 0 <= my < BOARD_WIDTH and grid[mx][my].visited == 0:
                        # if it is unflagged -> flag
                        if grid[mx][my].flag == 0:
                            grid[mx][my].flag = 1
                            nr_bombs -= 1
                            # print(mx, my)
                            print_flag(screen, mx*CELL_SIZE+100, my*CELL_SIZE)
                        else:  # if it is flagged then unflag
                            grid[mx][my].flag = 0
                            nr_bombs += 1
                            cell_rect = pygame.Rect(
                                my*CELL_SIZE, mx*CELL_SIZE+100, CELL_SIZE, CELL_SIZE)
                            pygame.draw.rect(
                                screen, WORD_BACKGROUND, cell_rect)
                            pygame.draw.rect(screen, BLACK, cell_rect, 1)
                            pygame.display.update()

        pygame.display.update()
        # win function

        if winGame(grid, BOMBS, BOARD_WIDTH, BOARD_HEIGHT):
            print_win_message(screen, BOARD_WIDTH*50, BOARD_HEIGHT*50+100)
            print_reset_button(
                screen, BOARD_WIDTH*50, 100, "winner-face.png")
            pygame.display.update()
            pygame.time.wait(3000)
            run = False

    if reset:
        start_game(BOARD_WIDTH, BOARD_HEIGHT, BOMBS)
    else:
        menu()


def menu():
    pygame.display.init()
    screen = pygame.display.set_mode((1190, 564))
    image = pygame.image.load(os.path.join("menu_background.jpg"))
    image = pygame.transform.scale(image, (1190, 564))
    screen.blit(image, (0, 0))  # where to insert image

    pygame.font.init()

    # Select Mode text
    font_type = pygame.font.SysFont("Arial", 50)
    text = font_type.render("Select the game mode", True, (102, 95, 94))
    screen.blit(text, (300, 150))

    # Mode button
    easy_box = pygame.Rect((200, 250), (145, 70))
    pygame.draw.rect(screen, WORD_BACKGROUND, easy_box)
    font_type = pygame.font.SysFont("comicsans", 70, True)
    text = font_type.render("Easy", True, WORD_FONT)
    screen.blit(text, (215, 260))

    medium_box = pygame.Rect((500, 250), (205, 70))
    pygame.draw.rect(screen, WORD_BACKGROUND, medium_box)
    font_type = pygame.font.SysFont("comicsans", 70, True)
    text = font_type.render("Medium", True, WORD_FONT)
    screen.blit(text, (510, 260))

    hard_box = pygame.Rect((800, 250), (145, 70))
    pygame.draw.rect(screen, WORD_BACKGROUND, hard_box)
    font_type = pygame.font.SysFont("comicsans", 70, True)
    text = font_type.render("Hard", True, WORD_FONT)
    screen.blit(text, (815, 260))

    quit_box = pygame.Rect((540, 400), (125, 60))
    pygame.draw.rect(screen, WORD_BACKGROUND, quit_box)
    font_type = pygame.font.SysFont("comicsans", 70, True)
    text = font_type.render("QUIT", True, WORD_FONT)
    screen.blit(text, (540, 405))

    pygame.display.update()
    # pygame.time.wait(2000)
    run = True
    start = 0
    while run:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = pygame.mouse.get_pos()
            if quit_box.collidepoint(mx, my):
                run = False
                break
            else:
                is_clicked = 0
                if easy_box.collidepoint(mx, my):
                    BOARD_WIDTH = 10
                    BOARD_HEIGHT = 10
                    BOMBS = 10
                    is_clicked = 1
                elif medium_box.collidepoint(mx, my):
                    BOARD_WIDTH = 16
                    BOARD_HEIGHT = 16
                    BOMBS = 40
                    is_clicked = 1
                elif hard_box.collidepoint(mx, my):
                    BOARD_WIDTH = 30
                    BOARD_HEIGHT = 16
                    BOMBS = 99
                    is_clicked = 1
                if is_clicked:
                    run = False
                    start = 1
                    break
    if start:
        start_game(BOARD_WIDTH, BOARD_HEIGHT, BOMBS)


def main():
    start_menu()
    menu()


if __name__ == "__main__":
    main()
