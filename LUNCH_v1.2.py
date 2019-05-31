import sys
import random
from random import shuffle
import time
import math
from getpass import getpass



########### TEXT COLORS MODIFIERS ###########

R = '\033[91m'		# Red
G = '\033[92m'		# Green
B = '\033[94m'		# Blue

WRN = '\033[93m'	# Warning (yellow)
HDR = '\033[95m'	# Header (purple)
NRM = '\033[0m'		# Normal (white)
BLD = '\033[1m'		# Bold (bold white)
UND = '\033[4m'		# Underline

################ FUNCTIONS ################

def printlistcolumn(reduced_rest_list):
    st = ''
    maxl = 35
    onethird = int(math.ceil(len(reduced_rest_list)*1.0/3))
    for idx in  range(0, onethird):
        for jdx in [idx,idx+onethird,idx+onethird*2]:
            if(jdx<len(reduced_rest_list)):
                txt = str(jdx+1) + '. ' + original_list[jdx]
                if(reduced_rest_list[jdx] == 'deleted'):
                    st += strikethrough(txt).ljust(maxl+2+len(txt))
                else:
                    st += txt.ljust(maxl+2)
        st+='\n'
    print (st)

def edit_distance(s1, s2):
    s1=s1.lower()
    s2=s2.lower()
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]
    
def strikethrough(text):
	result = '\u0336'.join(text) + '\u0336'
	return result
	
	
def Color(text, *args, end=True):
	result = ''
	for a in args:
		result += a
	result += text
	if end:
		result += NRM
	return result
	
	
#################################################
################## MAIN SCRIPT ##################
#################################################



restaurants = []
with open("LUNCH_restaurants_list.txt","r") as f:
	for line in f:
		line = line.rstrip()
		if line[0] != '#':
			restaurants += [line]

longest_string = 100
destination = ""
rest_len = len(restaurants)

################## PHASE 1 ##################

num_rest = int(input(Color("How many restaraunts to start with?  ", HDR)))
while(num_rest<7 or num_rest>rest_len-1):
    print(Color('Not that many!\n', WRN))
    num_rest = int(input(Color("How many restaraunts to start with?  ", HDR)))
    
reduced_rest_list = []
shuffle(restaurants)

history = 'LUNCH_history.txt'
with open(history,'r') as h:
	history_list = [ rst.strip() for rst in h.readlines() ]
num_hist = max(-3,-len(history_list))

while len(reduced_rest_list) < num_rest:
    randint = random.randint(0, rest_len-1)
    rest = restaurants[randint]
    if rest not in reduced_rest_list and rest not in history_list[num_hist:]: 
        reduced_rest_list.append(rest)
       
# Sort list by name (case-insensitive)
reduced_rest_list.sort(key = lambda x: x.lower())
original_list = list(reduced_rest_list)

print()
print(Color(' PHASE 1 '.center(longest_string,'#') + "\n", B))
printlistcolumn(reduced_rest_list)

currentrests = len(reduced_rest_list)
while currentrests > 6:
    thedevilhimself = input(Color("Choose a restaurant to remove from the list: ", HDR))
    if len(thedevilhimself) < 1:
        continue
    if thedevilhimself.isdigit():
        if int(thedevilhimself)>len(reduced_rest_list):
            print(Color('Index Out of Bound. You might love segfaults.', R))
            continue
        elif reduced_rest_list[int(thedevilhimself)-1] == 'deleted':
            print(Color("You can't delete what has already been deleted.", WRN))
            continue
        else:
            toRemove = reduced_rest_list[int(thedevilhimself)-1]
            print(Color("Removing ", HDR) + Color(toRemove, BLD))
            reduced_rest_list[int(thedevilhimself)-1] = 'deleted'
            currentrests -= 1
        #del reduced_rest_list[int(thedevilhimself)-1]
    elif thedevilhimself[0] == '-' and thedevilhimself[1:].isdigit():
        if reduced_rest_list[int(thedevilhimself)] == 'deleted':
            print(Color("You can't delete what has already been deleted.", WRN))
            continue
        toRemove = reduced_rest_list[int(thedevilhimself)]
        print(Color("Removing ", HDR) + Color(toRemove, BLD))
        reduced_rest_list[int(thedevilhimself)] = 'deleted'
        currentrests -= 1
    else:
        toRemove=""
        minEdit=100
    
        for i in reduced_rest_list:
            tmp = edit_distance(thedevilhimself.lower(), i.lower())
            if (tmp<minEdit): minEdit=tmp; toRemove=i
    
        try:
            print(Color("Removing ", HDR) + Color(toRemove, BLD))
            #reduced_rest_list.remove(toRemove)
            reduced_rest_list[reduced_rest_list.index(toRemove)] = 'deleted'
            currentrests -=1
        except ValueError or NameError:
            print(Color("\nThis is not a restaurant in the list...", R))
            print(Color("You probably spelled it wrong genius.", R))
            print(Color("Choose one that is actually in the list.", R))
            time.sleep(3)
        
    print()
    #reduced_rest_list.sort(key = lambda x: x.lower())
    printlistcolumn(reduced_rest_list)
    print()

