import sys
max_step = 30
board_size = 20
name = 'example'

with open('words.txt') as f:
    dic = [line[:-1] for line in f.readlines()[1:]]

class Game:

    def __init__(self, board, notes):
        self.board = [list(line) for line in board]
        self.notes = set([notes for word in notes if word in dic])
        self.step = 0

    def valid(self, word):
        if word not in dic:
            return False
        for note in self.notes:
            if note.startswith(word):
                return False
            if note.endswith(word):
                return False
        return True

    def commit(self, action):
        moves, notes = action
        direction = ["", -1]
        notes = [note for note in notes if self.valid(note)] + [note[::-1] for note in notes if self.valid(note)]
        real_notes = set()
        new_locs = set()
        # check if valid
        for move in moves:
            x, y, c = move
            if self.board[x][y] != '-':
                return -1
        if len(moves) > 1:
            moves = sorted(moves)
            # check if single line and continue
            x0, y0, _ = moves[0]
            x1, y1, _ = moves[1]
            xmax = -1
            ymax = -1
            xmin = board_size
            ymin = board_size
            if x0 == x1 and y0 == y1:
                return -1
            if x0 == x1:
                direction[0] = 'row'
                to_fill = []
                for move in moves:
                    x, y, _ = move
                    ymax = ymax if ymax > y else y
                    ymin = ymin if ymin < y else y
                    to_fill.append(y)
                    if x != x0:
                        return -1
                for i in range(ymin, ymax+1):
                    if i in to_fill:
                        continue
                    if self.board[x0][i] == '-':
                        return -1
            elif y0 == y1:
                direction[0] = 'col'
                to_fill = []
                for move in moves:
                    x, y, _ = move
                    xmax = xmax if xmax > x else x
                    xmin = xmin if xmin < x else x
                    to_fill.append(x)
                    if y != y0:
                        return -1
                for i in range(xmin, xmax+1):
                    if i in to_fill:
                        continue
                    if self.board[i][y0] == '-':
                        return -1
            elif (x0-y0) == (x1-y1):
                direction[0] = 'd1'
                to_fill = []
                for move in moves:
                    x, y, _ = move
                    xmax = xmax if xmax > x else x
                    xmin = xmin if xmin < x else x
                    to_fill.append(x)
                    if  (x-y) != (x0-y0):
                        return -1
                for i in range(xmin, xmax+1):
                    if i in to_fill:
                        continue
                    if self.board[i][i+y0-x0] == '-':
                        return -1
            elif (x0+y0) == (x1+y1):
                direction[0] = 'd2'
                to_fill = []
                for move in moves:
                    x, y, _ = move
                    xmax = xmax if xmax > x else x
                    xmin = xmin if xmin < x else x
                    to_fill.append(x)
                    if  (x+y) != (x0+y0):
                        return -1
                for i in range(xmin, xmax+1):
                    if i in to_fill:
                        continue
                    if self.board[i][x0+y0-i] == '-':
                        return -1
            else:
                return -1
        # commit board
        for move in moves:
            x, y, c = move
            self.board[x][y] = c

        # calc point
        for i in range(board_size):
            # exam row
            row = "".join(self.board[i])
            for word in notes:
                loc_y = row.find(word)
                if loc_y != -1:
                    real_notes.add(word)
                    for d in range(len(word)):
                        new_locs.add((i, loc_y+d))

            # exam col
            col = "".join([self.board[j][i] for j in range(board_size)])
            for word in notes:
                loc_x = col.find(word)
                if loc_x != -1:
                    real_notes.add(word)
                    for d in range(len(word)):
                        new_locs.add((loc_x+d, i))

        # exam diag
        for i in range(-board_size+1, board_size): # i = y - x
            diag = ""
            for loc_x in range(max(0, -i),min(board_size, board_size-i)):
                loc_y = loc_x + i
                diag = diag + self.board[loc_x][loc_y]
            for word in notes:
                inc = diag.find(word)
                if inc != -1:
                    real_notes.add(word)
                    for d in range(len(word)):
                        new_locs.add((max(0, -i)+inc+d, max(0, -i)+inc+i+d))

        for i in range(0, board_size + board_size - 1): # i = x + y
            diag = ""
            for loc_x in range(max(0, i-board_size+1),min(board_size, i+1)):
                loc_y = i - loc_x
                diag = diag + self.board[loc_x][loc_y]
            for word in notes:
                inc = diag.find(word)
                if inc != -1:
                    real_notes.add(word)
                    for d in range(len(word)):
                        new_locs.add((max(0, i-board_size+1)+inc+d, i-max(0, i-board_size+1)-inc-d))
        
        # last check, if failed roll back
        for move in moves:
            x, y, _ = move
            if (x, y) not in new_locs:
                # roll back
                for _move in moves:
                    xx, yy, _ = _move
                    self.board[xx][yy] = '-'
                return -1

        # commit notes
        for note in real_notes:
            if not self.valid(note):
                self.notes.add(note[::-1])
                continue
            self.notes.add(note)

        '''
        print("Update  : "+str(real_notes))
        print("History : "+str(self.notes))
        print("Board   : ")
        print("".join(["".join(line) for line in self.board])[:-1])
        print("Point   : "+str(len(new_locs) - len(moves)))
        print('\n')
        '''
        return len(new_locs) - len(moves)

def main(input_file, output_file):
    # readin input
    inputs = input_file.readlines()
    board = inputs[:20]
    notes = inputs[21:]
    game = Game(board, notes)
    actions = []
    # readin output
    try:
        outputs = output_file.readlines()
        total_step = int(outputs[0])
        assert total_step <= max_step
        cur_line = 1
        for _ in range(total_step):
            # read new move
            cur_move = []
            total_chr = int(outputs[cur_line])
            cur_line += 1
            for _ in range(total_chr):
                x, y, c = outputs[cur_line].split()
                cur_line += 1
                x = int(x)
                assert x < board_size
                y = int(y)
                assert y < board_size
                assert c.isalpha()
                assert len(c) == 1
                cur_move.append((x,y,c))
            # read new notes
            cur_notes = []
            total_notes = int(outputs[cur_line])
            cur_line += 1
            for _ in range(total_notes):
                cur_note = outputs[cur_line]
                if cur_note.endswith('\n'):
                    cur_note = cur_note[:-1]
                assert cur_note in dic
                cur_line += 1
                cur_notes.append(cur_note)
            actions.append((cur_move, cur_notes))
    except Exception:
        # print("error", str(e))
        print(-1)
        sys.exit(0)
    else:
        pass # successful read-in
    # judge moves
    points = 0
    for action in actions:
        point = game.commit(action)
        if point == -1:
            print(-1)
            sys.exit(0)
        points += point
    print(points)

with open(name+'.in') as fin, open(name+'.out') as fout:
    main(fin, fout)