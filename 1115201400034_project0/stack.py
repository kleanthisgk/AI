class Stack:
	def __init__(self): #initialize stack
		self.stackList = [] #list is empty

	def empty(self): #check if list is empty
		return not self.stackList #returns true if list is empty

	def push(self, c): #insert item at the end of the list
		self.stackList.append(c)

	def pop(self): #remove last item of the list
		return self.stackList.pop() #returns the item that was removed


def match(c, d): #check if parenthesis match
	if ( c == '(' ):
		return d == ')' # returns true if c = ( and d = )
	elif ( c == '[' ):
		return d == ']' #returns true if c = [ and d = ]
	elif ( c == '{' ):
		return d == '}' #returns true if c = { and d = }


def balanced(s): #checks if input string is balanced
	l = len(s) #l is the length of the input string
	stack = Stack() #create the stack
	i = 0 #i is the index of the input string
	left = ['(', '[', '{'] # a list with left parenthesis
	right = [')', ']', '}'] # a list with right parenthesis
	while ( i < l ): # a loop for every character of the input string
		d = s[i] # d is the character of the input string that the index points to
		if ( d in left ): # check if d is in left parenthesis
			stack.push(d) #insert it into stack
		elif ( d in right ): #check if d is in right parenthesis
			if ( stack.empty() ): #if stack is empty there are more right parenthesis
				print "More right parentheses than left"
				return
			else:
				c = stack.pop() #if stack is not empty remove the last item of the stack
				if ( not match(c, d) ): #if parenthesis dont match the input string is not balanced 
					print "Mismatched parentheses: ", c, d
					return
		else: #if input string doesnt contain only parenthesis
			print "Invalid character"
			return
		i = i + 1 #index points to the next character of the input string
	if ( stack.empty() ): # if the stack is empty the input string is balanced
		print "Parentheses are balanced properly"
	else: # if after the loop the stack is still not empty there are more lefte parenthesis than right
		print "More left parentheses than right"


if __name__ == '__main__':
	inputString = raw_input("Please enter string: ") # ask the user for an input string
	print "string entered is:", inputString
	balanced(inputString) #check if the input string is balanced