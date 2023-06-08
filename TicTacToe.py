from keyboard import read_key
from colorama import init as colorama_init, Fore, Style
import os


colorama_init()

INTER = {
    0: " ",
    1: f"{Fore.BLUE}X{Style.RESET_ALL}",
    2: f"{Fore.CYAN}O{Style.RESET_ALL}"
}


def clear():
    os.system('cls')


def interpreter(symbol: int):
    return INTER[symbol]


def launching_message():
    print(f"   Welcome to {Fore.RED}Tic{Fore.GREEN}Tac{Fore.BLUE}Toe{Style.RESET_ALL}!")
    print()
    print(" Choose a mark for Player 1:")
    print(f"  Type [{Style.BRIGHT}1{Style.RESET_ALL}] for {interpreter(1)}")
    print(f"  Type [{Style.BRIGHT}2{Style.RESET_ALL}] for {interpreter(2)}")

    return 1 if read_key() == "1" else 2


class TicTacToe:
    def __init__(self):
        self.game_finished = False
        self.P1, self.P2 = 1, 2
        self.current_turn = self.P1
        self.GRID_WIDTH, self.GRID_HEIGHT = 3, 3
        self.field = []
        for y in range(self.GRID_HEIGHT):
            self.field.append([0 for _ in range(self.GRID_WIDTH)])

    def get_tile(self, x):
        return self.field[(x - 1) // 3][(x - 1) % 3]

    def set_tile(self, x, p):
        self.field[(x - 1) // 3][(x - 1) % 3] = p

    def print_field(self, message=""):
        clear()

        print(f"  {Fore.RED}Tic{Fore.GREEN}Tac{Fore.BLUE}Toe{Style.RESET_ALL}"
              f"     Press numbers {Style.BRIGHT}1-9{Style.RESET_ALL} to place a mark.")

        #         ┌───┬───┬───┐
        string = ["\u2500" * 3 for _ in range(self.GRID_WIDTH)]
        print("\u250c", "\u252c".join(string), f"\u2510"
                                               f"   Press {Style.BRIGHT}Q{Style.RESET_ALL} to exit the game.", sep="")

        for y in range(self.GRID_HEIGHT - 1, -1, -1):
            #     │7  │8  │9  │
            string = [f"{y * self.GRID_HEIGHT + x + 1}  " for x in range(self.GRID_WIDTH)]
            print("\u2502", "\u2502".join(string), "\u2502", sep="")

            #     │ X │ O │ X │
            string = [f" {interpreter(self.field[y][x])} " for x in range(self.GRID_WIDTH)]
            print("\u2502", "\u2502".join(string), "\u2502", sep="", end="")
            print(f"   P1 is {interpreter(self.P1)}s." if y == self.GRID_HEIGHT - 1 else "")

            #     │   │   │   │
            string = ["   " for _ in range(self.GRID_WIDTH)]
            print("\u2502", "\u2502".join(string), "\u2502", sep="", end="")
            print(f"   P2 is {interpreter(self.P2)}s." if y == self.GRID_HEIGHT - 1 else "")

            if y:
                # ├───┼───┼───┤
                string = ["\u2500" * 3 for _ in range(self.GRID_WIDTH)]
                print("\u251c", "\u253c".join(string), "\u2524", sep="", end="")
                print(f"   It's {interpreter(self.current_turn)}'s turn." if y == self.GRID_HEIGHT - 1 else "")

        #         └───┴───┴───┘
        string = ["\u2500" * 3 for _ in range(self.GRID_WIDTH)]
        print("\u2514", "\u2534".join(string), "\u2518", sep="")

        print(message)

    def switch_turn(self):
        if self.current_turn == self.P1:
            self.current_turn = self.P2
        else:
            self.current_turn = self.P1

    def win_check(self):
        lines = []
        for row_id in range(self.GRID_WIDTH):
            lines.append(self.field[row_id])  # Add rows.
            lines.append([self.field[x][row_id] for x in range(self.GRID_HEIGHT)])  # Add columns.

        lines.append([self.field[x][x] for x in range(self.GRID_WIDTH)])  # Add main diagonal.
        lines.append([self.field[x][self.GRID_WIDTH - 1 - x] for x in range(self.GRID_WIDTH)])  # Add side diagonal.

        for line in lines:
            if 0 not in line:
                if all(x == line[0] for x in line):
                    return True

        return False

    def draw_check(self):
        has_empty = False
        for row in self.field:
            if 0 in row:
                has_empty = True

        return not has_empty

    def restart(self):
        self.field = []
        for y in range(self.GRID_HEIGHT):
            self.field.append([0 for _ in range(self.GRID_WIDTH)])

        self.print_field()

        self.current_turn = self.P1
        self.game_finished = False

    def play(self):
        if launching_message() != 1:
            self.P1 = 2
            self.P2 = 1

        self.current_turn = self.P1

        self.print_field()

        while True:
            key = read_key()

            if key == "q":
                break

            if key == "r" and self.game_finished:
                self.restart()

            if self.game_finished:
                continue

            if key == "0":
                continue

            try:
                key = int(read_key())
            except ValueError:
                continue

            if self.get_tile(key):
                self.print_field("Place already taken.")
            else:
                self.set_tile(key, self.current_turn)

                if self.win_check():
                    self.print_field(f"   {interpreter(self.current_turn)}s WIN")
                    print(f"\nPress {Style.BRIGHT}R{Style.RESET_ALL} to play another.")
                    self.game_finished = True
                elif self.draw_check():
                    self.print_field("    DRAW!")
                    print(f"\nPress {Style.BRIGHT}R{Style.RESET_ALL} to play another.")
                    self.game_finished = True
                else:
                    self.switch_turn()
                    self.print_field()
