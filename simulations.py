import os

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "data",
)
SHORT_WORD_LIST_FILE = os.path.join(DATA_DIR, "possible_words.txt")
LONG_WORD_LIST_FILE = os.path.join(DATA_DIR, "allowed_words.txt")

def get_word_list_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            words = file.read().splitlines()  # Reads lines and removes newline characters
        return words
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def filter_possible_words(words, last_input, accuracy):
    filtered_words = words

    matched_counts = {char: 0 for char in set(last_input)}

    for i, (char, acc) in enumerate(zip(last_input, accuracy)):
        if acc == 'g':
            filtered_words = [word for word in filtered_words if word[i] == char]
            matched_counts[char] += 1
        elif acc == 'y':
            filtered_words = [
                word for word in filtered_words
                if char in word and word[i] != char and word.count(char) > matched_counts[char]
            ]
            matched_counts[char] += 1
        elif acc == 'x':
            filtered_words = [
                word for word in filtered_words
                if char not in word or word.count(char) <= matched_counts[char]
            ]

    return filtered_words

def calculate_entropy(word, word_list):
    return -1

def get_guesses(possible_words):
    scored_words = [(word, calculate_entropy(word, possible_words)) for word in possible_words]
    scored_words.sort(key=lambda x: x[1], reverse=True)

    return scored_words[:3]

if __name__ == "__main__":
    inputs = []
    accuracy = 'xxxxx'
    possible_words = get_word_list_from_file(SHORT_WORD_LIST_FILE)
    guesses = []

    print("Welcome to Wordle Helper!")

    while len(inputs) < 6 and accuracy != 'ggggg':
        print(f"\nATTEMPT {len(inputs) + 1}")
        guesses = get_guesses(possible_words)

        print(f"Number of possible answers: {len(possible_words)}")
        print("Suggested words:")
        for (i, (word, entropy)) in enumerate(guesses):
            print(f"Word {i + 1}: '{word}', Entropy: {entropy}")

        inputs.append(input("\nWhich word did you choose?\n"))
        accuracy = input("\nEnter the corresponding correctness for each letter: \n('g' for a green letter, 'y' for yellow letter and 'x' for a grey one)\n")

        possible_words = filter_possible_words(possible_words, inputs[-1], accuracy)

    if (accuracy == 'ggggg'):
        print(f"\nWell done for getting the answer on attempt number {len(inputs)}!")
    else:
        print("\nBetter luck next time!")
