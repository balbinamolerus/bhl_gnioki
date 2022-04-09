path = "testalert.txt"
with open(path) as file:
    lines = file.readlines()
    for line in lines:
        idx = line.index(';')
        event = line[:idx]
        time = line[idx+1:]
        print(event,' - ', time)