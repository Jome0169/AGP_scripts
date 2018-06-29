from sys import argv

def ReadInAGPFile(arg1):
    """TODO: Docstring for ReadInAGPFile.

    :arg1: TODO
    :returns: TODO

    """
    
    AgpRawStorage = []
    RefinedDict = {}
    with open(arg1, 'r') as f:
        for line in f:
            if line.startswith("#"):
                pass
            else:
                CleanLine = line.strip().split()
                AgpRawStorage.append(CleanLine)
    for CleanLine in AgpRawStorage:
        if CleanLine[4] == 'U':
            pass
        elif CleanLine[5] not in RefinedDict:
            X = [CleanLine[0], CleanLine[5], CleanLine[1], CleanLine[2],CleanLine[8]]
            print('\t'.join(X))
        elif CleanLine[5] in RefinedDict:
            X = [CleanLine[0],CleanLine[5], CleanLine[1], CleanLine[2],CleanLine[8]]
            print('\t'.join(X))
    return RefinedDict





ReadInAGPFile(argv[1])



