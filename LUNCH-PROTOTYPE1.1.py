import sys
import random
from random import shuffle
import time
import math
def printlistcolumn(reduced_rest_list):
    st = ''
    maxl = 35
    onethird = int(math.ceil(len(reduced_rest_list)*1.0/3))
    for idx in  range(0, onethird):
        for jdx in [idx,idx+onethird,idx+onethird*2]:
            if(jdx<len(reduced_rest_list)):
                if(reduced_rest_list[jdx] == 'deleted'):
                    st+='----------'.ljust(maxl+2)
                else:
                    st+=(str(jdx+1)+'. '+reduced_rest_list[jdx]).ljust(maxl+2)
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

restaurants = []
with open("LUNCH_restaurants_list.txt","r") as f:
	for line in f:
		line = line.rstrip()
		restaurants += [line]

longest_string = 100
destination = ""
rest_len = len(restaurants)

num_rest = int(input("How many restaraunts to start with?  "))
while(num_rest>rest_len-1):
    print ('\nNot that many!\n')
    num_rest = int(input("How many restaraunts to start with?  "))
    
reduced_rest_list = []

shuffle(restaurants)

while len(reduced_rest_list) < num_rest:
    randint = random.randint(0, rest_len-1)
    rest = restaurants[randint]
    if rest not in reduced_rest_list: 
        reduced_rest_list.append(rest)
       
# Sort list by name (case-insensitive)
reduced_rest_list.sort(key = lambda x: x.lower())

print("############## PHASE 1 ##############\n")
printlistcolumn(reduced_rest_list)


while len(reduced_rest_list) > 6:
    inpt = input("Choose a restaurant to remove from the list: ")
    thedevilhimself = str(inpt)
    if thedevilhimself.isdigit():
        if int(thedevilhimself)>len(reduced_rest_list):
            print ('Index Out of Bound. You might love segfaults.')
            continue
        reduced_rest_list[int(thedevilhimself)-1] = 'deleted'
        #del reduced_rest_list[int(thedevilhimself)-1]
    else:
        toRemove=""
        minEdit=100
    
        for i in reduced_rest_list:
            tmp = edit_distance(thedevilhimself.lower(), i.lower())
            if (tmp<minEdit): minEdit=tmp; toRemove=i
    
        try:
            print("Removing {}".format(toRemove))
            #reduced_rest_list.remove(toRemove)
            reduced_rest_list[reduced_rest_list.index(toRemove)] = 'deleted'
        except ValueError or NameError:
            print("\nThis is not a restaurant in the list...")
            print("You probably spelled it wrong genius.")
            print("Choose one that is actually in the list.")
            time.sleep(3)
        
    print("\n")
    #reduced_rest_list.sort(key = lambda x: x.lower())
    printlistcolumn(reduced_rest_list)
    print("\n")


print()
print("############## PHASE 2 ##############\n")
print("These are the 6 restaurants you have chosen for today:\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n6. {}\n".format(reduced_rest_list[0], reduced_rest_list[1], reduced_rest_list[2], reduced_rest_list[3], reduced_rest_list[4], reduced_rest_list[5]))


choice = input("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n")
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
		print("\nPlease input either 1 or 2.")
		choice = input("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n")
		print("\033[A" + " "*longest_string + "\033[A")

print()

if choice == 1:
	#print("Time to roll a die and pick one! Hit enter to roll!")
	#input()
	for i in range(random.randint(1,6)):
		print("Rolling" + "." * i, end=="\r")
		time.sleep(1)
	num = random.randint(1, 6)
	print("\nYou rolled a {}!".format(num))
	destination = reduced_rest_list[num-1]
	
