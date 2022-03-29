with open('input.txt') as f:
    lines = f.readlines()

x1 = float(lines[0].strip().split()[1])
x2 = float(lines[1].strip().split()[1])

y1 = x1 ** 2 + x2 ** 2
y2 = x1 + x2
with open('output.txt', 'w') as f:
    f.write(f'y {y1}\ny2 {y2}')
