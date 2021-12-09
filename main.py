import random

#
regeln_anzeigen = input("Regeln anzeigen? (j/n)\n")
if regeln_anzeigen == "j":
  print("Regeln blablabla")
spielstart = input("Mit dem Spiel beginnen? (j/n)\n")

if regeln_anzeigen == "n" or spielstart == "j":
  # Wortliste aus Datei öffnen
  with open("wordlist-eng.txt", "r") as f:
    f_contents = f.readlines()
    f_contents = [line.rstrip() for line in f_contents]

  # 25 zufällige Wörter aus der Wortliste auswählen
  wortliste = random.sample(f_contents, 25)

  # 5x5 Wortmatrix anzeigen:
  #for i in range(5):
  #  print("\t\t".join(wortliste[i*5:i*5+5]))
  print(wortliste)

  print("\nTeam Rot ist dran!")

  if spielstart == "n":
    quit()