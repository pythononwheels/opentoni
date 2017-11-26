from random import randint

def get_rand(last, end):
    tries = 1
    while True:
        curr = randint(0,end)
        if curr != last:
            return curr, tries
        tries += 1

curr=0
for elem in range(0,20):
    curr, tries=get_rand(curr,4)
    print(str(curr) + " : " + str(tries))