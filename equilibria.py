import numpy as np
import matplotlib.pyplot as plt


valid_words = np.loadtxt("data/possible_words.txt", dtype=str)


def find_pattern(guess, actual):
    """Returns the pattern of the guess compared to the actual word."""
    result = ["X"] * len(guess)
    actual_list = list(actual)

    # check for green squares
    for i in range(len(guess)):
        if guess[i] == actual[i]:
            result[i] = "G"
            actual_list[i] = None 

    # check for yellow squares
    for i in range(len(guess)):
        if result[i] == "X" and guess[i] in actual_list:
            result[i] = "Y"
            actual_list[actual_list.index(guess[i])] = None  

    return "".join(result)


def score_naive(guess, actual):
    """ Returns the naive score of a guess compared to the actual word."""
    result = find_pattern(guess, actual)
    return result.count("G") + 1/2 * result.count("Y")


def information_gain(guess, actual):
    """ Returns the information gain of a guess compared to the actual word."""
    pattern = find_pattern(guess, actual)
    count = 0
    
    for word in valid_words:
        if find_pattern(guess, word) == pattern:
            count += 1
    
    p = count/len(valid_words)
    return -np.log2(p)


def create_payoff_matrix(guesses, actual_words, score=information_gain):
    """ Creates a payoff matrix for a list of guesses and actual words."""
    G = np.zeros((len(actual_words), len(guesses)))
    
    for i, actual in enumerate(actual_words):
        for j, guess in enumerate(guesses):
            G[i, j] = score(guess, actual)
    
    return G


def reduce_matrix(G, rows, columns):
    """ Reduces a payoff matrix to the specified rows and columns."""
    return G[rows][:, columns]


def find_equilibrium():
    """ Finds an equilibrium in this game."""
    A = create_payoff_matrix(["adieu", "salet", "brick", "arise", "fjord"],
                             ["endow", "crypt", "shaky", "guile", "mauve"])
    print("Payoff matrix:\n", A)

    A = reduce_matrix(A, [0, 2], [0, 1, 3])
    print("\nReduced payoff matrix:\n ", A)

    p = np.linspace(0, 1, 1000)
    y1 = A[1, 0] + (A[0, 0] - A[1, 0]) * p
    y2 = A[1, 1] + (A[0, 1] - A[1, 1]) * p
    y3 = A[1, 2] + (A[0, 2] - A[1, 2]) * p

    pstar = (A[1, 0] - A[1, 1]) / ((A[0, 1] - A[1, 1]) - (A[0, 0] - A[1, 0]))
    qstar = (A[0, 1] - A[0, 0]) / ((A[1, 0] - A[1, 1]) - (A[0, 0] - A[0, 1]))
    value = A[1, 0] + (A[0, 0] - A[1, 0]) * pstar

    print(f"\nMax-min strategy for Player 1: {(pstar, 0, 1-pstar, 0, 0)}")
    print(f"Min-max strategy for Player 2: {(qstar, 1-qstar, 0, 0, 0)}")
    print(f"Value of the game: {value}")

    plt.scatter(pstar, value, c="black", label="Min-max strategy, p = 0.58")
    plt.plot(p, y1, label=r"$g(\alpha, b_1) = 3.02 + 3.11p$", c="red")
    plt.plot(p, y2, label=r"$g(\alpha, b_2) = 6.17 - 2.35p$", c="darkblue")
    plt.plot(p, y3, label=r"$g(\alpha, b_3) = 5.24 - 0.97p$", c="darkgreen")

    plt.xlabel(r"$p$")
    plt.ylabel("Payoff")
    plt.title("Upper-envelope method for finding Nash equilibrium")
    plt.legend()
    plt.grid()
    plt.show()


find_equilibrium()