reduced_rest_list = [r for r in reduced_rest_list if r != 'deleted' ]

print()

################## PHASE 2 ##################
print(Color(' PHASE 2 '.center(longest_string,'#') + "\n", B))

print(Color("These are the 6 restaurants you have chosen for today:\n", HDR) + Color("1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n6. {}\n".format(reduced_rest_list[0], reduced_rest_list[1], reduced_rest_list[2], reduced_rest_list[3], reduced_rest_list[4], reduced_rest_list[5]), BLD))

time.sleep(2)
choice = input(Color("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n", HDR))
print("\033[A" + " "*longest_string + "\033[A")



while not isinstance(choice, int) or (choice != 1 and choice != 2):
	#print("Please input either 1 or 2.")
	#choice = input("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n")
	#while not isinstance(choice, int):
	try: 
		choice = int(choice)
		if choice != 1 and choice != 2:
			raise ValueError
	except ValueError:
		print(Color("\nPlease input either 1 or 2.", WRN))
		choice = input(Color("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n", HDR))
		print(Color(""), end="\r")
		print("\033[A" + " "*longest_string + "\033[A")

print()

if choice == 1:
	#print("Time to roll a die and pick one! Hit enter to roll!")
	#input()
	for i in range(random.randint(1,6)):
		print("Rolling" + "." * i, end="\r")
		time.sleep(1)
	num = random.randint(1, 6)
	print(Color("\nYou rolled a ", HDR) + Color(str(num), G, BLD) + Color("!", HDR))
	destination = reduced_rest_list[num-1]
	
