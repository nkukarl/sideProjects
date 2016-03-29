'''
This is the main file of a sudoku OCR solver
It reads in all the png files in Questions folder, performing

- image processing
- sudoku board generation
- sudoku solving
- answer generation

All the answers are saved in Answer folder
'''

import imageProcessing
import boardGeneration
import sudokuSolver
import answerGeneration
import glob
import copy

# find all png files in Questions folder
images = glob.glob('./Questions/*.png')
# sort file names
images.sort()

for image in images: # solve each question
	
	# obtain output file
	output = imageProcessing.generateOutput(image)

	# create sudoku board
	board = boardGeneration.generateBoard(output)

	# make a copy of sudoku board
	original = copy.deepcopy(board)

	# solve sudoku
	solver = sudokuSolver.SudokuSolver()
	solver.solve(board)

	# generate answer
	newImage = answerGeneration.generateAnswer(image, board, original)
	
	# prompt to update progress
	print image.split('/')[-1][:-4] + ' solved!'

