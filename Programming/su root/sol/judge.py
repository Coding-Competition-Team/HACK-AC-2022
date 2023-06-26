import os
import time
import subprocess
from multiprocessing import Pool

flag = "ACSI{su_r0O7_S7roNG_pw_cAt_fl@6}"
ac = True

def check_sudoku(grid):
    for i in range(9):
        row = [grid[i][j] for j in range(9)]
        if sorted(row) != list(range(1, 10)):
            return False

    for i in range(9):
        column = [grid[j][i] for j in range(9)]
        if sorted(column) != list(range(1, 10)):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if sorted(square) != list(range(1, 10)):
                return False

    return True

def run_test(test_number):
    start_time = time.time()

    try:
        process = subprocess.Popen(["./sol"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        with open(f"../in/{test_number}.in", 'rb') as file:
            input_data = file.read()
        output, _ = process.communicate(input_data + b'\n', timeout=2)
    except subprocess.TimeoutExpired:
        ac = False
        return f"#{test_number}: TLE"
    except subprocess.CalledProcessError:
        ac = False
        return f"#{test_number}: CE"

    output = output.decode().strip().split('\n')
    output = [list(map(int, line.split())) for line in output]

    if check_sudoku(output):
        end_time = time.time()
        return f"#{test_number}: AC - {int((end_time - start_time) * 1000)}ms"
    else:
        ac = False
        return f"#{test_number}: WA"


def main():
    test_numbers = [i for i in range(0, 100)]
    with Pool(os.cpu_count()) as p:
        results = p.map(run_test, test_numbers)

    for result in results:
        print(result)
    
    if ac:
        print(flag)

if __name__ == "__main__":
    main()
