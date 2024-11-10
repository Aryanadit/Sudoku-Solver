import pygame
from Tool import generate_board, solve, find_empty, valid
from copy import deepcopy

pygame.init()

class Board:
    def __init__(self, window):
        """Initializes a Board object with an initially empty puzzle."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]  # Initially empty
        self.tiles = [
            [Tile(self.board[i][j], window, i * 60, j * 60, is_preset=False) for j in range(9)]
            for i in range(9)
        ]
        self.window = window
        self.selected_cell = None  # To track the selected cell for user input

    def draw_board(self):
        """Draws the Sudoku board with grid lines and numbers."""
        self.window.fill((240, 240, 240))  # Background - white

        # Grid lines
        for i in range(10):
            line_thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.window, (0, 0, 0), (i * 60, 0), (i * 60, 540), line_thickness)
            pygame.draw.line(self.window, (0, 0, 0), (0, i * 60), (540, i * 60), line_thickness)

        # Numbers on the board
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j].value != 0:
                    self.tiles[i][j].display(self.tiles[i][j].value, (21 + j * 60, 16 + i * 60))

        # Highlight the selected cell
        if self.selected_cell:
            row, col = self.selected_cell
            pygame.display.flip()
            pygame.draw.rect(self.window, (0, 0, 255), (col * 60, row * 60, 60, 60), 4)  # Blue border for selected cell

        pygame.display.flip()

    def display_message(self, message, color=(255, 0, 0)):
        font = pygame.font.SysFont("lato", 30)
        text = font.render(message, True, color)
        self.window.blit(text, (10, 550))  # Display message near the bottom
        pygame.display.flip()

    def visualsolve(self):
        pygame.event.pump()
        empty = find_empty(self.board)
        if not empty:
            # Puzzle solved
            self.display_message("Puzzle Solved!", color=(0, 255, 0))  # Green color for success
            return True

        for num in range(1, 10):
            if valid(self.board, empty, num):
                self.board[empty[0]][empty[1]] = num
                self.tiles[empty[0]][empty[1]].value = num
                self.tiles[empty[0]][empty[1]].is_user_input = False  # Mark it as solved by the solver
                pygame.time.delay(100)  # Delay
                self.draw_board()

                if self.visualsolve():
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].is_user_input = False  # Mark it as unsolved
                pygame.time.delay(100)  # Delay
                self.draw_board()

        return False

    def handle_input(self, pos, value):
        """Handles user input for placing numbers into the cells, ensuring it's valid."""
        row, col = pos
        if self.board[row][col] == 0:  # Only allow input in empty cells
            if valid(self.board, (row, col), value):
                self.board[row][col] = value
                self.tiles[row][col].value = value
                self.tiles[row][col].is_user_input = True  # Mark tile as a user input
                self.draw_board()
            else:
                print("Invalid input: Conflicts with Sudoku rules.")
                self.display_message("Invalid input")

    def select_cell(self, pos):
        """Select a cell when clicked."""
        row, col = pos
        self.selected_cell = (row, col)

    def generate_random_board(self):
        self.board = generate_board()

        for i in range(9):
            for j in range(9):
                self.tiles[i][j].value = self.board[i][j]
                self.tiles[i][j].is_user_input = False
                self.tiles[i][j].is_preset = self.board[i][j] != 0

        self.draw_board()

class Tile:
    def __init__(self, value, window, x1, y1, is_preset=False):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.is_preset = is_preset  # Whether the value is preset or not
        self.is_user_input = False   # Whether the value was input by the user

    def display(self, value, position):
        font = pygame.font.SysFont("lato", 45)

        # Determine the color 
        if self.is_preset:
            color = (0, 0, 0)  # Black for preset values
        elif self.is_user_input:
            color = (255, 0, 0)  # Red for user inputted values
        else:
            color = (0, 0, 255)  # Blue for solver filled values

        text = font.render(str(value), True, color)
        self.window.blit(text, position)

def main():
    screen = pygame.display.set_mode((540, 580))
    pygame.display.set_caption("Sudoku Solver - ARYAN ADIT")
    icon = pygame.image.load("C:/Users/aryan/Desktop/DSA/naruto.jpeg")
    pygame.display.set_icon(icon)
    board = Board(screen)
    board.draw_board()

    running = True
    started_solving = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not started_solving:
                    x, y = event.pos
                    if y < 540:
                        row, col = y // 60, x // 60
                        board.select_cell((row, col))

            elif event.type == pygame.KEYDOWN:
                if not started_solving:
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        value = event.key - pygame.K_1 + 1
                        if board.selected_cell:
                            board.handle_input(board.selected_cell, value)
                    elif event.key == pygame.K_r:
                        board.generate_random_board()
                    elif event.key == pygame.K_RETURN:
                        temp_board = deepcopy(board.board)
                        if solve(temp_board):  # Check if solvable
                            started_solving = True
                            board.visualsolve()
                        else:
                            print("The current board configuration is unsolvable.")
                            board.display_message("Unsolvable board")

        pygame.display.update()

    pygame.quit()

#if __name__ == "__main__":
main()
