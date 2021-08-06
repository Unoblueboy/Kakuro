import json

solutions = {}
# solutions will be a dictionary with keys being tuples of the form
# (number of entries, sum of entries)

for i in range(1, 2**9):
    nums = [n+1 for n in range(0, 9) if (i & (2**n)) != 0]
    key = (len(nums), sum(nums))
    key = str(key)
    if solutions.get(key) is None:
        solutions[key] = [nums]
    else:
        solutions[key].append(nums)

# print(solutions)
print(json.dumps(solutions, indent=4))
with open("line_solutions.json", "w+") as file:
    json.dump(solutions, file, indent=4)
