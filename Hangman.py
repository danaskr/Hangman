import tkinter as tk
from tkinter import messagebox
import pygame
import random


pygame.mixer.init()


correct_sound = pygame.mixer.Sound('media/correct.wav')
wrong_sound = pygame.mixer.Sound('media/wrong.wav')
win_sound = pygame.mixer.Sound('media/win.wav')
lose_sound = pygame.mixer.Sound('media/lose.wav')

WORDS = ["PYTHON", "KEYBOARD", "CHIMNYCAKE", "SCIENCE", "HANGMAN", "DANA","PALESTINE"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.configure(bg="#ADD8E6")  
        
        # Game variables
        self.secret_word = random.choice(WORDS)
        self.display_word = ["_" for _ in self.secret_word]
        self.attempts_left = 6
        self.guessed_letters = set()
        
       
        self.word_label = tk.Label(root, text=" ".join(self.display_word), font=("Arial", 24), bg="#ADD8E6")
        self.word_label.pack(pady=20)
        
        self.attempts_label = tk.Label(root, text=f"Attempts Left: {self.attempts_left}", font=("Arial", 14), bg="#ADD8E6")
        self.attempts_label.pack(pady=10)
        
        self.buttons_frame = tk.Frame(root, bg="#414f55")
        self.buttons_frame.pack(pady=10)
        
        self.create_letter_buttons()
        
        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game, font=("Arial", 12), bg="#87CEEB", fg="white", relief="flat")
        self.reset_button.pack(pady=20)
    
    def create_letter_buttons(self):
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            button = tk.Button(
                self.buttons_frame, text=letter, width=4, font=("Arial", 10), bg="#87CEEB", fg="white", relief="flat",
                command=lambda l=letter: self.guess_letter(l) #the clicking event
            )
            button.grid(row=i // 6, column=i % 6, padx=5, pady=5)

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            messagebox.showinfo("Hangman", f"You already guessed '{letter}'!")
            return
        
        self.guessed_letters.add(letter)
        if letter in self.secret_word: #correct guess
            correct_sound.play()
            self.update_display_word(letter)
            if "_" not in self.display_word: # no more to guess == win
                win_sound.play()
                messagebox.showinfo("Hangman", "You won!")
                self.reset_game()
        else: # wrong guess
            wrong_sound.play()
            self.attempts_left -= 1
            self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")
            if self.attempts_left == 0: 
                lose_sound.play()
                messagebox.showinfo("Hangman", f"You lost! The word was '{self.secret_word}'.")
                self.reset_game()
    
    def update_display_word(self, letter):
        for idx, char in enumerate(self.secret_word):
            if char == letter:
                self.display_word[idx] = letter
        self.word_label.config(text=" ".join(self.display_word))
    
    def reset_game(self):
        self.secret_word = random.choice(WORDS)
        self.display_word = ["_" for _ in self.secret_word]
        self.attempts_left = 6
        self.guessed_letters.clear()
        
        self.word_label.config(text=" ".join(self.display_word))
        self.attempts_label.config(text=f"Attempts Left: {self.attempts_left}")


root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
