from random import *

#asks user for the board in correct form and returns a string
def user_board():
    bad_digits = True
    while (bad_digits):
        board = input("Enter a 3 digit number, ie 111.")
        if ((int(board[0]) < 6 and int(board[0]) >= 0) and(int(board[1]) < 6 and int(board[1]) >= 0)
            and (int(board[2]) < 6 and int(board[2]) >= 0)):
            bad_digits = False
    return board

#asks user for valid move and column
def move(board,turn,c,r):

    if (turn == 1):
        prefix = 'A'
        suffix = 'B'
    else:
        prefix = 'B'
        suffix = 'A'
    good_col = False
    good_rem = False
    while ((good_col == False) or (good_rem == False)):
        if (c == -1):
            col = int(input("col:"))
            rem = int(input("rem:"))
        else:
            col = c
            rem = r
        if (col >= 0 and col <= 2):
            good_col = True
        else:
            good_col = False
        if (good_col == True):
            if (int(board[col]) - rem > -1):
                good_rem = True
    move = int(board[col]) - rem
    if (col == 0):
        new = str(move) + board[1:]
    elif (col == 1):
        new = board[:1] + str(move) + board[2:]
    else:
        new = board[:2] + str(move)
    print ("RETUNRING INVALAC",prefix + new)
    return prefix + board + str(col) + str(rem), suffix + new, str(col), str(rem)

#calculates all reachable s' from state s and returns a list of them
def all_moves(s):
    states = []
    index = 0
    action = ''
    actions = []
    maxval = 0
    for x in s:
        counter = int(s[index])
        while (counter != 0):
            move = int(x) - counter
            if (index == 0):
                new = str(move)+ s[1:]
                states.append(new)
            elif (index == 1):
                new = s[:1]+str(move)+s[2:]
                states.append(new)
            else:
                new = s[:2]+str(move)
                states.append(new)


            #action = str(index) + str(x)
            #actions.append(action)
            counter -= 1
        index += 1
    #count2 = 0
    #print (max)
    for x in s:
        maxval = max(int(x), maxval)
    index2 = 0
    for x in s:
        newmax = maxval
        while (newmax != 0):
            if (int(x) - newmax >= 0):
                action = str(index2) + str(newmax)
                actions.append(action)
            newmax -=1
        index2 += 1
    #myset = set(actions)
    #actions = list(myset)
    return states, actions



def main():
    n = int(input("how many games to simulate?"))
    turn = int(input("do you want to go first or second (1or2)"))
    string_board = user_board()
    #board,nextmove,col,rem = move(string_board,turn,-1,-1)
    #print(board, nextmove)

    #map = {}
    #map[board] = nextmove
    #print ("mapping state to next move",map)
    counter = 0
    states,actions = all_moves(string_board)
    print ("all states from ", string_board, states)
    print ("all actions from ", string_board, actions)
    q = {}
    nextmoves = {}


    for x in actions:
        key = 'A'+string_board+x
        q[key] = 0


        c = int(x[0])
        r = int(x[1])

    print ('ogq', q)
    for a in range(0,n):
        s = 'A'+string_board
        for x in actions:

            print ("XXXXXXXXXXXXXX",x)
            while (s != 'B000' and s != 'A000'):

                copystate = s[1:]
                print("stringboardcscscscs", copystate)
                print("actions", actions)
                print()
                print("copys",copystate)
                s1,a1 = all_moves(copystate)
                print("all states from ", turn,copystate ,s1)
                print("all actions from ", turn,copystate,a1)



                index = randint(0,len(a1)-1)

                random = a1[index]
                c = random[0]
                r = random[1]

                board, nextmove,c1,c2 = move(copystate,turn,int(c),int(r))
                #nextmoves[board] = nextmove
                #print ("mapping next moves",nextmoves)
                sprime = nextmove[1:]
                #print ("______________",board)
                #print("______________", sprime)

                for z in s1:
                    #print("thistest",nextmove+z)
                    future_s, future_a = all_moves(z)
                    #print()
                    #print()
                    #print('fa',future_a)
                    for action in future_a:
                        if (turn == 1):
                            if 'B'+z+action not in q:
                                q['B'+z+action] = 0
                                print ("adding", "B"+z+action , " to Q")
                        else:
                            if "A"+action+z not in q:
                                q['A'+z+action] = 0
                                print("adding", "A" + z + action, " to Q")


                print("2ndq",q)
                if (nextmove == "B000"):
                    reward = -1000
                elif (nextmove == 'A000'):
                    reward = 1000
                else:
                    reward = 0
                if (turn == 1):
                    #player a update
                    min_index = min(q, key=q.get)
                    minimum = q[min_index]
                    add_right = 1 * (reward + .9 * (minimum - q['A' + copystate + x]))
                    print ("key", q['A' + copystate + x])
                    print('____','A'+copystate+x)
                    q['A' + copystate + x] = q['A' + copystate + x] + add_right
                else:
                    #player b update
                    maximum_index = max(q, key=q.get)
                    maximum = q[maximum_index]
                    add_right = 1*(reward + .9*(maximum-q['B'+copystate+x]))
                    print("key2", q['B' + copystate + x])
                    q['B'+copystate+x] = q['B'+copystate+x] + add_right
                # Q[s,a]←Q[s,a]+α[r+γmina′Q[s′,a′]−Q[s,a]]
                # Q[s,a]←Q[s,a]+α[r+γmaxa′Q[s′,a′]−Q[s,a]]
                string_board = sprime
                s = nextmove
                turn *= -1

    print ("final qtable:" ,q)

main()