elif choice == 2:
	finalists = {}
	reduced_rest_list.sort()
	for i in range(len(reduced_rest_list)):
		finalists[reduced_rest_list[i]] = 0
	
	
	
	print("Final list:\n")
	for i in range(len(reduced_rest_list)):
		print("%g. " % (i+1) + reduced_rest_list[i])
	print()
	
	
	
	num_voters = input("Enter number of people who are voting: ")
	print("\033[A" + " "*longest_string + "\033[A")
	while not isinstance(num_voters, int):
		try:
			num_voters = int(round(float(num_voters)))
			if num_voters < 1: raise ValueError
		except ValueError:
			print("Not a valid input.")
			num_voters = input("Enter number of people who are voting: ")
			print("\033[A" + " "*longest_string + "\033[A")
	
	
	
	if num_voters > 1:
		print("There are %g people voting\n" % num_voters)
	else:
		print("There is %g person voting\n" % num_voters)
	
	
	
	for voter in range(num_voters):
		print("Voter number %g, please enter the indices of your top 3 choices in order." % (voter+1))
		vote1, vote2, vote3 = 0, 0, 0
		
		
		
		# First choice is given 3 points
		vote1 = input("First choice (3 points): ")
		print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Preventing human errors in input
		while not isinstance(vote1,int):
			try:
				vote1 = int(round(float(vote1)))
				finalists[reduced_rest_list[vote1-1]] += 3
			except ValueError:
				print("Not a valid input.")
				vote1 = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
			except (IndexError, KeyError) as e:
				print("Your choice is not in the final list.")
				vote1 = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Second choice is given 2 points
		vote2 = input("Second choice (2 points): ")
		print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Prevents one choice from getting stacked
		
		
		
		
		while True:
			try:
				vote2 = int(round(float(vote2)))
				while vote1 == vote2:
					vote2 = input("You can't pick the same restaurant more than once. Please pick a different one: ")
					print("\033[A" + " "*longest_string + "\033[A")
					vote2 = int(round(float(vote2)))
				finalists[reduced_rest_list[vote2-1]] += 2
				break
			except ValueError:
				print("Not a valid input.")
				vote2 = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
			except (IndexError, KeyError) as e:
				print("Your choice is not in the final list.")
				vote2 = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		# Third choice is given 1 point
		vote3 = input("Third choice (1 point): ")
		print("\033[A" + " "*longest_string + "\033[A")
		
		
		
		while vote1 == vote3 or vote2 == vote3:
			vote3 = input("You can't pick the same restaurant more than once. Please pick a different one: ")
			print("\033[A" + " "*longest_string + "\033[A")
			
		while True:
			try:
				vote3 = int(round(float(vote3)))
				while vote1 == vote3 or vote2 == vote3:
					vote3 = input("You can't pick the same restaurant more than once. Please pick a different one: ")
					print("\033[A" + " "*longest_string + "\033[A")
					vote3 = int(round(float(vote3)))
				finalists[reduced_rest_list[vote3-1]] += 1
				break
			except ValueError:
				print("Not a valid input.")
				vote3 = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
			except (IndexError, KeyError) as e:
				print("Your choice is not in the final list.")
				vote3 = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
			
			
	
		print("Voter number %g is done.\n" % (voter+1))
		time.sleep(2)
	
	
	
	results = sorted(finalists, key=finalists.get, reverse=True)
	print("The votes are in!")
	for rest in results:
		print( rest + ": " + str(finalists[rest]) + " points" )
	
	
	tie = 1
	for i in range(1,len(results)):
		if finalists[results[0]] == finalists[results[i]]:
			tie += 1
		elif tie > 1:
			del results[i:]
			break	
	
	
	
	while tie > 1:
		time.sleep(2)
		print("But we're not done yet!")
		time.sleep(2)
		print()

		if tie == 2:
			print("We have a tie between " + results[0] + " and " + results[1] + ".")
		elif tie > 2:
			tie_announce = "We have a " + str(tie) + "-way tie between "
			for i in range(tie):
				if i == tie-2:
					tie_announce += results[i] + ", and " + results[i+1] + "."
					break
				tie_announce += results[i] + ", "
			print(tie_announce)
		
		
		
		tiebreak = {1:"Roll a die!", 2:"Vote again!"}
		print("The final decision! What will it be?")
		for i in range(len(tiebreak)):
			print("(" + str(i+1) + ") " + tiebreak[i+1])
		tiebreaker = input()
		print("\033[A" + " "*longest_string + "\033[A")
		
		while not isinstance(tiebreaker, int):
			try:
				tiebreaker = int(round(float(tiebreaker)))
				print("You have chosen to " + tiebreak[tiebreaker].lower())
			except ValueError:
				print("Not a valid input.")
				tiebreaker = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
			except KeyError:
				print("Your choice is not valid.")
				tiebreaker = input("Please enter a valid choice: ")
				print("\033[A" + " "*longest_string + "\033[A")
				
				
		time.sleep(2)	
		if tiebreaker == 1:
			for i in range(random.randint(1,6)):
				print("Rolling" + "." * i, end=="\r")
				time.sleep(1)
			num = random.randint(1, tie)
			print("\nYou rolled a {}!".format(num))
			destination = results[num-1]
			break
			
		elif tiebreaker == 2:
			final = { results[i-1]:0 for i in range(1,len(results)+1) }
			print()
			print("Here is the list choices:")
			for i in range(len(results)):
				print("(" + str(i+1) + ") " + results[i])
				
			time.sleep(2)
			print("Only 1 vote per person. Choose wisely.")
			time.sleep(2)
			
			for voter in range(num_voters):
				vote = input("Voter number %g, please enter your vote: " % (voter+1))
				print("\033[A" + " "*longest_string + "\033[A")
				
				while not isinstance(vote,int):
					try:
						vote = int(round(float(vote)))
						final[results[vote-1]] += 1
					except ValueError:
						print("Not a valid input.")
						vote = input("Please enter a valid choice: ")
						print("\033[A" + " "*longest_string + "\033[A")
					except (IndexError, KeyError) as e:
						print("Your choice is not valid.")
						vote = input("Please enter a valid choice: ")
						print("\033[A" + " "*longest_string + "\033[A")
				
				print("Voter number %g is done." % (voter+1))
				time.sleep(2)
			
			results = sorted(final, key=final.get, reverse=True)
			print("The final votes have been casted!")
			time.sleep(2)
			print("Here is the result:")
			for rest in results:
				print(rest + ": " + str(final[rest]) + " points" )		
			destination = results[0]
		
		tie = 1
		for i in range(1,len(results)):
			if final[results[0]] == final[results[i]]:
				tie += 1
			elif tie > 1:
				del results[i:]
				break
	else:	
		destination = results[0]

		
	

time.sleep(3)	
print()
print("Today's lunch will be at {}.".format(destination))
print("Enjoy! :)")



