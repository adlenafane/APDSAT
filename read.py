

def readCnfFile:
    cnf=[]
    cnfFile = open('output.txt', 'r')
    for line in cnfFile:
        if line[0]!="c" and line[0]!="p":
            cnf.append([cnfFile.readline()])
    cnfFile.close()
