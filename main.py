import sys

import pygame
from AI import *

#Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
SILVER = (192,192,192)

#Size of each rectangle.
LENGTH = 30
WIDTH = 30

#Margin between rectangles
MARGIN = 5

HUMAN_VS_HUMAN = False
HUMAN_VS_AI = False
AI_VS_HUMAN = False
AI_VS_AI = False

endGame = False
gameStart = False
gold_human = True
silver_human = True

gold_tt = []
silver_tt = []
hash_table = create_hashtable()

#turn = 1 is gold
#turn = -1 is silver
initial_turn = 1
turn = initial_turn
last_turn = initial_turn
turns_number = 2

gold_pieces = 12
silver_pieces = 20
winner = 0

# Grid, is list of lists
grid = []
for row in range(11):
    grid.append([])
    for column in range(11):
        grid[row].append(0)

# Flag
grid[5][5] = 3
grid[3][4] = 1
grid[3][5] = 1
grid[3][6] = 1
grid[4][7] = 1
grid[5][7] = 1
grid[6][7] = 1
grid[4][3] = 1
grid[5][3] = 1
grid[6][3] = 1
grid[7][4] = 1
grid[7][5] = 1
grid[7][6] = 1

grid[1][3] = 2
grid[1][4] = 2
grid[1][5] = 2
grid[1][6] = 2
grid[1][7] = 2
grid[9][3] = 2
grid[9][4] = 2
grid[9][5] = 2
grid[9][6] = 2
grid[9][7] = 2
grid[3][9] = 2
grid[4][9] = 2
grid[5][9] = 2
grid[6][9] = 2
grid[7][9] = 2
grid[3][1] = 2
grid[4][1] = 2
grid[5][1] = 2
grid[6][1] = 2
grid[7][1] = 2

origin = []
destiny = []
pin_piece = []

pygame.init()

# Size of the screen
WINDOW = [500, 500]
SCREEN = pygame.display.set_mode(WINDOW)

pygame.display.set_caption("Breakthru game")

clock = pygame.time.Clock()

coords_HvsH = pygame.draw.rect(SCREEN, RED, (20, 20, 456, 87))
coords_HvsAI = pygame.draw.rect(SCREEN, RED, (20, 120, 376, 110))
coords_AIvsH = pygame.draw.rect(SCREEN, RED, (20, 240, 330, 89))
coords_AIvsAI = pygame.draw.rect(SCREEN, RED, (20, 350, 218, 87))

#Main menu
while True:
    exiting = False
    # SCREEN.fill(BLACK)
    SCREEN.blit(pygame.image.load('images/H_vs_H.PNG'), (20, 20))
    SCREEN.blit(pygame.image.load('images/H_vs_AI.PNG'), (20, 120))
    SCREEN.blit(pygame.image.load('images/AI_vs_H.PNG'), (20, 240))
    SCREEN.blit(pygame.image.load('images/AI_vs_AI.PNG'), (20, 350))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (LENGTH + MARGIN)
            row = pos[1] // (WIDTH + MARGIN)
            print("Click ", pos, "Coordinates in the matrix: ", row, column)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if coords_HvsH.collidepoint(pos):
                    gold_human = True
                    silver_human = True
                    exiting = True
                    break
                elif coords_HvsAI.collidepoint(pos):
                    gold_human = True
                    silver_human = False
                    exiting = True
                    break
                elif coords_AIvsH.collidepoint(pos):
                    gold_human = False
                    silver_human = True
                    exiting = True
                    break
                elif coords_AIvsAI.collidepoint(pos):
                    gold_human = False
                    silver_human = False
                    exiting = True
                    break
    if exiting:
        break
    pygame.display.update()
    clock.tick(60)


# SET PIECES IN THE BOARD
# gameStart = False
# while not gameStart:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             endGame = True
#             pygame.quit()
#             sys.exit(0)
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             pos = pygame.mouse.get_pos()
#             column = pos[0] // (LENGTH + MARGIN)
#             row = pos[1] // (WIDTH + MARGIN)
#             if gold_pieces > 0:
#                 [grid, turn, changed] = add_piece_beginning(grid, 1, [row, column])
#                 if changed:
#                     gold_pieces -= 1
#             elif silver_pieces > 0:
#                 [grid, turn, changed] = add_piece_beginning(grid, -1, [row, column])
#                 if changed:
#                     silver_pieces -= 1
#             else:
#                 print("No more pieces in the grid")
#             if silver_pieces == 0 : gameStart = True
#             print("Click ", pos, "Coordinates in the matrix: ", row, column)


