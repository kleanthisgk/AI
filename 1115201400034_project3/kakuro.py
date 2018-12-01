from search import *
from utils import *
from grids import *
from csp import *
import time

class Kakuro(CSP):
	def __init__(self, grid):
		#runs is a list of lists with 2 items
		#the first item is the sum and the second is a list with the variables that are in the sum
		self.variables = self.setVariables(grid) #assign values
		self.domains = self.setDomains(self.variables) #assign domains
		self.runs, self.neighbors = self.setRunsAndNeighbors(grid, self.variables) #assign runs and neighbors
		#print("Variables are", self.variables)
		#print("\nDomains are", self.domains)
		#print("\nNeighbors are", self.neighbors)
		CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraints)

	def setVariables(self, grid):
		variables = []
		for i in range(len(grid)): #lines of grid
			for j in range(len(grid[i])): #columns of grid
				if grid[i][j] == '_': # _ means that its a variable
					var = 'X' + '_' + str(i) + '_' + str(j) #variable is of the type X_i_j where i is the line and j is the  column
					variables.append(var)
		return variables

	def setDomains(self, variables): #domains are 1-9 for all variables
		return {var:list(range(1,10)) for var in variables}

	def setRunsAndNeighbors(self, grid, variables):
		items = []
		runs = [] 
		m = 0
		for i, line in enumerate(grid): #line of grid
			for j, value in enumerate(line): #column of grid
				if value != '*' and value != '_' : #value is of the type [x,y] where x is the sum below and y th sum to the right
					if value[0] != '': #'' means there is sum below
						for k in range(i+1, len(grid)): #go to the lines below and append every variable
							if grid[k][j] == '_':
								var = 'X' + '_' + str(k) + '_' + str(j)
								items.append(var)
							else:
								break #it means that there is no variable left
						runs.append([value[0], items]) #runs is explained in the constructor
						items = []
					if value[1] != '': #there is sum to the right
						for k in range(j+1, len(line)): #go the columns to the right and do the same as above
							if grid[i][k] == '_':
								var = 'X' + '_' + str(i) + '_' + str(k)
								items.append(var)
							else:
								break
						runs.append([value[1], items])
						items = []
		neighbors = {}
		for var in variables: #for every valuable1
			neighbors[var] = []
			for run in runs: #for every run
				if var in run[1]: #every variable2 that is in the same run as the variable1 is added to neighbors of 1
					for item in run[1]:
						if item != var:
							neighbors[var].append(item)
		return runs, neighbors

	def constraints(self, A, a, B, b):
		if a == b: #if values are same
			return False
		for i, run in enumerate(self.runs):
			if A in self.runs[i][1] and B in self.runs[i][1]: #if variables are on the same run
				if len(self.runs[i][1]) == 2: #if they are the only ones then their sum must be equal to the sum of the run
					return (a + b) == self.runs[i][0]
				elif len(self.runs[i][1]) > 2:
					m = 0 #the number of variables in assignment
					flagA = 0
					flagB = 0
					summ = 0
					for item in self.runs[i][1]: #for every variable in run
						if item in self.infer_assignment().keys(): #if variable is already assigned
							m = m + 1
							if item != A and item != B:
								summ += self.infer_assignment()[item] #summ is the sum of all variables except A and B
							elif item == A:
								flagA = 1
							elif item == B:
								flagB = 1
					if (m == 0 and flagA == 0 and flagB == 0) or (m == 1 and flagA == 1 or flagB == 1) or (m == 2 and flagA == 1 and flagB == 1): #if no variable of the run is assigned
						return (a + b) < self.runs[i][0] #the sum of a and b has to be smaller than the sum required because more variables will be added
					elif m == (len(self.runs[i][1]) - 2) and flagA == 0 and flagB == 0: #if every variable in run is assigned except A and B
						return (a + b) == (self.runs[i][0] - summ)	
					else: #if some variables are assigned and some are not
						return (a + b) < (self.runs[i][0] - summ)
		return False


if __name__ == "__main__":
	#choose between grid1, grid2, grid3, grid4
	#difficulty: grid1 < grid2 < grid3 < grid4
	grid = grid1
	print_table(grid) #print the grid to check the solution

	#use every backtracking algorithm in the csp
	kakuro = Kakuro(grid)
	print()
	print("Backtracking Search starting")
	start = time.clock()
	solution_BT = backtracking_search(kakuro)
	end = time.clock()
	print("Backtracking Search finished in time", end - start)
	print("Solution of Backtracking Search is\n", solution_BT)

	
	kakuro = Kakuro(grid)
	print()
	print("Backtracking Search with Forward Checking starting")
	start = time.clock()
	solution_BT_FC = backtracking_search(kakuro, inference = forward_checking)
	end = time.clock()
	print("Backtracking Search with Forward Checking finished in time", end - start)
	print("Solution of Backtracking Search with Forward Checking is\n", solution_BT_FC)

	
	kakuro = Kakuro(grid)
	print()
	print("Backtracking Search with Maintaining Arc Constistency starting")	
	start = time.clock()
	solution_BT_MAC = backtracking_search(kakuro, inference = mac)
	end = time.clock()
	print("Backtracking Search with Maintaining Arc Constistency finished in time", end - start)
	print("Solution of Backtracking Search with Maintaining Arc Constistency is\n", solution_BT_MAC)

	kakuro = Kakuro(grid)	
	print()
	print("Backtracking Search with Minimum Remaining Values starting")
	start = time.clock()
	solution_BT_MRV = backtracking_search(kakuro, select_unassigned_variable = mrv)
	end = time.clock()
	print("Backtracking Search with Minimum Remaining Values finished in time", end - start)
	print("Solution of Backtracking Search with Minimum Values is\n", solution_BT_MRV)

	kakuro = Kakuro(grid)
	print()
	print("Backtracking Search with Forward Checking and Minimum Remaining Values starting")
	start = time.clock()
	solution_BT_FC_MRV = backtracking_search(kakuro, select_unassigned_variable = mrv, inference = forward_checking)
	end = time.clock()
	print("Backtracking Search with Forward Checking and Minimum Remaining Values finished in time", end - start)
	print("Solution of Backtracking Search with Forward Checking and Minimum Remaining Values is\n", solution_BT_FC_MRV)
