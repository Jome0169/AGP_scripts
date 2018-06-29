from sys import argv


def ReadFileOfWrongScgs(CorrectScafs):
    """TODO: Docstring for ReadFileOfWrongScgs.

    :CorrectScafs: TODO
    :returns: TODO

    """
    CleanScafs = set() 
    with open(CorrectScafs, 'r') as f:
        for line in f:
            clean = line.strip()
            CleanScafs.add(clean)
    return CleanScafs


def ReadInAGPFile(arg1, CorrScaf):
    """TODO: Docstring for ReadInAGPFile.

    :arg1: TODO
    :returns: TODO

    """
    AgpRawStorage = []
    with open(arg1, 'r') as f:
        for line in f:
            if line.startswith("#"):
                pass
            else:
                CleanLine = line.strip().split()
                AgpRawStorage.append(CleanLine)

    for thing in AgpRawStorage:
        if thing[5] in CorrScaf:
            thing[-1] = '-'
            print('\t'.join(thing))
        else:
            print('\t'.join(thing))

CorrectScafs1 = ReadFileOfWrongScgs(argv[2])
AgpList = ReadInAGPFile(argv[1], CorrectScafs1)
