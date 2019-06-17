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

CLR = '\033[2K'		# Clear line
UPL = '\033[A'		# Move cursor up

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

def clearInput():
	print(UPL + CLR, end='')

#################################################
################## LUNCH CLASS ##################
#################################################

class LUNCH:
	big_str = 100
	destination = ""
	history = 'LUNCH_history.txt'
	def __init__(self, restaurant_list_file):
		print(Color('Initializing...', BLD, R, end=False), end='')
		self.restaurants = []
		with open(restaurant_list_file, 'r') as f:
			for line in f:
				line = line.rstrip()
				if line[0] != '#':	self.restaurants += [line]
		rest_len = len(self.restaurants)
		
		with open(self.history,'r') as h:
			self.history_list = [ rst.strip() for rst in h.readlines() ]
		print(Color('done'))
	
	def Setup(self, restaurants, history):
		print(Color('Setting up...', BLD, R, end=False), end='')
		shuffle(restaurants)

		num_rest = int(input(Color("How many restaraunts to start with?  ", HDR)))
		while(num_rest<7 or num_rest>rest_len-1):
			print(Color('Not that many!\n', WRN))
			num_rest = int(input(Color("How many restaraunts to start with?  ", HDR)))
		
		num_hist = max(-3,-len(self.history_list))
		self.reduced_rest_list = []
		while len(reduced_rest_list) < num_rest:
			r_int = random.randint(0, rest_len-1)
			rest = restaurants[r_int]
			if rest not in reduced_rest_list and\
			   rest not in history_list[num_hist:]:
				reduced_rest_list.append(rest)
		# Sort list by name (case-insensitive)
		self.reduced_rest_list.sort(key = lambda x: x.lower())
		self.original_list = list(self.reduced_rest_list)
		print(Color('done'))

	def PHASE1(self):
		print('\n' + Color(' PHASE 1 '.center(big_str,'#') + '\n', B))
		printlistcolumn(reduced_rest_list)
		
		currentrests = len(self.reduced_rest_list)
		while currentrests > 6:
			thedevilhimself = input(Color("Choose a restaurant to remove from the list: ", HDR))
			if len(thedevilhimself) < 1: continue
			if thedevilhimself.isdigit():
				if int(thedevilhimself)>len(reduced_rest_list):
					print(Color('Index Out of Bound. You might love segfaults.', R))
					continue
				elif self.reduced_rest_list[int(thedevilhimself)-1] == 'deleted':
					print(Color("You can't delete what has already been deleted.", WRN))
					continue
				else:
					toRemove = self.reduced_rest_list[int(thedevilhimself)-1]
					print(Color("Removing ", HDR) + Color(toRemove, BLD))
					self.reduced_rest_list[int(thedevilhimself)-1] = 'deleted'
					currentrests -= 1
			elif thedevilhimself[0] == '-' and thedevilhimself[1:].isdigit():
				if self.reduced_rest_list[int(thedevilhimself)] == 'deleted':
					print(Color("You can't delete what has already been deleted.", WRN))
					continue
				toRemove = self.reduced_rest_list[int(thedevilhimself)]
				print(Color("Removing ", HDR) + Color(toRemove, BLD))
				self.reduced_rest_list[int(thedevilhimself)] = 'deleted'
				currentrests -= 1
			else:
				toRemove=""
				minEdit=100
		
				for i in self.reduced_rest_list:
					tmp = edit_distance(thedevilhimself.lower(), i.lower())
					if tmp < minEdit: minEdit = tmp; toRemove = i
		
				try:
					print(Color("Removing ", HDR) + Color(toRemove, BLD))
					self.reduced_rest_list[self.reduced_rest_list.index(toRemove)] = 'deleted'
					currentrests -=1
				except ValueError or NameError:
					print(Color("\nThis is not a restaurant in the list..."	, R))
					print(Color("You probably spelled it wrong genius."		, R))
					print(Color("Choose one that is actually in the list."	, R))
					time.sleep(3)

			print()
			printlistcolumn(reduced_rest_list)
			print()
		self.reduced_rest_list = [ r for r in reduced_rest_list if r != 'deleted' ]

	def PHASE2(self):
		print('\n' + Color(' PHASE 2 '.center(big_str,'#') + '\n', B))
		r1,r2,r3,r4,r5,r6 = self.reduced_rest_list[:6]
		print(Color('These are the 6 restaurants you have chosen for today:\n', HDR) + Color(f'1. {r1}\n2. {r2}\n3. {r3}\n4. {r4}\n5. {r5}\n6. {r6}\n'), BLD))
		time.sleep(2)
		choice = input(Color("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n", HDR))
		clearInput()
		
		while True:
			try:
				choice = int(choice)
				if choice != 1 and choice != 2:
					raise ValueError
				break
			except:
				print(Color("\nPlease input either 1 or 2.", WRN))
				choice = input(Color("Make a choice:\n" + "(1) Roll a die\n" + "(2) Vote\n", HDR))
				print(Color(""), end="\r")
				clearInput()
		print()
		
		if choice == 1:
			for i in range(random.randint(1,6)):
				print("Rolling" + "." * i, end="\r")
				time.sleep(1)
			num = random.randint(1,6)
			print(Color("\nYou rolled a ", HDR) + Color(str(num), G, BLD) + Color("!", HDR))
			destination = reduced_rest_list[num-1]
	
		elif choice == 2:
			finalists = {}
			self.reduced_rest_list.sort()
			for i in range(len(self.reduced_rest_list)):
				finalists[self.reduced_rest_list[i]] = 0

	
	
			num_voters = input(Color("Enter number of people who are voting: ", HDR))
			clearInput()
			while not isinstance(num_voters, int):
				try:
					num_voters = int(round(float(num_voters)))
					if num_voters < 1: raise ValueError
				except ValueError:
					print(Color("Not a valid input.", R))
					num_voters = input(Color("Enter number of people who are voting: ", HDR))
					clearInput()
	
	
	
			if num_voters != 1:
				print(Color(f'There are {num_voters} people voting\n', HDR))
			else:
				print(Color(f'There is 1 person voting\n', HDR))
	
	
	
			for voter in range(num_voters):
				pts = 3
				print(Color('Voter number ', HDR) + Color(str(voter+1), G, BLD) + Color(f', please enter your top {pts} choices in order.', HDR))
				voted = 0
				vote_list = []
				while pts > 0:
					v = getpass(Color(f'Choice {voted+1} ({pts} points): ', HDR, BLD))
					clearInput()
					while True:
						try:
							v = int(round(float(v)))
							while v in vote_list:
								print(Color("You can't pick the same restaurant!",WRN))
								v = getpass(Color("Please pick a different one: ", HDR,BLD))
								clearInput()
								v = int(round(float(v)))
							finalists[reduced_rest_list[v-1]] += pts
							vote_list += [v]
							voted += 1; pts -= 1
							break
						except ValueError:
							print(Color("Not a valid input.", R))
							v = getpass(Color("Please enter a valid choice: ", HDR))
							clearInput()
						except (IndexError, KeyError) as e:
							print(Color("Your choice is not in the final list.", WRN))
							v = getpass(Color("Please enter a valid choice: ", HDR))
							clearInput()

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
		
		
		
		
		
		
		
		
		
		
			
			
			
			
			




