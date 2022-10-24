print("You can't even exit()... hehehe...")

filter = '0123456789'
while True:
    print('>', end=' ')
    inp = input()
    if any([True for l in inp if l in filter]):
        print('no')
        continue
    try:
        print(eval(inp, {'__builtins__': {}}))
    except Exception as e:
        print(e)
