import random
import os
from enum import Enum
import math
import sys


# https://www.delftstack.com/de/howto/python/python-clear-console/
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
        full_wordlist = f.readlines()
        full_wordlist = [line.rstrip() for line in full_wordlist]

    def __init__(self):
        """Creates a new instance of Hangman. The number of players can be varied using the num_player parameter."""
        self.state = State.START
        self.active_team = 0
        self.current_wordlist = random.sample(self.full_wordlist, 25)
        self.wordlist = self.current_wordlist
        # Rote Wörter rausfiltern
        self.red_words = random.sample(self.current_wordlist, 9)
        self.update_list = set(self.red_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        # Blaue Wörter rausfiltern
        self.blue_words = random.sample(self.current_wordlist, 8)
        self.update_list = set(self.blue_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        # Weiße Wörter rausfiltern
        self.white_words = random.sample(self.current_wordlist, 7)
        self.update_list = set(self.white_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        # Schwarzes Wort rausfiltern
        self.black_word = random.sample(self.current_wordlist, 1)
        self.update_list = set(self.black_word)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]

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
                response = self.ask_for_word()
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
        self.current_wordlist = random.sample(self.full_wordlist, 25)
        self.wordlist = self.current_wordlist
        # Rote Wörter rausfiltern
        self.red_words = random.sample(self.current_wordlist, 9)
        self.update_list = set(self.red_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        # Blaue Wörter rausfiltern
        self.blue_words = random.sample(self.current_wordlist, 8)
        self.update_list = set(self.blue_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        # Weiße Wörter rausfiltern
        self.white_words = random.sample(self.current_wordlist, 7)
        self.update_list = set(self.white_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        # Schwarzes Wort rausfiltern
        self.black_word = random.sample(self.current_wordlist, 1)
        self.update_list = set(self.black_word)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]

    def explain_rules(self):
        """Prints an explanation of the rules."""
        clearConsole()
        print("Herzlichen Glückwunsch! Ihr seid Ermittler eines Geheimdienstes und sucht nach Euren Agenten.\n"
              "Diese Agenten verstecken sich hinter den 25 aufgeführten Wörtern, die gleich zu sehen sind.\n"
              "Die Wortliste ist zufällig aufgeteilt in 9 rote Agenten, 8 blaue Agenten, 7 unbeteiligte Zuschauer und einen Attentäter, \n"
              "doch nur die Spymaster wissen, wer zu welchem Team gehört. \n"
              "Teilt die Spieler den Teams Rot und Blau zu. Der Spymaster wird vom Computer übernommen.\n"
              "Zusammen mit dem jeweiligen Spymaster spielt ihr in den Teams gegeneinander.\n"
              "Team Rot beginnt und erhält vom Spymaster einen Hinweis gestellt.\n"
              "Dieser besteht aus einem Begriff, der eine oder mehrere aufgelistete Wörter in Assoziation stellt.\n"
              "Wieviele Wörter zu erraten sind, teilt der Spymaster mit (bspw. Speed 2).\n"
              "Nach Abschluss des Zuges, ist das nächste Team an der Reihe.\n"
              "Ein Team darf immer ein Mal mehr raten, als die Zahlvorgabe ist (Speed 2 -> 3 Mal raten)."
              "Ist ein Team sich zu unsicher, darf es jederzeit aufhören zu raten und das nächste Team beginnt den Zug.\n"
              "Mit dem Erraten der Wörter werden diese mit der Farbe des entsprechenden Agenten versehen - \n"
              "Team Rot kann also auch Karten von Team Blau erraten und anders herum.\n"
              "Unbeteiligte Zuschauer werden bei Erraten lediglich als solche gekennzeichnet.\n"
              "Ziel ist es, als erstes Team alle eigenen Wörter bzw. Agenten korrekt gefunden zu haben.\n"
              "Errät ein Team jedoch versehentlich den Attentäter, gewinnt automatisch das andere Team.\n"
              "Viel Erfolg!\n")

    def print_current_game_state(self):
        """Prints letters already guessed, open letters and player scores."""
        """ KOMMT!" """

    def spymaster(self):
        """ KOMMT!" """

    def ask_for_word(self):
        """Prints a prompt to guess a word and returns the user's input."""
        if self.active_team == 0:
            self.actual_active_team = str("Rot")
        else:
            self.actual_active_team = str("Blau")
        print(f"Team{self.actual_active_team} ist an der Reihe!")
        print("Welches Wort rätst du?")
        return input(">").upper()

    def evaluate_answer(self, user_input: str):
        """
        Evaluates the given user input and returns the corresponding next game state.

        If the user input is a single letter, it will be evaluated against the searched word and depending on the
        validity, the game's state is updated.
        If the user input is more than a single letter, it is interpreted as a command and appropriate actions are
        performed, depending on the command.
        """
        user_input = user_input.lower()

        # some command was entered, instead of a letter
        if user_input not in self.wordlist:
            if user_input == "lösen":
                return State.REQUEST_SOLUTION

            if user_input == "regeln":
                return State.DISPLAY_RULES

            clearConsole()
            print("Es sind nur Wörter aus der dargestellten Wortliste als Antwort möglich.")
            print(self.wordlist)
            return State.PLAY_TURN
        else:
            print("yay")

        # check guessed letter
        clearConsole()
        if user_input in self.wrong_letters.union(self.identified_letters):
            print('Der Buchstabe wurde bereits geraten, versuche es mit einem anderen Buchstaben.')
        elif user_input in self.word:
            print("Gut geraten!")
            self.identified_letters.add(user_input.lower())
        else:
            self.wrong_letters.add(user_input.lower())
            print(f"Leider nein. Spieler{self.active_player + 1} bekommt {Hangman.WRONG_GUESS_PENALTY} Strafpunkt.")
            print("Ihr habt bereits folgende Buchstaben falsch geraten:", ",".join(sorted(self.wrong_letters)))
            print()

            self.errors[self.active_player] += Hangman.WRONG_GUESS_PENALTY
            self.next_player()

        return State.PLAY_TURN

    def announce_winners(self):
        """ KOMMT!" """

    def ask_to_play_again(self):
        """Asks the players whether they want to play again and returns the corresponding next game state."""
        again = input("Möchtet ihr nochmal spielen? (ja/nein)")
        if again.lower().strip() == "ja":
            return State.PREPARE_ROUND
        else:
            return State.END

    def determine_winners(self):
        """ KOMMT!" """


def main():
    game = Codenames()
    game.run()


if __name__ == "__main__":
    main()
