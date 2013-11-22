contents = []
with open("black.txt","r") as f:
    for line in f.readlines():
        contents.append(line)
print contents
