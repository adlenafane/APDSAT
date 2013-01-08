

def loadCnfFile(fileName='example.cnf'):
    """ retourne une liste de listes d'entiers decrivants la forme normale conjonctive"""
    cnf=[]
    cnfFile = open(fileName, 'r')
    for line in cnfFile:
        if line[0]!="c" and line[0]!="p":
            l=line.split("0")[0].strip().split(" ")
            m=[]
            for k in l:
                m.append(int(k))
            cnf.append(m)
    cnfFile.close()
    return cnf
