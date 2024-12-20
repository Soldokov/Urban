count = dict()
for item in range(int(input())):
    for word in input().split():
        count[word] = count.get(word, 0) + 1


for item in count.items():
    if item == max(count.values()):
        print(item)