coords_gold = pygame.draw.rect(SCREEN, RED, (20, 20, 150, 83))
coords_silver = pygame.draw.rect(SCREEN, RED, (20, 120, 188, 92))
while True:
    exiting = False
    SCREEN.fill(BLACK)
    SCREEN.blit(pygame.image.load('images/gold.PNG'), (20, 20))
    SCREEN.blit(pygame.image.load('images/silver.PNG'), (20, 120))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (LENGTH + MARGIN)
            row = pos[1] // (WIDTH + MARGIN)
            print("Click ", pos, "Coordinates in the matrix: ", row, column)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if coords_gold.collidepoint(pos):
                    turn = 1
                    exiting = True
                    break
                elif coords_silver.collidepoint(pos):
                    turn = -1
                    exiting = True
                    break
    if exiting:
        break
    pygame.display.update()
    clock.tick(60)


while not endGame:
    if turn == 1 and not gold_human:
        # [grid, turn, changed, is_captured, winner] = make_random_moves(grid, turns_number, turn)
        [grid, turn, is_captured, winner] = make_move(grid, turn, gold_tt, hash_table)
        turn = -1
        turns_number = 2
    elif turn == -1 and not silver_human:
        # [grid, turn, changed, is_captured, winner] = make_random_moves(grid, turns_number, turn)
        [grid, turn, is_captured, winner] = make_move(grid, turn, silver_tt, hash_table)
        turn = 1
        turns_number = 2
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGame = True
            elif (winner == 0 and event.type == pygame.MOUSEBUTTONDOWN) :
                pos = pygame.mouse.get_pos()
                column = pos[0] // (LENGTH + MARGIN)
                row = pos[1] // (WIDTH + MARGIN)
                print("Click ", pos, "Coordinates in the matrix: ", row, column)
                if in_range([row, column]):
                    if turn == 1 and gold_human and turns_number > 0:
                        if grid[row][column] == 1 and [row, column] != pin_piece:
                            origin = [row, column]
                        elif (origin != [] and grid[origin[0]][origin[1]] == 1):
                            [grid, changed, is_captured, winner] = add_piece(grid, turns_number, turn, origin, [row, column], False)
                            if changed:
                                print("it changed!!!!!!")
                                turns_number -= 1
                                if turns_number == 0 or is_captured:
                                    turn = -1
                                    turns_number = 2
                                    pin_piece = []
                                elif total_pieces(grid, turn) == 1:
                                    turn = -1
                                    turns_number = 2
                                    pin_piece = []
                                else:
                                    turn = 1
                                    pin_piece = [row, column]
                                origin = []
                                destiny = []
                    if turn == 1 and gold_human and turns_number == 2:
                        if grid[row][column] == 3:
                            origin = [row, column]
                        elif (origin != [] and grid[origin[0]][origin[1]] == 3):
                            [grid, changed, is_captured, winner] = add_piece(grid, turns_number, turn, origin, [row, column], True)
                            if changed:
                                print("it changed!!!!!!")
                                turn = -1
                                turns_number = 2
                                origin = []
                                destiny = []
                    if turn == -1 and silver_human and turns_number > 0:
                        if grid[row][column] == 2 and [row, column] != pin_piece:
                            origin = [row, column]
                        elif (origin != [] and grid[origin[0]][origin[1]] == 2):
                            [grid, changed, is_captured, winner] = add_piece(grid, turns_number, turn, origin, [row, column], False)
                            if changed:
                                print("it changed!!!!!!")
                                turns_number -= 1
                                if turns_number == 0 or is_captured:
                                    turn = 1
                                    turns_number = 2
                                    pin_piece = []
                                elif total_pieces(grid, turn) == 1:
                                    turn = 1
                                    turns_number = 2
                                    pin_piece = []
                                else:
                                    turn = -1
                                    pin_piece = [row, column]
                                origin = []
                                destiny = []
    if winner == 1:
        print("Gold win!!!!")
        for row in range(11):
            print(grid[row])
        endGame = True
    elif winner == 2:
        print("Silver win!!!")
        for row in range(11):
            print(grid[row])
        endGame = True

    SCREEN.fill(BLACK)

    for row in range(11):
        for column in range(11):
            color = WHITE
            if grid[row][column] == 1:
                color = YELLOW
            elif grid[row][column] == 2:
                color = BLACK
            elif grid[row][column] == 3:
                color = RED
            pygame.draw.rect(SCREEN,
                             color,
                             [(MARGIN + LENGTH) * column + MARGIN,
                              (MARGIN + WIDTH) * row + MARGIN,
                              LENGTH,
                              WIDTH])

    clock.tick(60)

    pygame.display.flip()
    if endGame == True:
        pygame.time.wait(20000)

pygame.quit()