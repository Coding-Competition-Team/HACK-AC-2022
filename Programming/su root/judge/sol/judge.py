import os
import time
import subprocess
from multiprocessing import Pool

flag = "ACSI{su_r0O7_cAt_fl@6}"
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
        return f"#{test_number}: TLE"
    except subprocess.CalledProcessError:
        return f"#{test_number}: CE"

    output = output.decode().strip().split('\n')
    output = [list(map(int, line.split())) for line in output]

    if check_sudoku(output):
        end_time = time.time()
        total_time = int((end_time - start_time) * 1000)
        if total_time <= 128:
            return f"#{test_number}: AC - {total_time}ms"
        else:
            return f"#{test_number}: TLE - {total_time}ms"
    else:
        return f"#{test_number}: WA"


def main():
    test_numbers = [i for i in range(0, 200)]
    with Pool(os.cpu_count()) as p:
        results = p.map(run_test, test_numbers)

    all_AC = all("AC" in result for result in results)

    for result in results:
        print(result)

    if all_AC:
        print(flag)

if __name__ == "__main__":
    main()
