# Wordle Solver

## Overview

The **Wordle Solver** is a Python-based tool designed to assist players in solving Wordle puzzles efficiently. The program uses entropy-based scoring to suggest the best guesses and filters possible answers based on Wordle feedback.

## Features

- **Entropy-Based Suggestions**: Calculates the most informative guesses to prioritize.
- **Interactive Gameplay**: Guides users through their guesses and updates suggestions.

### 1. Start the Solver:
Run the program, and it will guide you through the process.
```bash
   cd wordle-project
   python simulations.py

### 2. Make a Guess:
The solver will suggest the most optimal words based on the remaining possibilities.
Enter your guessed word into Wordle and provide the guessed word to the solver.

### 3. Enter Feedback:
After each guess in Wordle, input the corresponding feedback into the solver:
E.g. **`gyxxy`**
- Use **`g`** for green (correct letter, correct position).
- Use **`y`** for yellow (correct letter, wrong position).
- Use **`x`** for grey (incorrect letter).

### 4. Repeat:
Continue following the solver’s suggestions until the solution is found or the maximum attempts are reached.

