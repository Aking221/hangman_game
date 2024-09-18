import random
import sys

# List of possible words
def random_liste():
    return ['paradis', 'cassable', 'inhaler', 'encore', 'casier', 'moustiquaire', 'tyran', 'déshabiller', 'parfumerie', 'paon', 'shenanigans', 'hangman', 'messi', 'ronaldo']

# Count the occurrences of a letter in a word
def count_occurrence(mot, lettre):
    return mot.count(lettre)

# Display the current state of the word
def display_word(mot, correct_guesses):
    return ' '.join([letter if letter in correct_guesses else '_' for letter in mot])

# Update penalties
def penalite(lettre, mot, penalites):
    if lettre not in mot:
        penalites += 3  # Penalty if the letter is not in the word
    else:
        penalites += 1  # Light penalty if the letter is present
    return penalites

# Reduce the list of possible words after each guess
def reduce_possible_words(possible_words, guessed_letter, correct_guesses):
    new_possible_words = []
    for word in possible_words:
        if all((letter in correct_guesses or letter != guessed_letter) for letter in word):
            new_possible_words.append(word)
    return new_possible_words

# Main function for the hangman game
def hangman_game(cheat_mode=False):
    a = random.choice(random_liste())  # The mystery word
    word_length = len(a)
    penalites = 0
    correct_guesses = set()  # Correct letters
    all_guesses = set()  # Already guessed letters
    possible_words = [word for word in random_liste() if len(word) == word_length]  # List of possible words of the same length

    print(display_word(a, correct_guesses))  # Display initial state

    while penalites < 40:  # As long as penalties are below 40
        if cheat_mode:
            # Cheat mode activated - AI chooses the most frequent letter
            letter_frequencies = {}
            for word in possible_words:
                for letter in word:
                    if letter not in all_guesses:
                        letter_frequencies[letter] = letter_frequencies.get(letter, 0) + 1
            
            # Choose the letter with the highest frequency
            if letter_frequencies:
                guessed_letter = max(letter_frequencies, key=letter_frequencies.get)
            else:
                break  # If no letters are available

            print(f"$> ('{guessed_letter.upper()}' advised) {guessed_letter.upper()}")

        else:
            # Normal mode - The player guesses a letter
            guessed_letter = input("Enter a single letter: ").lower()
            if len(guessed_letter) != 1 or not guessed_letter.isalpha():
                print("Please enter a single alphabetic letter.")
                continue

        all_guesses.add(guessed_letter)  # Add the guessed letter to the list of guesses
        occurences = count_occurrence(a, guessed_letter)

        if occurences > 0:
            correct_guesses.add(guessed_letter)
            print(f"Found {occurences} '{guessed_letter}'")
        else:
            print(f"No '{guessed_letter}' found")
        
        print(display_word(a, correct_guesses))  # Display the current state of the word
        penalites = penalite(guessed_letter, a, penalites)  # Update penalties
        print(f"Total penalties: {penalites}")

        # Reduce the list of possible words based on the guesses
        possible_words = reduce_possible_words(possible_words, guessed_letter, correct_guesses)

        # If the AI guessed the complete word
        if set(a) == correct_guesses:
            print(f"Well done! You found the word which was '{a}'.( ˶ˆ ᗜ ˆ˵ )")
            break

    if penalites >= 40:
        print(f"Game Over!(×_×) The word was '{a}'.")  


# Run the game with or without cheat based on the arguments
if __name__ == "__main__":
    cheat_mode = '-cheat' in sys.argv
    hangman_game(cheat_mode)
