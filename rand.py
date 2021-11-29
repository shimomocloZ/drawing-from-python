import random

PRODUCTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

result = []

p_list = PRODUCTS

for _ in range(len(PRODUCTS)):
    randi = random.randrange(len(p_list))
    prod = p_list[randi]
    result.append(prod)
    p_list.remove(prod)

for r in result:
    print(r, end='|')

print()