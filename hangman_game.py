import random

# Function to generate a random word from the list
def random_liste():
    liste = ['paradis', 'cassable', 'inhaler', 'encore', 'casier', 'moustiquaire', 'tyran', 'déshabiller', 'parfumerie', 'paon', 'shenanigans','hangman','messi','ronaldo']
    return random.choice(liste)

# Function to count occurrences of a letter in a word
def count_occurrence(mot, lettre):
    return mot.count(lettre)

# Function to display the current state of the word
def display_word(mot, correct_guesses):
    return ' '.join([letter if letter in correct_guesses else '_' for letter in mot])


def penalite(lettre, mot, penalites):
    if lettre in mot:
        penalites += 1  
    else:
        penalites += 3  
    return penalites


def hangman_game():
    a = random_liste()  # The mystery word
    penalites = 0
    correct_guesses = set()  # Set to store correct guesses
    all_guesses = set()  # Set to track all guesses (to avoid repeats)

    print(display_word(a, correct_guesses))  # Display initial word with dashes

    while penalites < 40:  
        b = input("Entrez une seule lettre : ").lower()

        if len(b) != 1 or not b.isalpha():  
            print("Veuillez entrer une seule lettre alphabétique.")
            continue
        
        if b in all_guesses:
            print(f"Vous avez déjà deviné la lettre {b}. Réessayez.")
            continue

        all_guesses.add(b)

        occurences = count_occurrence(a, b)
        if occurences > 0:
            correct_guesses.add(b)
            print(f"Found {occurences} '{b}'")
        else:
            print(f"No '{b}' found")

        
        print(display_word(a, correct_guesses))

       
        penalites = penalite(b, a, penalites)
        print(f"Totale penalites: {penalites}")

        
        if set(a) == correct_guesses:
            print(f"Bien Jouer Vous Avez trouvé le bon mot qui etais {a}.( ˶ˆ ᗜ ˆ˵ )")
            break

    if penalites >= 40:
        print(f"Game Over!(×_×) The word was {a}.")


hangman_game()
