import random
import os
from enum import Enum
import sys
import requests
from colorama import Fore

api_url = "https://api.conceptnet.io/query?node=/c/en/"
query = "&rel=/r/RelatedTo&offset=0&limit=50"

# https://www.delftstack.com/de/howto/python/python-clear-console/
def clearConsole():
    command = 'clear' if os.name not in ('nt', 'dos') else 'cls'  # If Machine is running on Windows, use cls
    os.system(command)

def abfragen(word):
    api_url = "https://api.conceptnet.io/query?node=/c/en/"
    query = "&rel=/r/RelatedTo&offset=0&limit=1000"
    query_word = word
    response = requests.get(api_url + query_word + query)
    asJson = response.json()
    related = asJson["edges"]

    testarray = []
    for x in related:
        word = x["end"]["label"]
        if word != query_word and word not in testarray and " " not in word:
            testarray.append(word)
    return testarray

class State(Enum):
    START = 0,
    PREPARE_ROUND = 1,
    DISPLAY_RULES = 2,
    PLAY_TURN = 3,
    PLAY_AGAIN = 4,
    GAME_OVER = 5
    END = -1,


class Codenames():
    with open("wordlist-eng.txt", "r") as f:
        full_wordlist = f.readlines()
        full_wordlist = [line.rstrip() for line in full_wordlist]

    def __init__(self):
        """Creates a new instance of Codenames."""
        self.state = State.START
        self.active_team = 0
        self.current_wordlist = random.sample(self.full_wordlist, 25)
        for i in range(len(self.current_wordlist)):
            self.current_wordlist[i] = self.current_wordlist[i].lower()
        self.wordlist = self.current_wordlist
        """Rote Wörter rausfiltern"""
        self.red_words = random.sample(self.current_wordlist, 9)
        self.update_list = set(self.red_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        """Blaue Wörter rausfiltern"""
        self.blue_words = random.sample(self.current_wordlist, 8)
        self.update_list = set(self.blue_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        """Weiße Wörter rausfiltern"""
        self.white_words = random.sample(self.current_wordlist, 7)
        self.update_list = set(self.white_words)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        """Schwarzes Wort rausfiltern"""
        self.black_word = random.sample(self.current_wordlist, 1)
        self.update_list = set(self.black_word)
        self.current_wordlist = [x for x in self.current_wordlist if x not in self.update_list]
        """Punktestände"""
        self.red_score = 9
        self.blue_score = 8
        """Bibliotheken anlegen"""
        dict_red = {}
        for i in self.red_words:
            abfrage = abfragen(i)
            for ab in abfrage:
                isThere = dict_red.get(ab)
                if isThere is None:
                    dict_red[ab] = 1
                else:
                    oldValue = dict_red[ab]
                    newValue = oldValue + 1
                    dict_red[ab] = newValue
        self.dict_red_sorted = sorted(dict_red.items(), key=lambda x: x[1], reverse=True)
        self.dict_red_sorted_names = []
        for i in self.dict_red_sorted:
            self.dict_red_sorted_names.append(i[0])

        dict_blue = {}
        for i in self.blue_words:
            abfrage = abfragen(i)
            for ab in abfrage:
                isThere = dict_blue.get(ab)
                if isThere is None:
                    dict_blue[ab] = 1
                else:
                    oldValue = dict_blue[ab]
                    newValue = oldValue + 1
                    dict_blue[ab] = newValue
        self.dict_blue_sorted = sorted(dict_blue.items(), key=lambda x: x[1], reverse=True)
        self.dict_blue_sorted_names = []
        for i in self.dict_blue_sorted:
            self.dict_blue_sorted_names.append(i[0])

        dict_white = {}
        for i in self.white_words:
            abfrage = abfragen(i)
            for ab in abfrage:
                isThere = dict_white.get(ab)
                if isThere is None:
                    dict_white[ab] = 1
                else:
                    oldValue = dict_white[ab]
                    newValue = oldValue + 1
                    dict_white[ab] = newValue
        self.dict_white_sorted = sorted(dict_white.items(), key=lambda x: x[1], reverse=True)
        self.dict_white_sorted_names = []
        for i in self.dict_white_sorted:
            self.dict_white_sorted_names.append(i[0])

        dict_black = {}
        for i in self.black_word:
            abfrage = abfragen(i)
            for ab in abfrage:
                isThere = dict_black.get(ab)
                if isThere is None:
                    dict_black[ab] = 1
                else:
                    oldValue = dict_black[ab]
                    newValue = oldValue + 1
                    dict_black[ab] = newValue
        self.dict_black_sorted = sorted(dict_black.items(), key=lambda x: x[1], reverse=True)
        self.dict_black_sorted_names = []
        for i in self.dict_black_sorted:
            self.dict_black_sorted_names.append(i[0])

    def run(self):
        """Starts the game."""
        self.state = State.START
        while True:
            if self.state == State.START:
                clearConsole()
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
                if len(self.black_word) == 0:
                    self.state = State.GAME_OVER
                elif len(self.red_words) == 0:
                    self.state = State.END
                elif len(self.blue_words) == 0:
                    self.state = State.END
                else:
                    self.print_current_game_state()
                    response = self.ask_for_word()
                    self.state = self.evaluate_answer(response)
                    continue

            if self.state == State.PLAY_AGAIN:
                self.state = self.ask_to_play_again()
                continue

            if self.state == State.END:
                self.announce_winners()
                self.ask_to_play_again()

            if self.state == State.GAME_OVER:
                self.announce_winners2()
                self.ask_to_play_again()

    def next_team(self):
        """Changes the active team."""
        self.active_team = (self.active_team + 1) % 2

    def prepare_round(self):
        """Prepares the next round."""
        self.active_team = 0
        self.current_wordlist = random.sample(self.full_wordlist, 25)
        for i in range(len(self.current_wordlist)):
            self.current_wordlist[i] = self.current_wordlist[i].lower()
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
        # Punktestände
        self.red_score = 9
        self.blue_score = 8

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
              "Ein Team darf immer ein Mal mehr raten, als die Zahlvorgabe ist (Speed 2 -> 3 Mal raten).\n"
              "Ist ein Team sich zu unsicher, darf es jederzeit aufhören zu raten und das nächste Team beginnt den Zug.\n"
              "Mit dem Erraten der Wörter werden diese mit der Farbe des entsprechenden Agenten versehen - \n"
              "Team Rot kann also auch Karten von Team Blau erraten und anders herum.\n"
              "Unbeteiligte Zuschauer werden bei Erraten lediglich als solche gekennzeichnet.\n"
              "Ziel ist es, als erstes Team alle eigenen Wörter bzw. Agenten korrekt gefunden zu haben.\n"
              "Errät ein Team jedoch versehentlich den Attentäter, gewinnt automatisch das andere Team.\n"
              "Viel Erfolg!\n")

    def print_current_game_state(self):
        """Prints the wordlist and team scores."""
        print(self.wordlist)
        print(Fore.RED + "Rote " + Fore.WHITE + "Agenten: ", self.red_score)
        print(Fore.BLUE + "Blaue " + Fore.WHITE + "Agenten: ", self.blue_score)

    def ask_for_word(self):
        """Prints a prompt to guess a word and returns the user's input."""
        if self.active_team == 0:
            self.actual_active_team = str("Rot")
        else:
            self.actual_active_team = str("Blau")
        print(f"Team {self.actual_active_team} ist an der Reihe!")
        if self.active_team == 0:
            for x in self.dict_red_sorted:
                if x[0] not in self.red_words and x[0] not in self.dict_blue_sorted_names and x[0] not in self.dict_white_sorted_names and x[0] not in self.dict_black_sorted_names:
                    print(x)
                break
        print("Welches Wort ratet ihr?")
        return input(">").upper()

    def evaluate_answer(self, user_input: str):
        ##user_input = user_input.lower()

        ##if user_input not in self.wordlist:

            ##if user_input == "regeln":
                ##return State.DISPLAY_RULES

            ##print("Es sind nur Wörter aus der dargestellten Wortliste als Antwort möglich.")

        # check guessed word
        """clearConsole()"""
        """KOMMT!"""
        """self.next_team()"""

        # check guessed word
        clearConsole()
        if self.active_team == 0:
            if user_input in self.red_words:
                self.wordlist.remove(user_input)
                self.red_words.remove(user_input)
                self.red_score -= 1
                print(user_input, " war ein roter Agent!")
                self.next_team()
            elif user_input in self.blue_words:
                self.wordlist.remove(user_input)
                self.blue_words.remove(user_input)
                self.blue_score -= 1
                print(user_input, " war ein blauer Agent!")
                self.next_team()
            elif user_input in self.white_words:
                self.wordlist.remove(user_input)
                self.white_words.remove(user_input)
                print(user_input, " war ein unbeteiliger Zuschauer!")
                self.next_team()
            elif user_input in self.black_word:
                self.wordlist.remove(user_input)
                self.black_word.remove(user_input)
            else:
                self.next_team()
        else:
            if user_input in self.blue_words:
                self.wordlist.remove(user_input)
                self.blue_words.remove(user_input)
                self.blue_score -= 1
                self.next_team()
            elif user_input in self.red_words:
                self.wordlist.remove(user_input)
                self.red_words.remove(user_input)
                self.red_score -= 1
                self.next_team()
            elif user_input in self.white_words:
                self.wordlist.remove(user_input)
                self.white_words.remove(user_input)
                self.next_team()
            elif user_input in self.black_word:
                self.wordlist.remove(user_input)
                self.black_word.remove(user_input)
            else:
                self.next_team()
        return State.PLAY_TURN

    def announce_winners(self):
        print("Ihr habt alle Agenten identifiziert.\nTeam " + self.actual_active_team + " gewinnt!")

    def announce_winners2(self):
        if self.actual_active_team == "Rot":
            print("Ihr seid dem Attentäter zum Opfer gefallen.\nTeam Blau gewinnt!")
        else:
            print("Ihr seid dem Attentäter zum Opfer gefallen.\nTeam Rot gewinnt!")

    def ask_to_play_again(self):
        """Asks the players whether they want to play again and returns the corresponding next game state."""
        again = input("Möchtet ihr nochmal spielen? (ja/nein)\n")
        if again.lower().strip() == "ja":
            self.state = State.START
        else:
            sys.exit()

    def determine_winners(self):
        """ KOMMT!" """


def main():
    game = Codenames()
    game.run()


if __name__ == "__main__":
    main()
