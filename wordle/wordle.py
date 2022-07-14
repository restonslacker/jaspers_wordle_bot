import string
import random
from collections import Counter
from itertools import chain
import operator
import re

possible_wordle_words = open('possible_wordle_words.txt','r').read().split('\n')

ALLOWED_ATTEMPTS = 6
WORD_LENGTH = 5
WORDS = list(set(possible_wordle_words))

def calculate_word_commonality(word, letter_frequency):
    """
    Edited

    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    score = 0.0
    for char in word:
        score += letter_frequency[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)

def sort_by_word_commonality(words, letter_frequency):
    """
    Edited

    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    sort_by = operator.itemgetter(1)
    lol = sorted(
        [(word, calculate_word_commonality(word, letter_frequency)) for word in words],
        key=sort_by,
        reverse=True,
    )
    return lol

def display_word_table(word_commonalities, top_n):
    """
    Edited

    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    count = 0
    freq_list = []
    for (word, freq) in word_commonalities:
        print(f"{word:<10} | {freq:<5.3}")
        freq_list.append(round(freq, 3))
        count+=1
        if count >=top_n:
            if sum(freq_list) / count != freq_list[0]:
                break
        
def input_word():
    """
    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    while True:
        word = input("Input the word you entered> ")
        if len(word) == WORD_LENGTH and word.lower() in WORDS:
            break
    return word.lower()

def input_response():
    """
    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    print("Type the color-coded reply from Wordle:")
    print("  G for Green")
    print("  Y for Yellow")
    print("  ? for Gray")
    while True:
        response = input("Response from Wordle> ")
        if len(response) == WORD_LENGTH and set(response) <= {"G", "Y", "?"}:
            break
        else:
            print(f"Error - invalid answer {response}")
    return response

def match_word_vector(word, word_vector):
    """
    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True

def match(word_vector, possible_words):
    """
    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    return [word for word in possible_words if match_word_vector(word, word_vector)]

def solve(top_n:int=5):
    """
    Edited - Play today's wordle

    Parameters
    ----------
    top_n :int
        display top n number of words

    Reference:
    ----------
    https://www.inspiredpython.com/article/solving-wordle-puzzles-with-basic-python
    """
    possible_words = WORDS.copy()
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    for attempt in range(1, ALLOWED_ATTEMPTS + 1):
        print(f"Attempt {attempt} with {len(possible_words)} possible words")
        letter_counter = Counter(chain.from_iterable(possible_words))
        letter_frequency = {character: value / sum(letter_counter.values()) for character, value in letter_counter.items()}
        display_word_table(sort_by_word_commonality(possible_words, letter_frequency), top_n)
        word = input_word()
        response = input_response()
        if response == 'GGGGG':
            if attempt <= 3:
                print("Congrats, you get cookies! You got", word, "in", attempt, 'tries! Goodbye Winner!')
            else:
                print("Darn, you get no cookies! You got", word, "in", attempt, 'tries! Goodbye Loser!')
            break
        for idx, letter in enumerate(response):
            if letter == "G":
                word_vector[idx] = {word[idx]}
                possible_words_copy = possible_words.copy()
                for i in possible_words_copy:
                    if word[idx] != i[idx]:
                        possible_words.remove(i)
            elif letter == "Y":
                try:
                    word_vector[idx].remove(word[idx])
                    possible_words_copy = possible_words.copy()
                    for i in possible_words_copy:
                        if word[idx] not in i:
                            possible_words.remove(i)
                except KeyError:
                    pass
            elif letter == "?":
                for vector in word_vector:
                    try:
                        vector.remove(word[idx])
                        possible_words_copy = possible_words.copy()
                        for i in possible_words_copy:
                            if word[idx] in i:
                                possible_words.remove(i)
                    except KeyError:
                        pass
        possible_words = match(word_vector, possible_words)

def get_feedback(word_list, answer):
    """
    Gives user feedback on word

    Parameters
    ----------
    word_list : str
        list of words entered
    answer : str
        answer to wordle

    Returns
    -------
    response : str
        feedback given to user
    """
    response_list = []
    for i in word_list:
        response = ''
        for index, item in enumerate(i):
            if item in answer:
                if item == answer[index]:
                    response = response + 'G'
                else:
                    response = response + 'Y'
            else:
                response = response + '?'
        response_list.append(response)
    return response_list[-1], response_list

def play_wordle(top_n:int=5):
    """
    Play wordle with available words that haven't been used

    Parameters
    ----------
    top_n :int
        display top n number of words
    """
    possible_words = WORDS.copy()
    answer = random.choice(list(possible_words))
    print(answer)
    word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]
    word_list = []
    for attempt in range(1, ALLOWED_ATTEMPTS + 1):
        print(f"Attempt {attempt} with {len(possible_words)} possible words")
        letter_counter = Counter(chain.from_iterable(possible_words))
        letter_frequency = {character: value / sum(letter_counter.values()) for character, value in letter_counter.items()}
        display_word_table(sort_by_word_commonality(possible_words, letter_frequency), top_n)
        while True:
            word = input_word()
            word_list.append(word)
            if len(word) == 5:
                response, response_list = get_feedback(word_list, answer)
                print("Feedback:")
                for i in range(len(response_list)):
                    print(response_list[i], ":", word_list[i])
                break
            else:
                'WARNING: Word can only be 5 characters long! Try again'
        if response == 'GGGGG':
            if attempt <= 3:
                print("Congrats, you get cookies! You got", word, "in", attempt, 'tries! Goodbye Winner!')
            else:
                print("Darn, you get no cookies! You got", word, "in", attempt, 'tries! Goodbye Loser!')
            break
        pattern = '.....'
        antipattern = '.....'
        must_haves=[]
        mustnt_haves=[]    
        for idx, letter in enumerate(response):
            if letter == "G":
                if(idx<4): pattern = pattern[:idx]+word[idx]+pattern[idx+1:]
                else: pattern = pattern[:idx]+word[idx]
                must_haves.append(word[idx])
                if mustnt_haves.count(word[idx]):
                    mustnt_haves.remove(word[idx])
            elif letter == "Y":
                possible_words = [w for w in possible_words if (re.search(word[idx], w) is not None) and
                (re.search(word[idx], w).start!=idx)]
                must_haves.append(word[idx])
                if mustnt_haves.count(word[idx]):
                    mustnt_haves.remove(word[idx])
            elif letter == "?":
                if(must_haves.count(word[idx])==0):
                    mustnt_haves.append(word[idx])
                    if(idx<4): antipattern = antipattern[:idx]+word[idx]+antipattern[idx+1:]
                    else: antipattern = antipattern[:idx]+word[idx]
        print((pattern, antipattern, must_haves,mustnt_haves))
        possible_words = [w for w in possible_words 
        if (re.search(pattern, w)is not None) and
        (re.search(antipattern, w) is None) and (re.search('|'.join(mustnt_haves),w) is None)]

# solve()
# play_wordle()
