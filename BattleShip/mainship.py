import tkinter as tk
from tkinter import messagebox
import random

# Initialize the board size and number of ships
board_size = 7  # Increased board size
ship_lengths = [2, 3, 4]  # Possible lengths of ships
num_ships = 5  # Increased number of ships

# Function to create the game board
def create_board():
    return [['~' for _ in range(board_size)] for _ in range(board_size)]

# Function to place ships randomly on the board
def place_ships():
    ships = []
    for _ in range(num_ships):
        while True:
            length = random.choice(ship_lengths)  # Randomly choose a ship length
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                row = random.randint(0, board_size - 1)
                col = random.randint(0, board_size - length)
                if all(board[row][col + i] == '~' for i in range(length)):  # Check if space is clear
                    for i in range(length):
                        board[row][col + i] = 'S'
                    ships.append((row, col, orientation, length))
                    break
            else:  # vertical
                row = random.randint(0, board_size - length)
                col = random.randint(0, board_size - 1)
                if all(board[row + i][col] == '~' for i in range(length)):  # Check if space is clear
                    for i in range(length):
                        board[row + i][col] = 'S'
                    ships.append((row, col, orientation, length))
                    break
    return ships

# Function to update the GUI board display
def update_board_gui():
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == '~' or board[i][j] == 'S':
                board_label[i][j].config(text="🌊", state="normal", bg="#99d9ea", fg="blue", relief="raised")  # Water (not revealed)
            elif board[i][j] == 'X':
                board_label[i][j].config(text="❌", bg="#ff4d4d", fg="white", relief="sunken")  # Miss (X)
            elif board[i][j] == 'B':
                board_label[i][j].config(text="🚢", bg="#4caf50", fg="white", relief="sunken")  # Hit (Ship)

# Function to handle the player's guess
def make_guess(row, col):
    global turns_left, score
    if board[row][col] == 'X' or board[row][col] == 'B':
        result_label.config(text="You've already guessed that spot!", fg="orange")
        return

    if board[row][col] == 'S':
        board[row][col] = 'B'  # Hit
        result_label.config(text="Direct hit! You've found a ship!", fg="green")
        score += 10
        turns_left += 1  # Grant an extra turn for a hit
    else:
        board[row][col] = 'X'  # Miss
        result_label.config(text="You missed! -1 turn.", fg="red")
        score -= 1
        turns_left -= 1  # Lose a turn for a miss

    update_board_gui()
    turns_label.config(text=f"Turns left: {turns_left}")
    score_label.config(text=f"Score: {score}")

    if turns_left == 0 or all(board[r][c] == 'B' for r, c, _, _ in ships):
        end_game()

# Function to start the game from the main menu
def start_game():
    global board, ships, turns_left, score
    turns_left = 10  # Reduced number of turns to increase difficulty
    score = 0
    result_label.config(text="Game Started! Hunt down the ships!", fg="blue")
    turns_label.config(text=f"Turns left: {turns_left}")
    score_label.config(text=f"Score: {score}")

    # Place ships randomly and reset the board
    board = create_board()
    ships = place_ships()
    update_board_gui()

    # Show the game screen
    main_menu_frame.pack_forget()
    game_frame.pack()

# Function to end the game
def end_game():
    if turns_left == 0:
        result_label.config(text=f"Game Over! You're out of turns!", fg="red")
    else:
        result_label.config(text=f"Victory! You've sunk all ships!", fg="green")
    disable_board()

# Function to disable the board after the game is over
def disable_board():
    for i in range(board_size):
        for j in range(board_size):
            board_label[i][j].config(state="disabled")

# Function to return to the main menu
def back_to_menu():
    game_frame.pack_forget()
    main_menu_frame.pack()

# Function to display "How to Play" instructions
def show_instructions():
    instructions = (
        "How to Play Battleship:\n\n"
        "1. You are playing on a 7x7 grid (the ocean).\n"
        "2. Ships of varying lengths (2 to 4) are hidden randomly on the grid.\n"
        "3. Click a cell to guess the ship's location.\n"
        "4. You have 10 turns to sink all the ships!\n"
        "5. A hit is marked with 🚢, and a miss is marked with ❌.\n"
        "6. A hit grants you an extra turn, but a miss takes away one."
    )
    messagebox.showinfo("How to Play", instructions)

# Function to exit the game
def exit_game():
    window.quit()

# Initialize the main window
window = tk.Tk()
window.title("Battleship Game")
window.geometry("500x500")
window.config(bg="#1e3d59")

# Main menu frame with enhanced visuals
main_menu_frame = tk.Frame(window, bg="#004466")

# Title label in the main menu with stylized appearance
title_label = tk.Label(main_menu_frame, text="⚓ Battleship Game ⚓", font=("Helvetica", 28, "bold"), bg="#004466", fg="white")
title_label.pack(pady=30)

# Create a fun and interactive Start button
start_button = tk.Button(main_menu_frame, text="🌊 Start Game 🌊", font=("Helvetica", 16), bg="#4caf50", fg="white", relief="raised", command=start_game)
start_button.pack(pady=15)

# Create an animated Help button for game instructions
help_button = tk.Button(main_menu_frame, text="🛈 How to Play", font=("Helvetica", 16), bg="#ffcc00", fg="black", relief="raised", command=show_instructions)
help_button.pack(pady=15)

# Create a fun Exit button
exit_button = tk.Button(main_menu_frame, text="❌ Exit Game", font=("Helvetica", 16), bg="#f44336", fg="white", relief="raised", command=exit_game)
exit_button.pack(pady=15)

main_menu_frame.pack()

# Game frame (initially hidden)
game_frame = tk.Frame(window, bg="#1e3d59")

# Create the labels for the game board (interactive buttons)
board_label = [[tk.Button(game_frame, text="~", width=4, height=2, font=("Helvetica", 16), bg="#99d9ea", fg="white", relief="ridge",
                          command=lambda i=i, j=j: make_guess(i, j)) for j in range(board_size)] for i in range(board_size)]
for i in range(board_size):
    for j in range(board_size):
        board_label[i][j].grid(row=i, column=j, padx=5, pady=5)

# Result and turns labels
result_label = tk.Label(game_frame, text="Press Start to begin!", font=("Helvetica", 14, "bold"), bg="#1e3d59", fg="white")
result_label.grid(row=5, column=0, columnspan=5)

turns_label = tk.Label(game_frame, text=f"Turns left: 10", font=("Helvetica", 14), bg="#1e3d59", fg="white")
turns_label.grid(row=6, column=0, columnspan=5)

# Score label
score_label = tk.Label(game_frame, text="Score: 0", font=("Helvetica", 14), bg="#1e3d59", fg="white")
score_label.grid(row=7, column=0, columnspan=5)

# Back button to return to the main menu
back_button = tk.Button(game_frame, text="Back to Menu", font=("Helvetica", 12), bg="#ffcc00",