elif choice == 2:
	finalists = {}
	reduced_rest_list.sort()
	for i in range(len(reduced_rest_list)):
		finalists[reduced_rest_list[i]] = 0

	
	
	num_voters = input(Color("Enter number of people who are voting: ", HDR))
	print("\033[A" + " "*longest_string + "\033[A")
	while not isinstance(num_voters, int):
		try:
			num_voters = int(round(float(num_voters)))
			if num_voters < 1: raise ValueError
		except ValueError:
			print(Color("Not a valid input.", R))
			num_voters = input(Color("Enter number of people who are voting: ", HDR))
			print("\033[A" + " "*longest_string + "\033[A")
	
	
	
	if num_voters > 1:
		print(Color("There are %g people voting\n" % num_voters, HDR))
	else:
		print(Color("There is %g person voting\n" % num_voters, HDR))
	
	
	
	for voter in range(num_voters):
		print(Color("Voter number ", HDR) + Color(str(voter+1), G, BLD) + Color(", please enter your top 3 choices in order.", HDR))
		vote1, vote2, vote3 = 0, 0, 0
		
		
		
		# First choice is given 3 points
		vote1 = getpass(Color("First choice (3 points): ", HDR, BLD))
		print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Preventing human errors in input
		while not isinstance(vote1,int):
			try:
				vote1 = int(round(float(vote1)))
				finalists[reduced_rest_list[vote1-1]] += 3
			except ValueError:
				print(Color("Not a valid input.", R))
				vote1 = getpass(Color("Please enter a valid choice: ", HDR, BLD))
				print("\033[A" + " "*longest_string + "\033[A")
			except (IndexError, KeyError) as e:
				print(Color("Your choice is not in the final list.", WRN))
				vote1 = getpass(Color("Please enter a valid choice: ", HDR, BLD))
				print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Second choice is given 2 points
		vote2 = getpass(Color("Second choice (2 points): ", HDR, BLD))
		print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		while True:
			try:
				vote2 = int(round(float(vote2)))
				while vote1 == vote2:
					print(Color("You can't pick the same restaurant more than once.", WRN))
					vote2 = getpass(Color("Please pick a different one: ", HDR,BLD))
					print("\033[A" + " "*longest_string + "\033[A")
					vote2 = int(round(float(vote2)))
				finalists[reduced_rest_list[vote2-1]] += 2
				break
			except ValueError:
				print(Color("Not a valid input.", R))
				vote2 = getpass(Color("Please enter a valid choice: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
			except (IndexError, KeyError) as e:
				print(Color("Your choice is not in the final list.", WRN))
				vote2 = getpass(Color("Please enter a valid choice: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Third choice is given 1 point
		vote3 = getpass(Color("Third choice (1 point): ", HDR, BLD))
		print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		#while vote1 == vote3 or vote2 == vote3:
		#	vote3 = getpass(Color("You can't pick the same restaurant more than once. Please pick a different one: ", WRN))
		#	print("\033[A" + " "*longest_string + "\033[A")
			
		while True:
			try:
				vote3 = int(round(float(vote3)))
				while vote1 == vote3 or vote2 == vote3:
					print(Color("You can't pick the same restaurant more than once.", WRN))
					vote3 = getpass(Color("Please pick a different one: ", HDR,BLD))
					print("\033[A" + " "*longest_string + "\033[A")
					vote3 = int(round(float(vote3)))
				finalists[reduced_rest_list[vote3-1]] += 1
				break
			except ValueError:
				print(Color("Not a valid input.", R))
				vote3 = getpass(Color("Please enter a valid choice: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
			except (IndexError, KeyError) as e:
				print(Color("Your choice is not in the final list.", WRN))
				vote3 = getpass(Color("Please enter a valid choice: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
			
			
	
		print(Color("Voter number ", HDR) + Color(str(voter+1), G, BLD) + Color(" is done.\n", HDR))
		time.sleep(2)
	
	
	
	results = sorted(finalists, key=finalists.get, reverse=True)
	print(Color("The votes are in!", HDR))
	for rest in results:
		print(Color(rest + ": ", BLD) + Color(str(finalists[rest]), G, BLD) + Color(" points", BLD))
	
	
	tie = 1
	for i in range(1,len(results)):
		if finalists[results[0]] == finalists[results[i]]:
			tie += 1
		elif tie > 1:
			del results[i:]
			break	
	
################## PHASE 3+ ##################

	counter = 3
	while tie > 1:
		time.sleep(2)
		print(Color("\nBut we're not done yet!", HDR))
		time.sleep(2)
		print()
		
		phase = " PHASE %g " % counter
		print(Color(phase.center(longest_string, "#") + "\n", B))

		if tie == 2:
			print(Color("We have a tie between ",HDR) + Color(results[0], BLD) + Color(" and ", HDR) + Color(results[1], BLD) + Color(".", HDR))
		elif tie > 2:
			tie_announce = Color("We have a " + str(tie) + "-way tie between ", HDR)
			for i in range(tie):
				if i == tie-2:
					tie_announce += Color(results[i], BLD) + Color(", and ",HDR) + Color(results[i+1], BLD) + Color(".", HDR)
					break
				tie_announce += Color(results[i], BLD) + Color(", ", HDR)
			print(tie_announce)
		
		
		
		tiebreak = {1:"Roll a die!", 2:"Vote again!"}
		print(Color("The final decision! What will it be?", HDR))
		for i in range(len(tiebreak)):
			print(Color("(" + str(i+1) + ") " + tiebreak[i+1], HDR))
		tiebreaker = input()
		print("\033[A" + " "*longest_string + "\033[A")
		
		while not isinstance(tiebreaker, int):
			try:
				tiebreaker = int(round(float(tiebreaker)))
				print(Color("You have chosen to " + tiebreak[tiebreaker].lower(), HDR))
			except ValueError:
				print(Color("Not a valid input.", R))
				tiebreaker = input(Color("Please enter a valid choice: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
			except KeyError:
				print(Color("Your choice is not valid.", WRN))
				tiebreaker = input(Color("Please enter a valid choice: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
				
				
		time.sleep(2)	
		if tiebreaker == 1:
			for i in range(random.randint(1,6)):
				print("Rolling" + "." * i, end="\r")
				time.sleep(1)
			num = random.randint(1, tie)
			print(Color("\nYou rolled a ", HDR) + Color(str(num), G, BLD) + Color("!", HDR))
			destination = results[num-1]
			break
			
		elif tiebreaker == 2:
			final = { results[i-1]:0 for i in range(1,len(results)+1) }
			print()
			print(Color("Here is the list:", HDR))
			for i in range(len(results)):
				print(Color("(" + str(i+1) + ") " + results[i], BLD))
				
			time.sleep(2)
			print(Color("Only 1 vote per person. Choose wisely.", HDR, BLD))
			time.sleep(2)
			
			for voter in range(num_voters):
				vote = getpass(Color("Voter number ", HDR) + Color(str(voter+1), G, BLD) + Color(", please enter your vote: ", HDR))
				print("\033[A" + " "*longest_string + "\033[A")
				
				while not isinstance(vote,int):
					try:
						vote = int(round(float(vote)))
						final[results[vote-1]] += 1
					except ValueError:
						print(Color("Not a valid input.", R))
						vote = getpass(Color("Please enter a valid choice: ", HDR))
						print("\033[A" + " "*longest_string + "\033[A")
					except (IndexError, KeyError) as e:
						print(Color("Your choice is not valid.", WRN))
						vote = getpass(Color("Please enter a valid choice: ", HDR))
						print("\033[A" + " "*longest_string + "\033[A")
				
				print(Color("Voter number ", HDR) + Color(str(voter+1), G, BLD) + Color(" is done.\n", HDR))
				time.sleep(2)
			
			results = sorted(final, key=final.get, reverse=True)
			print(Color("The final votes have been casted!", HDR, BLD))
			time.sleep(2)
			print(Color("Here is the result:", HDR))
			for rest in results:
				print(Color(rest + ": ", BLD) + Color(str(final[rest]), G, BLD) + Color(" points", BLD))
			destination = results[0]
		
		tie = 1
		for i in range(1,len(results)):
			if final[results[0]] == final[results[i]]:
				tie += 1
			elif tie > 1:
				del results[i:]
				break
		counter += 1
	else:	
		destination = results[0]

		
	
################## FINAL RESULTS ##################

time.sleep(1)	
print()
print(Color("Today's lunch will be at ", HDR) + Color(destination, G, BLD))
print(Color("Enjoy! :)", HDR))

hist_flag = 1
if hist_flag > 0:
	with open(history,'a') as hist:
		hist.write('\n'+destination)



