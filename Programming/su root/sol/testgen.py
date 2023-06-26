import random

def generate_sudoku(mask_rate):
    base  = 3
    side  = base*base
    nums  = list(range(1, side + 1))
    board = [[None]*side for _ in range(side)]

    def pattern(r, c):
        return (base*(r%base)+r//base+c)%side

    def shuffle(s):
        return random.sample(s, len(s)) 

    r_base = range(base) 
    rows  = [ g*base + r for g in shuffle(r_base) for r in shuffle(r_base) ] 
    cols  = [ g*base + c for g in shuffle(r_base) for c in shuffle(r_base) ]
    nums  = shuffle(nums)

    for r in range(side):
        for c in range(side):
            board[r][c] = nums[pattern(r, c)]
    
    mask = [[False]*side for _ in range(side)]

    cells = side*side
    no_to_mask = int(mask_rate*cells)

    for _ in range(no_to_mask):
        r, c = random.randrange(side), random.randrange(side)
        while mask[r][c]:
            r, c = random.randrange(side), random.randrange(side)
        mask[r][c] = True
        board[r][c] = 0

    return board

t = 100
for tn in range(t):
    sudoku = generate_sudoku(mask_rate=0.7)
    f = open(f"../in/{tn}.in", "w")
    cnt = 0
    for row in sudoku:
        f.write(' '.join(map(str, row)))
        if (cnt != 8):
            f.write('\n')
        cnt = cnt + 1
    f.close()    