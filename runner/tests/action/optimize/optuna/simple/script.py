with open('input.txt') as f:
    _, x = f.read().strip().split()
x = float(x)
y = x ** 2
with open('output.txt', 'w') as f:
    f.write(f'y {y}')
