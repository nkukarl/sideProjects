'''
This program generates answer for sudoku image file
'''

from PIL import Image, ImageDraw, ImageFont

def generateAnswer(image, board, original):

	img = Image.open(image)

	# mac
	myfont = ImageFont.truetype('/Library/Fonts/verdana.ttf', 100)
	
	# ubuntu
	# myfont = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-B.ttf', 100)

	for i in range(9):
		for j in range(9):
			# if the original sudoku board is 0, update the 
			if original[i][j] == 0:
				ImageDraw.Draw(img).text((40 + j * 115, 5 + 115 * i), str(board[i][j]), font = myfont, fill = 'red')

	# add 'solve_' to the original image file name and save it to folder Answer
	newImg = './Answers/solved_' + image.split('/')[-1]
	img.save(newImg)