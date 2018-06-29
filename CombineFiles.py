from sys import argv

def ReadInFile1(File1):
    """TODO: Docstring for ReadInFile.

    :File1: TODO
    :returns: TODO

    """
    DictThing = {}
    with open(File1, 'r') as f:
        for line in f:
            Clean = line.strip().split()
            if Clean[0] not in DictThing:
                DictThing[Clean[0]] = [Clean]
            else:
                DictThing[Clean[0]].append(Clean)

    return DictThing

def ReadinFile2(File2,otherdict):
    """TODO: Docstring for ReadinFile2.

    :File2: TODO
    :returns: TODO

    """
    with open(File2, 'r') as f:
        for line in f:
            Clean = line.strip().split()
            if Clean[1] not in otherdict:
                otherdict[Clean[1]] = [Clean]
            else:
                otherdict[Clean[1]].append(Clean)
    return otherdict

FileName1 = ReadInFile1(argv[1])
EditedDict = ReadinFile2(argv[2], FileName1)

for key,value in EditedDict.items():
    if len(value) >= 2:
        if value[0][-1] == value[1][-1]:
            CombVal = value[1] + value[0] + ["MATCH"]
            print('\t'.join(CombVal))

        elif value[0][-1] != value[1][-1] and value[1][-1] == '?' and \
        value[0][-1] =='+':
                CombVal = value[1] + value[0] + ["MATCH"]
                print('\t'.join(CombVal))
        
        elif value[0][-1] != value[1][-1] and value[1][-1] == '?' and \
        value[0][-1] =='-':
            CombVal = value[1] + value[0] + ["DOES NOT MATCH"]
            print('\t'.join(CombVal))
    else:
        results = [str(i) for i in value[0]]
        print('\t'.join(results))
