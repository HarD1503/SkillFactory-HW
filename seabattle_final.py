import random
import copy

class AS_BusyDotException(Exception):
    def __init__(self):
        pass


class AS_OutOfBoardException(Exception):
    def __init__(self):
        pass

class Shot_BusyDotException(Exception):
    def __init__(self,text):
        print(text)

class Shot_OutOfBoardException(Exception):
    def __init__(self,text):
        print(text)


class Dot:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length,front_dot,direction):
        self.length = length
        self.front_dot = front_dot
        self.direction = direction
        self.lives = length

    def dots(self):
        list_dot = []
        x = self.front_dot.x
        y = self.front_dot.y
        for i in range(self.length):
            if self.direction == 0: # 0 - вертикальная ориентация
                list_dot.append(Dot(x + i, y))
            if self.direction == 1: # 1 - горизонтальная ориентация
                list_dot.append(Dot(x, y + i))
        return list_dot

class Board:
    def __init__(self, hid):
        self.field = [[0 for i in range(6)] for j in range(6)]
        self.busy_dots = []
        self.contour_dots = []
        self.ships = []
        self.hid = hid
        self.alive_ships = 0

    def add_ship(self, ship):
        field_t = copy.deepcopy(self.field)
        for dot in ship.dots():
            if self.out(dot):
                raise AS_OutOfBoardException
            if (field_t[dot.x][dot.y] != 0) or (dot in self.contour_dots):
                raise AS_BusyDotException
            field_t[dot.x][dot.y] = 1
        self.field = copy.deepcopy(field_t)
        self.ships.append(ship)
        self.alive_ships += 1
        self.contour(ship,0)


    def contour(self, ship, state): #state == 0 - при расстановке, state == 1 - при игре
        for dot in ship.dots():
            for x in range(dot.x - 1,dot.x + 2):
                for y in range(dot.y - 1, dot.y + 2):
                    if not self.out(Dot(x,y)):
                        if (self.field[x][y] == 0) and (state == 0):
                            self.field[x][y] = 2
                            self.contour_dots.append(Dot(x, y))
                        if (self.field[x][y] == 0 or self.field[x][y] == 2) and (state == 1):
                            self.field[x][y] = 5
                            self.contour_dots.append(Dot(x, y))

    def out(self,dot):
        if 0 <= dot.x <= 5 and 0 <= dot.y <= 5:
            return False
        else:
            return True

    def shot(self, dot):
        if self.out(dot):
            raise Shot_OutOfBoardException('Выстрел вне поля. Попробуйте ещё раз.')
        if dot in self.busy_dots:
            raise Shot_BusyDotException('Выстрел в стреляную ячейку. Попробуйте ещё раз.')

        for ship in self.ships:
            if dot in ship.dots():
                self.field[dot.x][dot.y] = 3
                self.ships.remove(ship)
                ship.lives -= 1
                self.ships.append(ship)
                self.busy_dots.append(dot)
                if ship.lives == 0:
                    self.contour(ship,1)
                    self.alive_ships -=1
                    print('Убил')
                    return True
                else:
                    print('Ранил')
                    return True
        self.field[dot.x][dot.y] = 4
        self.busy_dots.append(dot)
        print('Промах')
        return False

    def show_field(self):
        simb_field = copy.deepcopy(self.field)
        for i in range(6):
            for j in range(6):
                if self.field[i][j] == 0 or self.field[i][j] == 2:
                    simb_field[i][j] = '\u25CB' # o
                if self.field[i][j] == 1:
                    if self.hid:
                        simb_field[i][j] = '\u25A0' # квадрат
                    else:
                        simb_field[i][j] = '\u25CB'  # o
                if self.field[i][j] == 3:
                    simb_field[i][j] = 'X'
                if self.field[i][j] == 4:
                    simb_field[i][j] = 'T'
                if (self.field[i][j] == 5):
                    simb_field[i][j] = '\u2219' # точка
        if self.hid:
            print('\nПоле игрока')
        else:
            print('\nПоле компьютера')
        print(' |0|1|2|3|4|5|')
        for i in range(6):
            st = str(i) + '|'
            for j in range(6):
                st += f'{simb_field[i][j]}|'
            print(st)

