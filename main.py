print("RUNNING PROGRAM")
import string
import pandas as pd

alpha = list(string.ascii_lowercase)
letter_scores = dict.fromkeys(alpha,[0,0,0,0,0])
scores = pd.DataFrame(letter_scores)
text = open("/Users/sammachin/Documents/Data Science Practice Problems/Wordle/sgb-words.txt")
word_list = []
turns_taken = 1

# Creating a list of words, where each word is a list of 5 letters
for line in text:
    stripped = line.strip()
    line_list = list(stripped)
    word_list.append(line_list)

# Creating starting scores for each letter
for word in word_list:
    for index, letter in enumerate(word):
        scores[letter][index] += 1
scores = scores/len(word_list)
# Producing Optimal Word
word_values = []
original_list = tuple(word_list)
for word in word_list:
    word_val = 0
    for index, letter in enumerate(word):
        val_green = scores[letter][index] * (1-scores[letter][index])
        val_yellow = (sum(scores[letter])-scores[letter][index]) * (scores[letter][index] - sum(scores[letter]))
        val_black = sum(scores[letter])*(1-sum(scores[letter]))
        word_val += sum([val_green, val_yellow, val_black])
    word_values.append(word_val)

best_word = word_list[word_values.index(max(word_values))]
print(f"Best word to play is {best_word}") # Kicks out the best word to enter

result = input(f"Turn {turns_taken} results for all 5 letters (G/Y/B):")  # Interprets results
result = list(result)

# Turn results into scores
certain_letters = [0,0,0,0,0]
# Remove the words from the list that no longer are possible
while result != ["G","G","G","G","G"]:
    turns_taken += 1
    for index in [0,1,2,3,4]: # Go through the letters in the word
        colour_out = result[index]
        letter_in = best_word[index]
        words_to_remove = []
        print(f'{letter_in} --> {colour_out}')
        if colour_out == "B":
            for word in word_list:
                for letter in word:
                    if letter == letter_in and certain_letters.count(letter) == 0:
                        words_to_remove.append(word)
                        break   # Remove any word containing a B that we don't have a green for
                    elif certain_letters.count(letter) >= 1: # If there is a green for that letter
                        if certain_letters.index(letter) != word.index(letter):    # Then remove all words where the
                            # position of that letter does not match the green
                            words_to_remove.append(word)
                    break
        elif colour_out == "Y":
            for word in word_list:
                if word[index] == letter_in:    # Remove all words  with yellow letter in yellow position
                    words_to_remove.append(word)
                elif word.count(letter_in) <= certain_letters.count(letter_in):
                    words_to_remove.append(word)    # Remove all words with less than the minimum number of letter in
        elif colour_out == "G":
            certain_letters[index] = letter_in
            for word in word_list:
                if word[index] != letter_in:
                    words_to_remove.append(word)
        for word in words_to_remove:
            word_list.remove(word)
    print(f"{len(word_list)} words remaining")
    if len(word_list) < 50:
        print(word_list)
    # Creating starting scores for each letter
    scores = pd.DataFrame(letter_scores)
    for word in word_list:
        for index, letter in enumerate(word):
            scores[letter][index] += 1
    scores = scores/len(word_list)
    # Producing Optimal Word
    word_values = []

    for word in original_list:
        word_val = 0
        for index, letter in enumerate(word):
            val_green = scores[letter][index] * scores.sum(axis=1)[index]
            val_yellow = (sum(scores[letter]) - scores[letter][index]) * (scores[letter][index] - sum(scores[letter]))
            val_black = sum(scores[letter]) * (1 - sum(scores[letter]))
            word_val += sum([val_green, val_yellow, val_black])
        word_values.append(word_val)

    best_word = original_list[word_values.index(max(word_values))]
    print(f"Best word to play is {best_word}")  # Kicks out the best word to enter
    result = input(f"Turn {turns_taken} results for all 5 letters (G/Y/B):")  # Interprets results
    result = list(result)

print(f"Congratulations!!! Finished in {turns_taken} turns")
