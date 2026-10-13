memoryFilePath = "test.txt"
found = False
lineNum = 0

with open(file=memoryFilePath, mode="r") as rFile:
    lines = rFile.readlines()
    print(len(lines))
    print(lines)
    totalLines = int(len(lines))
    

    for x in range(0, totalLines):
        print(x)
        print(lines[x])
        if "ASDF" in lines[x]:
            print(f"FOUND AT {x}")
            found = True
            lineNum = x + 1
            break

            

if not found:
    
    with open(file=memoryFilePath, mode="a") as addText:
        addText.write(f"NEW LINE\n")
    with open(file=memoryFilePath, mode="r") as rFile:
        lines = rFile.readlines()
        lineNum = len(lines)
        print(f"That text was not there so the new text had been added to line {lineNum}")
                
print(lines)
print(f"attempting to change line {lineNum} to TEST..")
print(lineNum)
lines[lineNum - 1] = f"TEST..\n"
print(lines)
            
print("for loop time!")
firstEdit = False

with open(file=memoryFilePath, mode="w") as memoryFileWrite:
    for line in lines:
        memoryFileWrite.write(line)