class Player:
    def __init__(self,own_board,enemy_board):
        self.own_board = own_board
        self.enemy_board = enemy_board
    def ask(self):
        pass

    def move(self):
        need_attempt = True
        while need_attempt:
            try:
                dot = self.ask()
                shot_result = self.enemy_board.shot(dot)
            except ValueError:
                print("Некорректный ввод. Попробуйте ещё раз.")
                need_attempt = True
            except (Shot_OutOfBoardException,Shot_BusyDotException):
                need_attempt = True
            else:
                need_attempt = False
        return shot_result

class User(Player):
    def ask(self):
        print('\nВаш ход: ')
        x, y = map(int, input().split())
        return Dot(x, y)

class AI(Player):
    def ask(self):
        dot = Dot(random.randint(0, 5), random.randint(0, 5))
        while (dot in self.enemy_board.busy_dots) and (dot in self.enemy_board.contour_dots):
            dot = Dot(random.randint(0, 5), random.randint(0, 5))
        print('\nХод компьютера: ' + str(dot.x) + ' ' + str(dot.y))
        return dot

class Game:
    def __init__(self, user, ai, user_board, ai_board):
        self.user = user
        self.ai = ai
        self.user_board = user_board
        self.ai_board = ai_board

    def random_board(self,board:Board):
        ship_length_list = [3, 2, 2, 1, 1, 1, 1]
        i = 0
        while i <= len(ship_length_list)-1:
            j = 0
            except_flag = True
            while (j < 1000) and except_flag:
                j += 1
                try:
                    x = random.randint(0,5)
                    y = random.randint(0, 5)
                    direction = random.randint(0, 1)
                    board.add_ship(Ship(ship_length_list[i], Dot(x,y), direction))
                except(AS_BusyDotException, AS_OutOfBoardException):
                    except_flag = True
                else:
                    except_flag = False
            i += 1
            if i <= len(ship_length_list) and j > 990 and except_flag:
                i = 0
                j = 0
                hid = board.hid
                board.__init__(hid)

    def greet(self):
        print('''Игра "Морской бой".
Формат ввода: "x y", 
где x - координата по вертикали,
    y - координата по горизонтали.''')
        input('\nДля продолжения нажмите Enter\n')

    def loop(self):
        print('\nГенерируется доска игрока...')
        self.random_board(self.user_board)
        print('\nГотово.')
        print('\nГенерируется доска компьютера...')
        self.random_board(self.ai_board)
        print('\nГотово.\n')
        self.user_board.show_field()
        self.ai_board.show_field()
        print('\n--------------------\n')
        input('Для продолжения нажмите Enter\n')

        while True:

            flag = True
            while flag:
                if self.ai_board.alive_ships == 0:
                    print('Вы выиграли.')
                    input('\nДля выхода нажмите Enter')
                    exit()
                flag = self.user.move()
                self.user_board.show_field()
                self.ai_board.show_field()
                print('\n--------------------\n')
                input('Для продолжения нажмите Enter\n')

            flag = True
            while flag:
                if self.user_board.alive_ships == 0:
                    print('Вы проиграли.')
                    input('\nДля выхода нажмите Enter')
                    exit()
                flag = self.ai.move()
                self.user_board.show_field()
                self.ai_board.show_field()
                print('\n--------------------\n')
                input('Для продолжения нажмите Enter\n')

    def start(self):
        self.greet()
        self.loop()


user_board = Board(True)
ai_board = Board(False)
user = User(user_board,ai_board)
ai = AI(ai_board,user_board)

game = Game(user,ai,user_board,ai_board)
game.start()