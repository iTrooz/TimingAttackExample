from time import time, sleep
import string
from concurrent.futures import ProcessPoolExecutor
from thread_with_return_value import ThreadWithReturnValue

# MDP, INVISIBLE
PASSWORD = "bbb"
TIMING = 0.000_01
# TIMING = 0

def characters():
    for i in string.ascii_letters:
        yield i
    for i in string.digits:
        yield i
    for i in string.punctuation:
        yield i

# PARTIE BACKEND, INVISIBLE MAIS GO DIRE QUE JE DEVINE LE CODE
def check_password(candidate):
    if len(PASSWORD) != len(candidate):
        return False
    sleep(TIMING)

    for i in range(len(PASSWORD)):
        if PASSWORD[i] != candidate[i]:
            return False
        sleep(TIMING)
    return True

# MON CODE

class TimedData:
    def __init__(self, time, data):
        self.time = time
        self.data = data

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Timed(time={},data={})".format(round(self.time, 3), self.data)

def guess_length():
    print("\nGuessing length..")
    times = []
    for i in range(10):
        start = time()
        check_password("A"*i)
        end = time()
        times.append(TimedData(time=end-start, data=i))

    sorted_times = sorted(times, reverse=True)
    assumed_length = sorted_times[0].data
    print(f"Assumed length: {assumed_length}")
    return assumed_length

def letter_times(guessed_mdp, letter_n, assumed_length, repeat):
    # print(f"\nGuessing letter {letter_n}..")
    times = []
    
    for letter in characters():
        
        guess = guessed_mdp+letter + "a"*(assumed_length-letter_n)

        start = time()
        for i in range(repeat):
            check_password(guess)
        end = time()

        times.append(TimedData(time=(end-start), data=letter))

    return times



def guess_letters(assumed_length, repeat=1, repeat_threads=1):
    letter_n = 1
    guessed_mdp = ""
    for letter_n in range(1, assumed_length+1):
    
        tasks = []

        executor = ProcessPoolExecutor()
        for i in range(repeat_threads-1):
            future = executor.submit(letter_times, guessed_mdp, letter_n, assumed_length, repeat)
            tasks.append(future)

        all_results = letter_times(guessed_mdp, letter_n, assumed_length, repeat)

        for thr in tasks:
            his_result = thr.result()
            for i in range(len(his_result)):
                all_results[i].time += his_result[i].time


        sorted_times = sorted(all_results, reverse=True)
        guessed_letter = sorted_times[0].data
        
        # print(f"Guessed letter: {guessed_letter}")
        guessed_mdp+=guessed_letter
        letter_n += 1

    # print(f"\n\nGUESSED LETTERS: {guessed_mdp}")
    return guessed_mdp

def letter_count(pass_list, letter='b'):
    wrong = 0
    right = 0
    for L in pass_list:
        for i in L:
            if i == 'b':
                right+=1
            else:
                wrong+=1
    return {"B":right, "Not_B":wrong}

# guessed_length = guess_length()
guessed_length = 3


pass_list_A = []
for i in range(5):
    print("A iteration ", i)
    pass_list_A.append(guess_letters(guessed_length, repeat_threads=1))


pass_list_B = []
REPEAT = 10
THREADS = 12
for i in range(5):
    print("B iteration ", i)
    pass_list_B.append(guess_letters(guessed_length, REPEAT, repeat_threads=THREADS))

print("without repeat:")
print(pass_list_A)
print("B counts:", letter_count(pass_list_A))

print(f"with repeat: (repeat={REPEAT} threads={THREADS})")
print(pass_list_B)
print("B counts:", letter_count(pass_list_B))
