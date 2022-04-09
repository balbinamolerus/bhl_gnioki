path = "testalert.txt"
with open(path) as file:
    lines = file.readlines()
    for line in lines:
        idx = line.index(';')
        event = lines[:idx]
        time = lines[idx+1:]
        print(event,' - ', time)