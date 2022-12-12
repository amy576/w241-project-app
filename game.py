
from random import *
import time
import os
import time
import platform
import csv  
import pandas as pd
import datetime
from pygame import mixer

def intro():
    person_id = int(input("Person ID: "))
    print("You have 5 seconds to memorize the number shown. There are {} numbers total. Good luck!".format(num_rounds))
    time.sleep(3)
    return person_id

def countdown(rest=False):
    if rest:
        for i in range(5):
            time.sleep(10)
            print("{} seconds left...".format((5 - i) * 10))
        time.sleep(5)
        print("5 seconds left!")
        time.sleep(5)
    else:
        print("Ready? 3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)

def get_input():
    while True:
        guess = input("What is the number? ") 
        if guess.isdigit():
            if len(str(guess)) > 10:
                guess = str(guess)[:10]
            break
        print("Incorrect type of input: Please make sure you are submitting a 10 digit number.\n") 
    return int(guess)  
        
def get_score(guess, answer):
    score = 0

    # Trim answer to guess length
    if len(str(answer)) > len(str(guess)):
        answer = int(str(answer)[:len(str(guess))])

    for d in range(len(str(answer))):
        guess_digit = guess % 10
        answer_digit = answer % 10
        if guess_digit == answer_digit:
            score += 1

        guess = (guess - (guess%10)) / 10
        answer = (answer - (answer%10)) / 10
    return score


##### Setup #####
num_digits = 10
num_rounds = 5
file_exists = os.path.exists('data/output.csv') 

treatment_options = {
    1: ['pretest', 'control', 'music', 'noise'],
    2: ['pretest', 'control', 'noise', 'music'],
    3: ['pretest', 'music', 'control', 'noise'],
    4: ['pretest', 'music', 'noise', 'control'],
    5: ['pretest', 'noise', 'control', 'music'],
    6: ['pretest', 'noise', 'music', 'control']
}
treatment_order = randint(1, 6)
treatments = treatment_options[treatment_order]

mixer.init()
if platform.system() == 'Windows':
    clear = lambda: os.system('cls')
else:  
    clear = lambda: os.system('clear')

##### Game #####
person_id = intro()

for t in range(len(treatments)):
    treatment = treatments[t]
    sub_treatment = treatment # TODO

    if treatment == 'noise':
        mixer.music.load("audio/noise.mp3")
        mixer.music.play()

    if treatment == 'music':
        mixer.music.load("audio/music.mp3")
        mixer.music.play()

    for i in range(num_rounds):   
        answer = randint(10**(num_digits-1), 10**num_digits-1)
        countdown()

        # Show the number for 5 seconds
        print(answer)  
        time.sleep(5) 
        clear()

        # Ask input to guess number
        start = time.time()
        guess = get_input()
        end = time.time()
        timestamp = datetime.datetime.now().replace(microsecond=0)

        # Score answer
        score = get_score(guess, answer)

        row = [person_id, treatment_order, treatment, sub_treatment, timestamp, i + 1, answer, guess, score, round(end-start, 2)]

        # Write to csv
        with open('data/output.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # If it's a new CSV, include column names
            if not file_exists:
                columnNames = ['person_id', 'treatment_order', 'treatment', 'sub_treatment', 'timestamp', 'q_number', 'question', 'input', 'score', 'time']
                writer.writerow(columnNames)
                file_exists = True
            writer.writerow(row)
    
    mixer.music.stop()
    if t < 3:
        print("You finished the round! You have 60 seconds to rest.")
        countdown(rest=True)


clear()
print("Thanks for playing!")
