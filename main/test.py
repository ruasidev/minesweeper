import random
exclude = (1, 3)
height = 4
width = 4
exclude_sample = width*exclude[1] + exclude[0]
exclusions = {}
exclusions.update(exclude_sample)
board = [[0 for _ in range(width)] for _ in range(height)]
board[exclude[1]][exclude[0]] = 1
sample_range = set(range(width*height)) - exclude_sample
sample = random.sample(sample_range, 10)
print(f"Sample: {sample}")
while exclude_sample in sample:
    print(f'Exclude Sample {exclude_sample} found in sample, regenerating at sample[{sample.index(exclude_sample)}]')
    sample[sample.index(exclude_sample)] = random.sample(sample_range, 1)[0]
for value in sample:
    print(f"Value: {value}")
    x_val = value%width
    y_val = value//width
    print(f"Position: {(x_val, y_val)}")
    board[y_val][x_val] = 9

for row in board:
    print(row)

# Exclude (3, 1)
# Width = 6
# Height = 4
# Value is at Width*1 + exclude[0]
# 0 0 0 0 0 0 
# 0 0 0 * 0 0 
# 0 0 0 0 0 0 
# 0 0 0 0 0 0 

# Exclude (2, 3)
# Width = 6
# Height = 4
# Value is at Width*3 + exclude[0]
# 0 0 0 0 0 0 
# 0 0 0 0 0 0 
# 0 0 0 0 0 0 
# 0 0 * 0 0 0 