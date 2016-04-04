from Tkinter import *
import random
from datetime import datetime
from tabulate import tabulate

# create number colour dictionary
# rgb code from http://www.w3schools.com/colors/colors_picker.asp
colours = {0: '#ffe6e6', 2: '#ffcccc', 4: '#ffb3b3', 8: '#ff9999', 16: '#ff8080', 32: '#ff6666', 64: '#ff4d4d', 128: '#ff3333', 256: '#ff1a1a', 512: '#ff0000', 1024: '#e60000', 2048: '#cc0000', 4096: '#b30000'}

class Game(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.grid()
		self.master.title('2048')
		self.master.bind('<KeyPress>', self.getChar)

		self.dirnMap = {
		"u'\uf700'": 'up',
		"u'\uf701'": 'down',
		"u'\uf702'": 'left',
		"u'\uf703'": 'right'
		}

		self.isOver = False
		self.init()

		self.canvas = Canvas(self, width = 620, height = 620)
		self.canvas.pack()

		self.tStart = datetime.now()
		
		self.canvasDraw()

		self.mainloop()

	def canvasDraw(self):
		self.canvas.delete('all')

		# draw horizontal lines
		self.canvas.create_line(10, 10, 610, 10)
		self.canvas.create_line(10, 160, 610, 160)
		self.canvas.create_line(10, 310, 610, 310)
		self.canvas.create_line(10, 460, 610, 460)
		self.canvas.create_line(10, 610, 610, 610)

		# draw vertical lines
		self.canvas.create_line(10, 10, 10, 610)
		self.canvas.create_line(160, 10, 160, 610)
		self.canvas.create_line(310, 10, 310, 610)
		self.canvas.create_line(460, 10, 460, 610)
		self.canvas.create_line(610, 10, 610, 610)

		# display matrix content

		for i in range(4):
			for j in range(4):
				num = self.matrix[i][j]
				x, y = 85 + 150 * j, 85 + 150 * i
				self.canvas.create_rectangle(10 + 150 * j, 10 + 150 * i, 160 + 150 * j, 160 + 150 * i, fill = colours[num])
				if self.matrix[i][j] != 0:
					self.canvas.create_text(x, y, text = str(num), font = ('Serif', 80 - len(str(num)) * 5, 'bold'))

	def thumbnailDraw(self):

		self.canvas.create_rectangle(10, 10, 610, 610, fill = 'grey')
		self.canvas.create_text(310, 450, text = 'Game over!', fill = 'red', font = ('Serif', 50, 'bold'))

		# draw horizontal lines
		self.canvas.create_line(150, 50, 470, 50)
		self.canvas.create_line(150, 130, 470, 130)
		self.canvas.create_line(150, 210, 470, 210)
		self.canvas.create_line(150, 290, 470, 290)
		self.canvas.create_line(150, 370, 470, 370)

		# draw vertical lines
		self.canvas.create_line(150, 50, 150, 370)
		self.canvas.create_line(230, 50, 230, 370)
		self.canvas.create_line(310, 50, 310, 370)
		self.canvas.create_line(390, 50, 390, 370)
		self.canvas.create_line(470, 50, 470, 370)
		
		# display matrix content

		for i in range(4):
			for j in range(4):
				num = self.matrix[i][j]
				x, y = 190 + 80 * j, 90 + 80 * i
				self.canvas.create_rectangle(150 + 80 * j, 50 + 80 * i, 230 + 80 * j, 130 + 80 * i, fill = colours[num])
				if self.matrix[i][j] != 0:
					self.canvas.create_text(x, y, text = str(num), font = ('Serif', 40 - len(str(num)) * 5, 'bold'))

		self.canvas.create_text(310, 550, text = '\n'.join(self.summary), font = ('Serif', 24, 'bold'))

	def init(self):
		self.matrix = [[0] * 4 for _ in range(4)]
		indices = [i for i in range(16)]
		random.shuffle(indices)
		pos = indices[:2]
		row0, col0 = pos[0] // 4, pos[0] % 4
		row1, col1 = pos[1] // 4, pos[1] % 4
		self.matrix[row0][col0] = 2
		self.matrix[row1][col1] = 2

	def move(self, dirn):
		# print dirn, 'pressed'
		flag = 0
		if dirn == 'up' or dirn == 'down':
			for j in range(4):
				col = []
				for i in range(4):
					col.append(self.matrix[i][j])
				col = self._update(col, dirn == 'up')
				for i in range(4):
					if self.matrix[i][j] != col[i]:
						flag = 1
						self.matrix[i][j] = col[i]                
		elif dirn == 'left' or dirn == 'right':
			for i in range(4):
				row = []
				for j in range(4):
					row.append(self.matrix[i][j])
				row = self._update(row, dirn == 'left')
				for j in range(4):
					if self.matrix[i][j] != row[j]:
						flag = 1
						self.matrix[i][j] = row[j]
		# print 'updated matrix', self.matrix
		return flag

	def _update(self, rowCol, dirn = True):
		if not dirn:
			rowCol.reverse()
		
		raw = []
		while rowCol:
			tmp = rowCol.pop(0)
			if tmp == 0:
				continue
			raw.append(tmp)

		new = [0] * 4
		j = 0
		while raw:
			tmp = raw.pop(0)
			if not raw or tmp != raw[0]:
				new[j] = tmp
			else:
				raw.pop(0)
				new[j] = tmp * 2
			j += 1

		if not dirn:
			new.reverse()

		return new

	def insert(self):
		tmp = []
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == 0:
					tmp.append((i, j))
		choice = random.choice(tmp)
		i, j = choice
		
		self.matrix[i][j] = 2
		self.matrix[i][j] = random.choice([2, 4])

	def gameOver(self):
		# check if matrix is empty
		for i in range(4):
			for j in range(4):
				if self.matrix[i][j] == 0:
					return False
		# check if there exists identical adjacent numbers
		for i in range(3):
			for j in range(4):
				if self.matrix[i][j] == self.matrix[i + 1][j]:
					return False
		for j in range(3):
			for i in range(4):
				if self.matrix[i][j] == self.matrix[i][j + 1]:
					return False
		return True

	def getChar(self, event):
		if not self.isOver:
			key = repr(event.char)
			if not self.gameOver():
				dirn = self.dirnMap[key]
				flag = self.move(dirn)
				if flag:
					self.insert()
				self.canvasDraw()
			else:
				self.isOver = True
				self.tEnd = datetime.now()
				self.tDiff = self.tEnd - self.tStart
				
				filename = self.tEnd.strftime('%Y-%d-%m %H-%M-%S') + '.txt'
				
				tStart = self.tStart.strftime('%m/%d/%Y %H:%M:%S')
				tEnd = self.tEnd.strftime('%m/%d/%Y %H:%M:%S')
				tDiff = self.tDiff.seconds

				f = open(filename, 'w+')

				self.summary = []

				self.summary.append('Game started at: ' + tStart)
				self.summary.append('Game ended at: ' + tEnd)
				self.summary.append('Game lasted: ' + str(tDiff) + ' second(s)')

				f.write('\n'.join(self.summary))
				f.write('\n')
				f.write(tabulate(self.matrix, tablefmt = 'grid'))
				
				f.close()

				self.thumbnailDraw()

if __name__ == '__main__':
	game = Game()