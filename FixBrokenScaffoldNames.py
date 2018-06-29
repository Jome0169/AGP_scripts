from sys import argv
import copy
import os




def ReadInGffFile(FileToRead):
    """Reads in a basic stap seperated Gff3 file with the key being the
    scaffold.

    :FileToRead: TODO
    :returns: TODO

    """
    Gff4Dict = {}
    with open(FileToRead, 'r') as f:
        for line in f:
            cleanline = line.strip().split()
            if cleanline[0] not in Gff4Dict:
                Gff4Dict[cleanline[0]] = [cleanline]
            elif cleanline[0]  in Gff4Dict:
                Gff4Dict[cleanline[0]].append(cleanline)
    return Gff4Dict



def BreakGffDictFile(RawGff3Dict):
    """The read in Dict from ReadInGffFile must have read in list broken 
    by gene features. Will have scaffold as key, and gene featutes in a broken
    nested list format

    :RawGff3Dict: TODO
    :returns: TODO
    SpoScf_02751: [['SpoScf_02751', 'maker', 'mRNA', '39353', '40162', '.', '+',
    '.', 'ID=Spo00005'], ['SpoScf_02751', 'maker', 'exon', '39353', '40162', '.',
    '+', '.', 'Parent=Spo00005'], ['SpoScf_02751', 'maker', 'CDS', '39353',
    '40162', '.', '+', '0', 'Parent=Spo00005']]
    
    SpoScf_01719: [['SpoScf_01719', 'maker', 'mRNA', '42092', '44435', '.', '+',
    '.', 'ID=Spo00010'], ['SpoScf_01719', 'maker', 'exon', '42092', '42398', '.',
    '+', '.', 'Parent=Spo00010'], ['SpoScf_01719', 'maker', 'exon', '42984',
    '43273', '.', '+', '.', 'Parent=Spo00010'], ['SpoScf_01719', 'maker', 'exon',
    '43458', '44435', '.', '+', '.', 'Parent=Spo00010'], ['SpoScf_01719', 'maker',
    'CDS', '42092', '42398', '.', '+', '0', 'Parent=Spo00010'], ['SpoScf_01719',
    'maker', 'CDS', '42984', '43273', '.', '+', '2', 'Parent=Spo00010'],
    ['SpoScf_01719', 'maker', 'CDS', '43458', '44435', '.', '+', '0',
    'Parent=Spo00010']]

    """
    NestedGeneLevelDict = {}
    DeepCopyIter  = RawGff3Dict
    for key, value in RawGff3Dict.items():
        NestedGeneLevelDict[key] = []
        for item in value:
            if 'ID' in item[8] and len(BrokenList) ==  0:
                BrokenList = []
                BrokenList.append(item)
            elif 'ID' in item[8] and len(BrokenList) !=  0:
                NestedGeneLevelDict[key].append(BrokenList)
                BrokenList = []
                BrokenList.append(item)
            elif len(BrokenList) != 0:
                BaseGeneID1 = BrokenList[0][8].split('=')
                BaseGeneID1 = BaseGeneID1[1]
                IndGeneID = item[8].split('=')
                IndGeneID = IndGeneID[1]
                if IndGeneID in BaseGeneID1:
                    BrokenList.append(item)
                
    return NestedGeneLevelDict


def ReadInAGPReplaceFile(AgpFile):
    """Read in the AGP file with Break locations. File should look like

    :AgpFile
    SpoScf_00333_s1 1       33569   1       W       SpoScf_00333    1       33569 +
    SpoScf_00333_s2 1       484466  1       W       SpoScf_00333    34041   518506 +
    :returns: TODO

    """
    ReadInAgp = []
    CreateSplitDict = {}
    with open(AgpFile, 'r') as f:
        for line in f:
            cleanline = line.strip().split()
            ReadInAgp.append(cleanline)
    
    for item in ReadInAgp:
        if item[5] not in CreateSplitDict:
            CreateSplitDict[item[5]] = [item]
        elif item[5] in CreateSplitDict:
            CreateSplitDict[item[5]].append(item)
    return CreateSplitDict


def ReformatGff3File(Gff3Dict, Agpdict):
    """TODO: Docstring for ReformatGff3File.

    :Gff3Dict: TODO
    :AgpFileList: TODO
    :returns: TODO

    """
    ImprovedDict = {}
    
    Itercopy= copy.deepcopy(Gff3Dict)
    for key,val  in Itercopy.items():
        if key in Agpdict:
            CreatedSetRanges = []
            RetreiveList = Agpdict[key]
            for item in RetreiveList:
                SmallerRange = [item[0],item[6], item[7]]
                CreatedSetRanges.append(SmallerRange)
                ImprovedDict[item[0]] = []
            for item in CreatedSetRanges:
                Range1 = range(int(item[1]),int(item[2]))
                for gene in val:
                    genelow  = int(gene[3])
                    genehigh = int(gene[4]) 
                    if genehigh in Range1:
                        ReformatedList = gene 
                        ReformatedList[0] = item[0]
                        ImprovedDict[item[0]].append(ReformatedList)
                    else:
                        pass
        else:
            ImprovedDict[key] = val
    return ImprovedDict


def WriteGff3File(arg1):
    """TODO: Docstring for WriteGff3File.

    :arg1: TODO
    :returns: TODO

    """

    try:
        os.remove("SpinachScafSplitGff3.gff3")
    except OSError:
        pass

    with open("SpinachScafSplitGff3.gff3", 'a') as f:
        for key, val in arg1.items():
            for item in val:
                Format = '\t'.join(item)
                f.write(Format)
                f.write('\n')




ReadRawGff = ReadInGffFile(argv[1])
ReadAGPFile = ReadInAGPReplaceFile(argv[2])
FinalGffDict = ReformatGff3File(ReadRawGff,ReadAGPFile)
WriteGff3File(FinalGffDict)








