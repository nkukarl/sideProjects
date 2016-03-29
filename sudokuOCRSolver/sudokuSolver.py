'''
This program reads in a 2D matrix as a board of sudoku and returns the solution
'''

class SudokuSolver:
	def solve(self, board):
		'''
		Main function
		'''
		self.possibleVals(board)
		self.solver(board)

	def possibleVals(self, board):
		'''
		Create a dictionary self.valsMap to store the possible values for each location
		Each dictionary entry in the format of (r, c) = [val1, val2, ...]
		'''
		self.valsMap = dict() # Dictionary initialisation
		for row in range(9):
			for col in range(9):
				
				if board[row][col] == 0: # only search for locations with 0
					vals = [n + 1 for n in range(9)] # all possible values
					key = (row, col)
					unavail = set() # unavailable values initialised to empty
					
					# check values existing in the same row and add them to unavail
					for c in range(9):
						if board[row][c] != 0:
							unavail.add(board[row][c])

					# check values existing in the same column and add them to unavail
					for r in range(9):
						if board[r][col] != 0:
							unavail.add(board[r][col])

					# check values existing in the same block and add them to unavail
					for vShift in range(3): # vertical shift
						for hShift in range(3): # horizontal shift
							r, c = row // 3 * 3 + vShift, col // 3 * 3 + hShift
							if board[r][c]:
								unavail.add(board[r][c])

					# remove values in unavail from all possible values
					for val in unavail:
						vals.remove(val)

					# create a dictionary entry
					self.valsMap[key] = vals

	def solver(self, board):
		if len(self.valsMap) == 0:
			return True
		kee = min(self.valsMap.keys(), key = lambda x: len(self.valsMap[x]))
		nums = self.valsMap[kee]

		for n in nums:
			(i, j) = kee
			board[i][j] = n
			update = {kee: self.valsMap[kee]}
			del self.valsMap[kee]
			valid = True
			for ind in self.valsMap.keys():
				if n in self.valsMap[ind]:
					if ind[0] == i or ind[1] == j or (ind[0] // 3, ind[1] // 3) == (i // 3, j // 3):
						update[ind] = n
						self.valsMap[ind].remove(n)
						if len(self.valsMap[ind]) == 0:
							valid = False
							break
			if valid and self.solver(board):
				return True
			board[i][j] == 0
			self.valsMap = self.undo(update)
		return False

	def undo(self, update):
		for k in update:
			if k not in self.valsMap:
				self.valsMap[k] = update[k]
			else:
				self.valsMap[k].append(update[k])
		return self.valsMap

# test case

if __name__ == '__main__':

	board = [
	[5, 4, 1, 7, 8, 9, 3, 2, 6],
	[9, 7, 3, 1, 6, 2, 5, 4, 8],
	[0, 0, 2, 5, 4, 3, 1, 7, 9],
	[4, 1, 9, 2, 5, 6, 7, 8, 3],
	[3, 2, 6, 8, 7, 4, 9, 5, 1],
	[0, 0, 0, 3, 9, 1, 2, 6, 4],
	[1, 0, 8, 0, 2, 5, 4, 3, 7],
	[0, 3, 0, 0, 1, 7, 8, 9, 0],
	[0, 0, 0, 0, 3, 8, 6, 1, 0]
	]
	solver = SudokuSolver()

	solver.solve(board)

	print 'answer:'
	for row in board:
		for n in row:
			print n,
		print