import os
from collections import defaultdict
import math

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

def filter_possible_answers(possible_answers, last_input, accuracy):
    matched_counts = {char: 0 for char in set(last_input)}

    for i, (char, acc) in enumerate(zip(last_input, accuracy)):
        if acc == 'g':
            possible_answers = [word for word in possible_answers if word[i] == char]
            matched_counts[char] += 1
        elif acc == 'y':
            possible_answers = [
                word for word in possible_answers
                if char in word and word[i] != char and word.count(char) > matched_counts[char]
            ]
            matched_counts[char] += 1
        elif acc == 'x':
            possible_answers = [
                word for word in possible_answers
                if char not in word or word.count(char) <= matched_counts[char]
            ]

    return possible_answers

def generate_correctness_pattern(guess, answer):
    pattern = []
    answer_used = [False] * len(answer)
    
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            pattern.append('g')
            answer_used[i] = True
        else:
            pattern.append(None)
    
    for i in range(len(guess)):
        if pattern[i] is None:
            if guess[i] in answer and not answer_used[answer.index(guess[i])]:
                pattern[i] = 'y'
                answer_used[answer.index(guess[i])] = True
            else:
                pattern[i] = 'x'
    
    return ''.join(pattern)

def calculate_entropy(guess, possible_answers):
    pattern_counts = defaultdict(int)
    
    for answer in possible_answers:
        pattern = generate_correctness_pattern(guess, answer)
        pattern_counts[pattern] += 1
    
    entropy = 0
    for count in pattern_counts.values():
        probability = count / len(possible_answers)
        entropy -= probability * math.log2(probability)
    
    return entropy

def get_best_guesses(possible_guesses):
    scored_guesses = [(guess, calculate_entropy(guess, possible_guesses)) for guess in possible_guesses]
    scored_guesses.sort(key=lambda x: x[1], reverse=True)

    return scored_guesses[:3]

if __name__ == "__main__":
    inputs = []
    accuracy = 'xxxxx'
    possible_answers = get_word_list_from_file(SHORT_WORD_LIST_FILE)
    best_guesses = []

    print("Welcome to Wordle Solver!")

    while len(inputs) < 6 and accuracy != 'ggggg':
        print(f"\nATTEMPT {len(inputs) + 1}")
        best_guesses = get_best_guesses(possible_answers)

        if len(best_guesses) == 1:
            print(f"The answer is '{best_guesses[0][0]}'")
            inputs.append(best_guesses[0][0])
            accuracy = 'ggggg'

        else:
            print(f"Number of possible answers: {len(possible_answers)}")
            print("Suggested words:")
            for (i, (guess, entropy)) in enumerate(best_guesses):
                print(f"Word {i + 1}: '{guess}', Entropy: {entropy}")

            inputs.append(input("\nWhich word did you guess?\n"))
            accuracy = input("\nEnter the corresponding correctness for each letter: \n('g' for a green letter, 'y' for yellow letter and 'x' for a grey one) e.g. 'gyxxy'\n")

            possible_answers = filter_possible_answers(possible_answers, inputs[-1], accuracy)

    if (accuracy == 'ggggg'):
        print(f"\nWell done for getting the answer on attempt number {len(inputs)}!")
    else:
        print("\nBetter luck next time!")
