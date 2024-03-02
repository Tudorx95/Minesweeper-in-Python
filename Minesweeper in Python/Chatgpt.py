import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Minesweeper")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Set up game variables
grid_size = 10
cell_size = 40
mine_count = 15
revealed = [[False] * grid_size for _ in range(grid_size)]
flags = [[False] * grid_size for _ in range(grid_size)]
grid = [[0] * grid_size for _ in range(grid_size)]

# Place the mines randomly on the grid
mines_placed = 0
while mines_placed < mine_count:
    row = random.randint(0, grid_size - 1)
    col = random.randint(0, grid_size - 1)
    if grid[row][col] == 0:
        grid[row][col] = -1  # -1 represents a mine
        mines_placed += 1

# Calculate the number of neighboring mines for each cell
for row in range(grid_size):
    for col in range(grid_size):
        if grid[row][col] != -1:
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < grid_size and 0 <= col + j < grid_size and grid[row + i][col + j] == -1:
                        count += 1
            grid[row][col] = count


def reveal_cell(row, col):
    if 0 <= row < grid_size and 0 <= col < grid_size and not revealed[row][col]:
        revealed[row][col] = True

        if grid[row][col] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    reveal_cell(row + i, col + j)


# Main game loop
# def main():
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        cell_col = mouse_pos[0] // cell_size
        cell_row = mouse_pos[1] // cell_size
        # print(cell_row, cell_col)
        # Left mouse button clicked
        if event.button == 1 and (cell_row >= 0 and cell_row < grid_size) and (cell_col >= 0 and cell_col < grid_size):
            if grid[cell_row][cell_col] == -1:  # Clicked on a mine
                revealed[cell_row][cell_col] = True
                print("Game Over!")
                break
            else:
                reveal_cell(cell_row, cell_col)

        elif event.button == 3:  # Right mouse button clicked
            flags[cell_row][cell_col] = not flags[cell_row][cell_col]

    # Clear the screen
    # screen.fill(BLACK)

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            cell_rect = pygame.Rect(
                col * cell_size, row * cell_size, cell_size, cell_size)

            if revealed[row][col]:
                pygame.draw.rect(screen, WHITE, cell_rect)
                if grid[row][col] != 0:
                    text = str(grid[row][col])
                    font = pygame.font.Font(None, 30)
                    text_surface = font.render(text, True, BLACK)
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    screen.blit(text_surface, text_rect)
                    # print(row, col)
            elif flags[row][col]:
                # pygame.draw.rect(screen, GRAY, cell_rect)
                # Replace with your flag image path
                flag_img = pygame.image.load("flag.png")
                flag_img = pygame.transform.scale(
                    flag_img, (cell_size, cell_size))
                screen.blit(flag_img, cell_rect)
            else:
                pygame.draw.rect(screen, GRAY, cell_rect)

            pygame.draw.rect(screen, BLACK, cell_rect, 1)

    # Update the screen
    pygame.display.flip()

# Quit the game
pygame.quit()
