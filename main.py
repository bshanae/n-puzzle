from Algo.Move import Move
from Visual import Visual

if __name__ == '__main__':
    values = [[22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22]]

    moves = [Move((0, 0), (0, 1)),
             Move((1, 0), (1, 1)),
             Move((2, 0), (2, 1))]

    Visual.init()
    Visual.visualise(values, moves)
