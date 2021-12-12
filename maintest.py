import random
import os
from enum import Enum
import math
import sys

#https://www.delftstack.com/de/howto/python/python-clear-console/
def clearConsole():
    command = 'clear' if os.name not in ('nt', 'dos') else 'cls'  # If Machine is running on Windows, use cls
    os.system(command)

class State(Enum):
  START = 0,
  PREPARE_ROUND = 1,
  DISPLAY_RULES = 2,
  PLAY_TURN = 3,
  PLAY_AGAIN = 4,
  END = -1,

class Codenames():
  with open("wordlist-eng.txt", "r") as f:
    ganze_wortliste = f.readlines()
    ganze_wortliste = [line.rstrip() for line in ganze_wortliste]

  def __init__(self):
      """Creates a new instance of Hangman. The number of players can be varied using the num_player parameter."""
      self.state = State.START

      self.active_team = 0
      self.wortliste = random.sample(Codenames.ganze_wortliste, 25)
      self.wortliste2 = self.wortliste
      self.red_words = random.sample(self.wortliste, 9)
      self.wortliste = self.wortliste - [self.red_words]
      self.blue_words = random.sample(self.wortliste, 8)
      self.wortliste = self.wortliste - [self.blue_words]
      self.white_words = random.sample(self.wortliste, 7)
      self.wortliste = self.wortliste - [self.white_words]
      self.black_word = self.wortliste[0]
      print(wortliste)

  def run(self):
    """Starts the game."""
    self.state = State.START
    while True:
      if self.state == State.START:
        print("Hallo! Willkommen bei Codenames! Möchtest du erst die Regeln erfahren? (ja/nein)")
        response = input('>')
        if response.lower() == 'ja':
          self.state = State.DISPLAY_RULES
        else:
          self.state = State.PREPARE_ROUND
        continue

      if self.state == State.DISPLAY_RULES:
        self.explain_rules()
        self.state = State.PLAY_TURN
        continue

      if self.state == State.PREPARE_ROUND:
        self.prepare_round()
        self.state = State.PLAY_TURN
        continue

      if self.state == State.PLAY_TURN:
        self.print_current_game_state()
        response = self.ask_for_letter()
        self.state = self.evaluate_answer(response)
        continue

      if self.state == State.PLAY_AGAIN:
        self.state = self.ask_to_play_again()
        continue

      if self.state == State.END:
        self.announce_winners()
        print("Okay! Bye-bye!")
        sys.exit()

  def next_team(self):
      """Changes the active team."""
      self.active_team = (self.active_team + 1) % 2

  def prepare_round(self):
      """Prepares the next round by setting a new word to guess and resetting the guessed letters."""
      self.next_team()
      self.wortliste = random.sample(ganze_wortliste, 25)
      self.identified_letters = set()
      self.wrong_letters = set()

  def explain_rules(self):
      """Prints an explanation of the rules."""
      clearConsole()
      print("Das Spiel funktioniert so: Es gibt zwei Spieler und den Computer.\n"
            "Der Computer denkt sich ein Wort aus und die Spieler müssen es erraten.\n"
            "Wenn ein Spieler am Zug ist, darf er einen Buchstaben raten.\n"
            "Wenn der Buchstabe im Wort enthalten ist, darf der Spieler nochmal raten, \n"
            "ansonsten ist der andere Spieler an der Reihe.\n"
            "Für jeden falsch geratenen Buchstaben gibt es 1 Strafpunkt.\n"
            "Wenn ihr das Wort lösen möchtet, schreibt 'lösen'.\n"
            "Wenn ihr die Regeln nochmal lesen möchtet, schreibt 'Regeln'.\n"
            "Achtung! Bei falscher Lösung gibt es 3 Strafpunkte! "
            "Wer das Wort rät, bekommt 5 Strafpunkte abgezogen."
            "Wer am Ende die wenigsten Strafpunkte hat, gewinnt! , gewinnt! Viel Spaß :)")

  def print_current_game_state(self):
      """Prints letters already guessed, open letters and player scores."""
      for i in range(5):
        print("\t\t".join(wortliste[i * 5:i * 5 + 5]))

  def spymaster(self):

  def ask_for_word(self):
      """Prints a prompt to guess a word and returns the user's input."""
      print(f"Team{self.active_team + 1} ist an der Reihe!")
      print("Welches Wort rätst du?")
      return input(">").upper()

  def announce_winners(self):


  def ask_to_play_again(self):
    """Asks the players whether they want to play again and returns the corresponding next game state."""
    again = input("Möchtet ihr nochmal spielen? (ja/nein)")
    if again.lower().strip() == "ja":
      return State.PREPARE_ROUND
    else:
      return State.END

  def determine_winners(self):



def main():
  game = Codenames()
  game.run()

if __name__ == "__main__":
    main()
