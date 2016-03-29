'''
This program splits the entire output into 9 x 9 pieces, and recognise the character in each piece to construct the board of sudoku
'''

from PIL import Image
import pytesseract

def generateBoard(output):

	# initialise board to be a 9 x 9 matrix with default value 0
	board = [[0] * 9 for _ in range(9)]

	for i in range(9):
		for j in range(9):
			# split the entire output into 9 x 9 pieces and assign each piece to tmp
			tmp = output[i * 50 + 5: (i + 1) * 50 - 5, j * 50 + 5 : (j + 1) * 50 - 5]
			# convert tmp into an Image object
			im = Image.fromarray(tmp)

			# use pytesseract to recognise digits in each block of the output
			# setting image_to_string to single character mode using config = '-psm 10'
			char = pytesseract.image_to_string(im, config = '-psm 10')

			# if the recognised character is a digit, update the original value of board into the recognised digits
			try:
				board[i][j] = int(char)
			# otherwise, keep the original value of board
			except:
				continue

	return board