from time import time, sleep
import string
import threading
from thread_with_return_value import ThreadWithReturnValue

# MDP, INVISIBLE
PASSWORD = "bbb"
# TIMING = 0.000_000_000_1
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
    # sleep(TIMING)

    for i in range(len(PASSWORD)):
        if PASSWORD[i] != candidate[i]:
            return False
        # sleep(TIMING)
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

    print(times)
    sorted_times = sorted(times, reverse=True)
    assumed_length = sorted_times[0].data
    print(f"Assumed length: {assumed_length}")
    return assumed_length

def letter_times(guessed_mdp, letter_n, assumed_length, repeat):
    print("Letter times")
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
    print("a")
    for letter_n in range(1, assumed_length+1):
        print(letter_n)

        threads = []

        for i in range(repeat_threads-1):
            thr = ThreadWithReturnValue(target=letter_times, args=(guessed_mdp, letter_n, assumed_length, repeat))
            thr.daemon = True
            thr.start()
            threads.append(thr)

        all_results = letter_times(guessed_mdp, letter_n, assumed_length, repeat)

        for thr in threads:
            his_result = thr.join()
            for i in range(len(his_result)):
                all_results[i].time += his_result[i].time


        sorted_times = sorted(all_results, reverse=True)
        print("b")
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
guessed_length = 1


# pass_list_A = []
# for i in range(5):
#     pass_list_A.append(guess_letters(guessed_length, repeat=100, repeat_threads=1))


pass_list_B = []
REPEAT = 200000
THREADS = 2
for i in range(1):
    pass_list_B.append(guess_letters(guessed_length, REPEAT, repeat_threads=THREADS))


exit(1)

print("without repeat:")
print(pass_list_A)
print("B counts:", letter_count(pass_list_A))

print(f"with repeat: (repeat={REPEAT} threads={THREADS})")
print(pass_list_B)
print("B counts:", letter_count(pass_list_B))
