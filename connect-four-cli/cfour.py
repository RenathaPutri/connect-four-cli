"""
This file contains code for the game "Connect Four CLI".

Authors:
1. Renatha Putri
2. SoftwareApkDev
"""


# Importing necessary libraries


import json
import os
import random
import time
import google.generativeai as genai
from colorama import Fore, Style
from dotenv import load_dotenv


def print_instructions():
    print(Fore.GREEN + "\nWelcome to Connect Four! 🎮")
    print("How to Play:")
    print("1️⃣ Players take turns dropping tokens into columns (1-7).")
    print("2️⃣ The goal is to connect four tokens in a row (horizontal, vertical, or diagonal).")
    print("3️⃣ Choose a difficulty level: Easy, Medium, or Hard.")
    print("4️⃣ You can undo your last move by typing 'u'.")
    print("5️⃣ AI can suggest the best move for you.")
    print("6️⃣ Scores will be tracked across games.")
    print("Let's begin!\n" + Style.RESET_ALL)

def print_board(board):
    
    print(Fore.CYAN + "\n Connect Four Board")
    for row in board:
        print(Fore.YELLOW + " | ".join(row) + Style.RESET_ALL)
        print("-" * 29)

def check_winner(board, player):
    for row in range(6):
        for col in range(7):
            if col + 3 < 7 and all(board[row][col + i] == player for i in range(4)):
                return True
            if row + 3 < 6 and all(board[row + i][col] == player for i in range(4)):
                return True
            if row + 3 < 6 and col + 3 < 7 and all(board[row + i][col + i] == player for i in range(4)):
                return True
            if row - 3 >= 0 and col + 3 < 7 and all(board[row - i][col + i] == player for i in range(4)):
                return True
    return False

def ai_move(board, difficulty):
    model = genai.GenerativeModel("gemini-1.5-pro")
    available_moves = [col for col in range(7) if board[0][col] == " "]
    if difficulty == "easy":
        return random.choice(available_moves)
    prompt = f"Given the Connect Four board {board}, what is the best move? Choose from {available_moves}."
    response = model.generate_content(prompt)
    try:
        move = int(response.text.strip())
        if move in available_moves:
            return move
    except ValueError:
        pass
    return random.choice(available_moves) if available_moves else None

def suggest_move(board):
    print("AI Suggestion Mode: AI is analyzing...")
    time.sleep(1)
    return ai_move(board, "hard")

def save_score(result):
    try:
        with open("../scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = {"wins": 0, "losses": 0, "ties": 0}
    
    scores[result] += 1
    with open("../scores.json", "w") as file:
        json.dump(scores, file)

def play_game():
    print_instructions()
    board = [[" " for _ in range(7)] for _ in range(6)]
    user_symbol, ai_symbol = ('X', 'O') if random.choice([True, False]) else ('O', 'X')
    history = []
    difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
    print(f"You are {user_symbol}, AI is {ai_symbol}")
    
    while True:
        print_board(board)
        if (len(history) % 2 == 0 and user_symbol == 'X') or (len(history) % 2 == 1 and user_symbol == 'O'):
            move = input("Enter your move (1-7), 's' for suggestion, or 'u' to undo: ")
            if move.lower() == 's':
                move = suggest_move(board)
                print(f"AI suggests column {move + 1}")
            elif move.lower() == 'u':
                if history:
                    last_move = history.pop()
                    board[last_move[0]][last_move[1]] = " "
                    print("Undo successful!\n")
                    continue
                else:
                    print("No moves to undo.")
                    continue
            else:
                move = int(move) - 1
                while move not in range(7) or board[0][move] != " ":
                    move = int(input("Invalid move. Enter again: ")) - 1
        else:
            print("AI is thinking...")
            time.sleep(1)
            move = ai_move(board, difficulty)
        
        for row in range(5, -1, -1):
            if board[row][move] == " ":
                board[row][move] = user_symbol if len(history) % 2 == 0 else ai_symbol
                history.append((row, move))
                break
        
        if check_winner(board, user_symbol if len(history) % 2 == 0 else ai_symbol):
            print_board(board)
            if len(history) % 2 == 0:
                print(Fore.GREEN + "Congratulations! You win!" + Style.RESET_ALL)
                save_score("wins")
            else:
                print(Fore.RED + "AI wins! Better luck next time." + Style.RESET_ALL)
                save_score("losses")
            return

def main():
    print("Welcome to Connect Four!")

    # Configure Gemini AI API Key
    load_dotenv()
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])

    while True:
        play_game()
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()
