print("Hello! Hope you are a vim fan!")

exits = ["q", "q!", "x", "wq", "wq!", "x!"]

while True:
    print(':', end='')
    inp = input()
    if inp in exits:
        print("This isn't vim sadly...")
        continue
    try:
        print(eval(f'exit({inp})'))
    except Exception as e:
        print(e)
