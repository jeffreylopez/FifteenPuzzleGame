import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
from random import *
import numpy as np

CELL_COUNT = 4
CELL_SIZE = 75
GRID_ORIGINX = 100
GRID_ORIGINY = 100
W_WIDTH = 500
W_HEIGHT = 500
numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']
numbers_checker = [['1','2','3','4'],['5','6','7','8'],['9','10','11','12'],['13','14','15',' ']]
numbers2 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' ']


class Game(QWidget):



  def __init__(self):
    super().__init__()
    self.setGeometry(50, 50, 500, 500)
    self.setWindowTitle('Game')
    self.inversions = 0
    self.legal_move_generator()
    print(f'Inverions: {self.inversions}')
    self.board = np.array(self.final_list).reshape(4,4)
    self.__counter2 = 0
    self.final_list = []
    self.__counter = 'Moves: 0'
    self.count = False
    self.game_won = False
    button = QPushButton('Reset', self)
    button.clicked.connect(self.legal_move_generator)
    button.resize(70,50)
    button.move(30,30)
    button2 = QPushButton('Close', self)
    button2.clicked.connect(self.closeprogram)
    button2.resize(50,50)
    button.move(200,30)
    self.show()

  # Close program
  def closeprogram(self):
      sys.exit()
  # swaps the tiles
  def swapper(self, row1, col1, row2, col2):
    a = self.board[row1, col1]
    b = self.board[row2, col2]
    self.board[row1][col1] = b
    self.board[row2][col2] = a
    self.count = True

  # Creates solavable boards
  def legal_move_generator(self):
    x = 0
    b = 0
    self.inversions = 0
    self.final_list = []
    shuffle(numbers)
    while len(self.final_list) < 16:
        y = choice(numbers)
        if y not in self.final_list:
            self.final_list.append(y)
    self.final_list = [int(i) for i in self.final_list]
    while x < 16:
        comparing_number = self.final_list[x]
        counter = 0
        b += x
        while b < 16:
            if 0 < self.final_list[b] < comparing_number:
                counter += 1
            b += 1
        x += 1
        b = 0
        self.inversions += counter
    self.final_list = [str(i) for i in self.final_list]
    self.zero_location = self.final_list.index('0')
    print(f'Inversions: {self.inversions}')
    self.board = self.final_list
    self.board = np.array(self.board).reshape(4,4)
    self.update()
    if self.inversions % 2 == 0 and (4 <= self.zero_location <= 7 or 12 <= self.zero_location <= 15):
        pass
    elif self.inversions % 2 == 1 and (0 <= self.zero_location <= 3 or 8 <= self.zero_location <= 11):
        pass
    else:
        print('illegal board')
        self.legal_move_generator()
        self.update()


  # checks when the board is complete
  def game_checker(self):
      self.board = np.array(self.board).reshape(-1)
      if np.array_equal(self.board,numbers2):
          self.game_won = True
      else:
          self.board = np.array(self.board).reshape(4,4)


  # Swaps tiles
  def tile_swapper(self, row, col):
      # up 3
      if row >= 3:
          if self.board[row - 3][col] == ' ':
              self.swapper(row - 2, col, row - 3, col)
              self.swapper(row - 2, col, row - 1, col)
              self.swapper(row, col, row - 1, col)
      # up 2
      if row >= 2:
          if self.board[row - 2][col] == ' ':
              self.swapper(row - 1, col, row - 2, col)
              self.swapper(row, col, row - 1, col)
      # up
      if row > 0:
          if self.board[row - 1][col] == ' ':
              self.swapper(row, col, row - 1, col)
      # down 3
      if row < len(self.board[0]) - 3:
          if self.board[row + 3][col] == ' ':
              self.swapper(row + 2, col, row + 3, col)
              self.swapper(row + 2, col, row + 1, col)
              self.swapper(row, col, row + 1, col)
      # down 2
      if row < len(self.board[0]) - 2:
          if self.board[row + 2][col] == ' ':
              self.swapper(row + 1, col, row + 2, col)
              self.swapper(row, col, row + 1, col)
      # down
      if row < len(self.board[0]) - 1:
          if self.board[row + 1][col] == ' ':
              self.swapper(row, col, row + 1, col)
      # right 3
      if col >= 3:
          if self.board[row][col - 3] == ' ':
              self.swapper(row, col - 2, row, col - 3)
              self.swapper(row, col - 2, row, col - 1)
              self.swapper(row, col, row, col -1)
      # right 2
      if col >= 2:
          if self.board[row][col - 2] == ' ':
              self.swapper(row, col - 1, row, col - 2)
              self.swapper(row, col, row, col - 1)
      # right
      if col > 0:
          if self.board[row][col - 1] == ' ':
              self.swapper(row, col, row, col - 1)
      # left 3
      if col < len(self.board) - 3:
          if self.board[row][col + 3] == ' ':
              self.swapper(row, col + 2, row, col + 3)
              self.swapper(row, col + 2, row, col + 1)
              self.swapper(row, col, row, col + 1)
      # left 2
      if col < len(self.board) - 2:
          if self.board[row][col + 2] == ' ':
              self.swapper(row, col + 1, row, col + 2)
              self.swapper(row, col, row, col + 1)
      # left
      if col < len(self.board) - 1:
          if self.board[row][col + 1] == ' ':
              self.swapper(row, col, row, col + 1)


  # draws the stuff
  def paintEvent(self, event):
    qp = QPainter()
    qp.begin(self)
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            qp.drawRect(GRID_ORIGINX + CELL_SIZE*col, GRID_ORIGINY + CELL_SIZE*row, \
            CELL_SIZE, CELL_SIZE)
            if self.board[row][col] == '0':
                self.board[row][col] = ' '
            qp.drawText((GRID_ORIGINX + CELL_SIZE*col) + 30, (GRID_ORIGINY + CELL_SIZE*row) + 50, \
            self.board[row][col])
            qp.drawText(20, 400, self.__counter)

    qp.end()



  def mousePressEvent(self, event):
      self.__x = event.x()
      self.__y = event.y()
      row = (self.__y - GRID_ORIGINY) // CELL_SIZE
      col = (self.__x - GRID_ORIGINX) // CELL_SIZE
      if self.game_won == True:
          print('You won already buddy!')
      if self.game_won == False:
          if 400 > self.__x > 100:
              if 400 > self.__y > 100:
                 if self.board[row][col].isalnum():
                     self.tile_swapper(row, col)
                     if self.count == True:
                        self.__counter2 += 1
                        self.__counter = f'Moves: {self.__counter2}'
                        self.count = False
                        self.game_checker()
      self.update()




if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = Game()
  sys.exit(app.exec_())
