from time import time, sleep
import string

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

def guess_letters(assumed_length, repeat=1):
    letter_n = 1
    guessed_mdp = ""
    for letter_n in range(1, assumed_length+1):
        print(f"\nGuessing letter {letter_n}..")
        times = []


        for letter in characters():
            
            guess = guessed_mdp+letter + "a"*(assumed_length-letter_n)

            total_time = 0
            start = time()
            for i in range(repeat):
                check_password(guess)
            end = time()
            total_time += end-start
            times.append(TimedData(time=total_time, data=letter))

        sorted_times = sorted(times, reverse=True)
        guessed_letter = sorted_times[0].data
        
        print(f"Guessed letter: {guessed_letter}")
        guessed_mdp+=guessed_letter

        letter_n += 1

    print(f"\n\nGUESSED PASSWORD: {guessed_mdp}")
    return guessed_mdp

# guessed_length = guess_length()
guessed_length = 3

A = []
for i in range(10):
    A.append(guess_letters(guessed_length))

B = []
for i in range(10):
    B.append(guess_letters(guessed_length, repeat=100_000))


def b_count(LL):
    wrong = 0
    right = 0
    for L in LL:
        for i in L:
            if i == 'b':
                right+=1
            else:
                wrong+=1
    return {"B":right, "Not_B":wrong}


print("without repeat:")
print(A)
print("B counts:", b_count(A))

print("with repeat:")
print(B)
print("B counts:", b_count(B))