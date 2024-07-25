import random

#--------------temp-----------------------

#--------------constants------------------

help_field = ((7,8,9),(4,5,6),(1,2,3))
initial_field = [['-','-','-'],['-','-','-'],['-','-','-']]

#--------------functions------------------

def print_field(field):
    print('  0 1 2')
    for i in range(0,3):
        str_temp = f"{i} "
        for j in range(0,3):
            str_temp += f"{field[i][j]} "
        print(str_temp)
    print('\n')

def human_step(field):
    global initial_field
    pass_flag = False
    field_temp = field

    while pass_flag == False:
        inp = input('Ваш ход: ')
        if inp in list([str(i) for i in range(1, 10)]):
            if (inp == '7') and (field_temp[0][0] == '-'):
                field_temp[0][0] = 'X'
                pass_flag = True
            elif (inp == '8') and (field_temp[0][1] == '-'):
                field_temp[0][1]='X'
                pass_flag = True
            elif (inp == '9') and (field_temp[0][2] == '-'):
                field_temp[0][2]='X'
                pass_flag = True
            elif (inp == '4') and (field_temp[1][0] == '-'):
                field_temp[1][0] = 'X'
                pass_flag = True
            elif (inp == '5') and (field_temp[1][1] == '-'):
                field_temp[1][1] = 'X'
                pass_flag = True
            elif (inp == '6') and (field_temp[1][2] == '-'):
                field_temp[1][2] = 'X'
                pass_flag = True
            elif (inp == '1') and (field_temp[2][0] == '-'):
                field_temp[2][0] = 'X'
                pass_flag = True
            elif (inp == '2') and (field_temp[2][1] == '-'):
                field_temp[2][1] = 'X'
                pass_flag = True
            elif (inp == '3') and (field_temp[2][2] == '-'):
                field_temp[2][2] = 'X'
                pass_flag = True
            else:
                print('\nПоле занято. Попробуйте еще раз.')
                pass_flag = False
        else:
            print('\nОшибка ввода. Введите число от 1 до 9.')
            pass_flag = False
    return field_temp

def pc_step(field):
    field_temp = field
    print('Ход PC: ')

    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if field_temp[x][y] == '-':
            field_temp[x][y] = 'O'
            break
    return field_temp

def check_field(field):
    result = 0

    for i in range(0,3):
        if (field[i][0] == 'X') and (field[i][1] == 'X') and (field[i][2] == 'X'):
            result = 1
        elif (field[0][i] == 'X') and (field[1][i] == 'X') and (field[2][i] == 'X'):
            result = 1
        if (field[0][0] == 'X') and (field[1][1] == 'X') and (field[2][2] == 'X'):
            result = 1
        if (field[0][2] == 'X') and (field[1][1] == 'X') and (field[2][0] == 'X'):
            result = 1

        if (field[i][0] == 'O') and (field[i][1] == 'O') and (field[i][2] == 'O'):
            result = 2
        elif (field[0][i] == 'O') and (field[1][i] == 'O') and (field[2][i] == 'O'):
            result = 2
        if (field[0][0] == 'O') and (field[1][1] == 'O') and (field[2][2] == 'O'):
            result = 2
        if (field[0][2] == 'O') and (field[1][1] == 'O') and (field[2][0] == 'O'):
            result = 2

    return result

#--------------code-----------------------

print('Крестики-нолики. Ниже приведена схема нажатия клавиш.\n')

print_field(help_field)
field=initial_field
finish_flag = 0
count = 0

while True:

    field = human_step(field)
    count += 1
    print_field(field)
    finish_flag = check_field(field)

    if finish_flag == 1:
        print('\nВы выиграли!')
        break

    if (finish_flag == 0) and (count == 9):
        print('\nНичья.')
        break

    field = pc_step(field)
    count += 1
    print_field(field)
    finish_flag = check_field(field)

    if finish_flag == 2:
        print('\nВы проиграли...')
        break

i=input('\nДля выхода нажмите Enter')
