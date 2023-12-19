import tkinter as tk
from tkinter import simpledialog, messagebox
import time
from database import TicTacToeDB  # Import the database module

class TicTacToe:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")

        self.colors = {'X': 'blue', 'O': 'orange'}
        
        self.player_names = self.get_player_names()
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None, None, None] for _ in range(3)]
        self.scores = {self.player_names['X']: 0, self.player_names['O']: 0}

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.window, text='', font=('normal', 20), width=8, height=4,
                                              command=lambda row=i, col=j: self.button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5, ipadx=10, ipady=10)

        button_frame = tk.Frame(self.window)
        button_frame.grid(row=3, column=0, columnspan=3)
        
        self.quit_button = tk.Button(button_frame, text='Quit', command=self.window.destroy, bg='red', fg='white')
        self.quit_button.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10)

        self.score_label = tk.Label(self.window, font=('normal', 12), bg='yellow')
        self.score_label.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

        self.update_scores()

    def get_player_names(self):
        player_frame = tk.Frame(self.window, bg='cyan')
        player_frame.grid(row=5, column=0, columnspan=3)
        
        player1_label = tk.Label(player_frame, text="Enter the name for Player 1:", bg='cyan')
        player1_label.grid(row=0, column=0, padx=5, pady=5)
        player1_entry = tk.Entry(player_frame, bg='lightblue')
        player1_entry.grid(row=0, column=1, padx=5, pady=5)

        player2_label = tk.Label(player_frame, text="Enter the name for Player 2:", bg='cyan')
        player2_label.grid(row=1, column=0, padx=5, pady=5)
        player2_entry = tk.Entry(player_frame, bg='lightblue')
        player2_entry.grid(row=1, column=1, padx=5, pady=5)

        submit_button = tk.Button(player_frame, text="Submit", command=lambda: self.submit_names(player1_entry.get(), player2_entry.get(), player_frame), bg='green', fg='white')
        submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10)

        self.window.wait_window(player_frame)  # Wait for the player name input window to be closed
        return {'X': self.player1_name, 'O': self.player2_name}

    def submit_names(self, player1_name, player2_name, player_frame):
        self.player1_name = player1_name
        self.player2_name = player2_name
        player_frame.destroy()

    def button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, bg=self.colors[self.current_player])
            self.animate_button(row, col)
            
            if self.check_winner(row, col):
                winner_name = self.player_names[self.current_player]
                self.show_winning_animation(row, col)
                messagebox.showinfo("Game Over", f"{winner_name} wins!", icon='info')
                self.scores[winner_name] += 1
                self.update_scores()
                self.db.save_score(self.player_names['X'], self.scores[self.player_names['X']], self.player_names['O'], self.scores[self.player_names['O']])
                self.reset_game()
                self.delayed_start_next_round()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a tie!", icon='info')
                self.reset_game()
                self.delayed_start_next_round()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, row, col):
        # Check row
        if all(self.board[row][i] == self.current_player for i in range(3)):
            return True
        # Check column
        if all(self.board[i][col] == self.current_player for i in range(3)):
            return True
        # Check diagonals
        if row == col and all(self.board[i][i] == self.current_player for i in range(3)):
            return True
        if row + col == 2 and all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def reset_game(self):
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', bg='SystemButtonFace')

    def update_scores(self):
        score_text = f"Score: {self.player_names['X']} {self.scores[self.player_names['X']]} - {self.scores[self.player_names['O']]} {self.player_names['O']}"
        self.score_label.config(text=score_text)

    def animate_button(self, row, col):
        for i in range(1, 6):
            self.window.update()
            time.sleep(0.05)
            self.buttons[row][col].config(bg='white')
            self.window.update()
            time.sleep(0.05)
            self.buttons[row][col].config(bg=self.colors[self.current_player])

    def show_winning_animation(self, row, col):
        winning_combinations = [
            [(row, i) for i in range(3)],  # row
            [(i, col) for i in range(3)],  # column
            [(i, i) for i in range(3)],  # diagonal \
            [(i, 2 - i) for i in range(3)]  # diagonal /
        ]

        for combination in winning_combinations:
            if (row, col) in combination:
                for i, j in combination:
                    self.buttons[i][j].config(bg='yellow')
                    self.window.update()
                    time.sleep(0.2)
                    self.buttons[i][j].config(bg=self.colors[self.current_player])
                    self.window.update()
                    time.sleep(0.2)

    def delayed_start_next_round(self):
        self.window.update()
        time.sleep(2)
        self.reset_game()
        self.current_player = 'X'
        self.update_scores()

if __name__ == "__main__":
    db = TicTacToeDB()
    game = TicTacToe(db)
    game.window.mainloop()
    db.close_connection()
