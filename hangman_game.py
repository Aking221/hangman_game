import random
import sys
import unicodedata
from datetime import datetime

# Fonction pour normaliser les lettres
def normalize_letter(letter):
    return unicodedata.normalize('NFD', letter).encode('ascii', 'ignore').decode('utf-8')

# Fonction pour générer un mot aléatoire à partir d'un fichier
def random_liste(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            liste = f.read().splitlines()
            if not liste:  # Vérifie si le fichier est vide
                print(f"Erreur : {filename} est vide.")
                sys.exit(1)
    except FileNotFoundError:
        print(f"Erreur : Fichier {filename} non trouvé.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur : Un problème inattendu est survenu : {e}")                   
        sys.exit(1)

    return random.choice(liste)

# Fonction pour compter les occurrences d'une lettre dans un mot
def count_occurrence(mot, lettre):
    return mot.count(lettre)

# Fonction pour afficher l'état actuel du mot
def display_word(mot, correct_guesses):
    return ' '.join([letter if letter in correct_guesses else '_' for letter in mot])

# Fonction pour calculer les pénalités
def penalite(lettre, mot, penalites):
    if lettre in mot:
        penalites += 1  
    else:
        penalites += 3  
    return penalites

# Fonction pour gérer les meilleurs scores
def get_best_score():
    try:
        with open("best_scores.txt", "r", encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                parts = last_line.split(" - ")
                if len(parts) == 2:
                    date = parts[0]
                    word_attempts = parts[1].split(" : ")
                    if len(word_attempts) == 2:
                        word = word_attempts[0]
                        attempts = int(word_attempts[1].split()[0])  # Prendre uniquement le nombre avant 'tentatives'
                        return (word, attempts), date
    except FileNotFoundError:
        return None, None
    except Exception as e:
        print(f"Erreur lors de la lecture des meilleurs scores : {e}")
    return None, None

def update_best_score(attempts, word):
    try:
        with open("best_scores.txt", "a", encoding='utf-8') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {word} : {attempts} tentatives\n")
    except Exception as e:
        print(f"Erreur lors de la mise à jour des meilleurs scores : {e}")

# Fonction principale du jeu Hangman
def hangman_game(filename):
    a = random_liste(filename)  # Le mot mystère depuis le fichier
    penalites = 0
    correct_guesses = set()  # Ensemble pour stocker les bonnes lettres
    all_guesses = set()  # Ensemble pour suivre toutes les lettres devinées
    attempts = 0  # Compteur de tentatives

    # Obtenir le meilleur score actuel
    best_score, best_date = get_best_score()
    if best_score:
        print(f"Meilleur score précédent : {best_score[0]} avec {best_score[1]} tentatives (enregistré le {best_date}).")

    print(display_word(a, correct_guesses))  # Afficher le mot initial

    while penalites < 40:  
        b = input("Entrez une seule lettre ou un mot complet : ").lower()
        attempts += 1  # Incrémenter le compteur de tentatives

        # Vérifie si l'utilisateur a entré un mot complet
        if len(b) > 1 and b.isalpha():  
            if b == a:
                print(f"Bien joué ! Vous avez trouvé le mot qui était {a} en {attempts} tentatives. ( ˶ˆ ᗜ ˆ˵ )")
                if best_score is None or attempts < best_score[1]:
                    print("Meilleur score battu !!!")
                    update_best_score(attempts, a)  # Mettre à jour les meilleurs scores
                else:
                    print(f"Vous avez deviné le mot en {attempts} tentatives. Le record est {best_score[1]} tentatives.")
                break
            else:
                penalites += 5
                print(f"Mauvais essai ! Pénalités ajoutées : 5. Pénalités totales : {penalites}.")
                continue

        if len(b) == 1 and b.isalpha():  
            if b in all_guesses:
                print(f"Vous avez déjà deviné la lettre {b}. Réessayez.")
                continue

            all_guesses.add(b)

            occurences = count_occurrence(a, b)
            if occurences > 0:
                correct_guesses.add(b)
                print(f"Trouvé {occurences} '{b}'")
            else:
                print(f"Aucun '{b}' trouvé")

            print(display_word(a, correct_guesses))

            penalites = penalite(b, a, penalites)
            print(f"Pénalités totales : {penalites}")

            if set(a) == correct_guesses:
                print(f"Bien joué ! Vous avez trouvé le mot qui était {a} en {attempts} tentatives. ( ˶ˆ ᗜ ˆ˵ )")
                if best_score is None or attempts < best_score[1]:
                    print("Meilleur score battu !!!")
                    update_best_score(attempts, a)  # Mettre à jour les meilleurs scores
                else:
                    print(f"Vous avez deviné le mot en {attempts} tentatives. Le record est {best_score[1]} tentatives.")
                break
        else:
            print("Veuillez entrer une seule lettre alphabétique ou un mot complet.")

    if penalites >= 40:
        print(f"Game Over ! (×_×) Le mot était {a}.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]  # Prendre le nom de fichier du premier argument
        hangman_game(filename)
    else:
        print("Erreur : argument manquant")
