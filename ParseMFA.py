from sys import argv
from operator import itemgetter


def ReadInLASTFile(FileName):
    """Read in last file to print out the best alignment for each gene and
    print the STARTsite,ENDSite, and Strand as compared to the thing you
    BlASTED to.

    :FileName: Maf file from last with format
    a score=27 EG2=4.7e+04 E=2.6e-05
    s humanMito 2170 145 + 16571 AGTAGGCCTAAAAGCAGCCACCAATTAAGAAAGCGTT...
    s fuguMito  1648 142 + 16447 AGTAGGCTTAGAAGCAGCCACCA--CAAGAAAGCGTT...
    
    
    :returns: the above in a formatted list with each align being an entry
    [['a', 'score=290424', 'mismap=1e-10'], ['s',
    'PGA_scaffold1__1360_contigs__length_129104686', '56293792', '48424', '+',
    '129104586',]].....

    """
    FinalGroups = []
    with open(FileName, 'r') as f:
        SmalllList = []
        for line in f:
            if line.startswith('#'):
                pass
            else:
                CleanLine = line.strip().split()
                if len(CleanLine) != 0 :
                    SmalllList.append(CleanLine)
                else:
                    FinalGroups.append(SmalllList)
                    SmalllList = []

    return FinalGroups



def SortListofLAST(ListofLast):
    """Takes in the list of last files and creates a dictionary object based on
    the query names as the key and the lsit as val

    :ListofLast: FOr 
    formatted list with each align being an entry
    [['a', 'score=290424', 'mismap=1e-10'], ['s',
    'PGA_scaffold1__1360_contigs__length_129104686', '56293792', '48424', '+',
    '129104586',]].....

    :returns: Dict object
    SpoScf_01999 : [['a', 'score=290424', 'mismap=1e-10'], ['s',
    'PGA_scaffold1__1360_contigs__length_129104686', '56293792', '48424', '+',
    '129104586',]].....[[[]]]

p

    """
    SortedDict = {}

    for item in ListofLast:
        scaffoldname = item[2][1]
        if scaffoldname not in SortedDict:
            SortedDict[scaffoldname] = [item[1:3]]
        elif scaffoldname in SortedDict:
            SortedDict[scaffoldname].append(item[1:3])

    return SortedDict


def FilterScafDict(ScafDict):
    """Fitlers down all scaffold hits to find the longest hit to the DB. Will
    finally print STARTsite,ENDSite, and Strand as compared to the thing you
    BlASTED to.

    :ScafDict:Dict object
    SpoScf_01999 : [['a', 'score=290424', 'mismap=1e-10'], ['s',
    'PGA_scaffold1__1360_contigs__length_129104686', '56293792', '48424', '+',
    '129104586',]].....[[[]]]

    :returns: prints values out

    """

    def CheckScafOrder(NestedListBoi, StrandInfo):
        """The purpose of this nested function is to check if the size of the
        previous scaffold is less than the current. Returns True if this is the
        case, and false if this fails

        :arg1: [[0, 82558], [82568, 14200], [96783, 4436], [101349, 11648],
        [113468, 12600], [126901, 6375], [136697, 30162]]
        :returns: Boolean value TRUE of FALSE
        """
        NoOverlap = True
        
        
        
        CurrentLen = 0
        if StrandInfo == '+':
            for item in NestedListBoi:
                AddItems = item[0] + item[1] 
                if AddItems > CurrentLen:
                     CurrentLen = AddItems
                else:
                    print("WE ARE FUCKEDDDDDD")
                    NoOverlap = False

        elif StrandInfo == '-':
            #Flip list for negative
            NestedListBoi = NestedListBoi[::-1]
            for item in NestedListBoi:
                AddItems = item[0] + item[1] 
                if AddItems > CurrentLen:
                     CurrentLen = AddItems
                else:
                    print("WE ARE FUCKEDDDDDD")
                    break
                    sys.exit(2)
                    NoOverlap = False
        return NoOverlap


    for key, value in ScafDict.items():
        StartPGASeq = int(value[0][0][2])
        EndPGaSeq = int(value[-1][0][2])
       
        TotalScaflen = int(value[0][1][5])
        LastLastScafLentoadd = int(value[-1][1][3])
        NegLastScafToAdd = int(value[0][1][3])


        TakeAllScafStartsAndLens = []

        for thing in value:
            StartAndLen = [int(thing[1][2]), int(thing[1][3])]
            TakeAllScafStartsAndLens.append(StartAndLen)
        
        #Check if there is any overlap with scaf hitting different PGA scaf
        TakeStrand = value[0][1][4]
        Overlap = CheckScafOrder(TakeAllScafStartsAndLens, TakeStrand)
    

        #Print List out with correct orientation
        if TakeStrand == '-':
            FinalPGSLoc = (EndPGaSeq)
            NegScafEnd = StartPGASeq + NegLastScafToAdd
            FinalListToPrint = [key,str(EndPGaSeq), str(NegScafEnd), str(TakeStrand)]
            print('\t'.join(FinalListToPrint))

        elif TakeStrand == '+':
            FinalPGSLoc = (EndPGaSeq + LastLastScafLentoadd)
            FinalListToPrint = [key,str(StartPGASeq), str(FinalPGSLoc), str(TakeStrand)]
            print('\t'.join(FinalListToPrint))

        #print("FINAL")
        #print(key)
        #print(CurrentVal)
        #print(FinalItem[2][0:5])
        #input()

MAFFileList = ReadInLASTFile(argv[1])
DictOfScafs =SortListofLAST(MAFFileList)
FilteredScafs = FilterScafDict(DictOfScafs)

