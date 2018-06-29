import getopt
import sys
import os
import re
import copy
from sys import argv
from datetime import datetime
import argparse

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
    for item in AgpRawStorage:
        if item[4] == 'U':
            pass
        elif item[5] not in RefinedDict:
            RefinedDict[item[5]] = [item]
        elif item[5] in RefinedDict:
            RefinedDict[item[5]].append(item)
    return RefinedDict



def ReadInGffFile(FileToRead):
    """Reads in a basic stap seperated Gff3 file with the key being the
    scaffold.

    :FileToRead: TODO
    :returns: TODO

    """
    ListOfSites = [] 
    with open(FileToRead, 'r') as f:
        SmallNestedList = []
        BasicName = ""
        for line in f:
            if line.startswith("#"):
                pass
            else:
                cleanline = line.strip().split()
                GeneName = cleanline[8] 
                SplitName = GeneName.split('=')
                SplitGeneName = SplitName[1]

                if len(SmallNestedList) == 0 and len(BasicName) == 0:
                    SmallNestedList.append(cleanline)
                    BasicName = SplitGeneName
                elif len(SmallNestedList) != 0 and SplitGeneName in BasicName:
                    SmallNestedList.append(cleanline)
                elif len(SmallNestedList) != 0 and SplitGeneName not in BasicName:
                    ListOfSites.append(SmallNestedList)
                    SmallNestedList = [cleanline]
                    BasicName = SplitGeneName   
    return ListOfSites 

def CreateGffDict(NestedList):
    """TODO: Docstring for CreateGffDict.

    :NestedList: 
    ['SpoScf_01999', 'maker', 'mRNA', '90359', '90730', '.', '-', '.','ID=Spo00003'], 
    ['SpoScf_01999', 'maker', 'exon', '90359', '90730', '.', '-','.', 'Parent=Spo00003'], 
    ['SpoScf_01999', 'maker', 'CDS', '90359', '90730','.', '-', '0', 'Parent=Spo00003']]
    :returns: TODO

    """
    Gff3ScafDict = {}

    for genelist in NestedList:
        Firstitem = genelist[0][0]
        if Firstitem not in Gff3ScafDict:
            Gff3ScafDict[Firstitem] = [genelist]
        elif Firstitem in Gff3ScafDict:
            Gff3ScafDict[Firstitem].append(genelist)
    return Gff3ScafDict



def PairGenesWithAgpScafs(Gff3Dict,AGPLoadedFile):
    """Pairs the Gff3 files with their correlation AGP files
        One of the biggest things to take note also is gene orientation of
        files. Remember that if the scaffold being inserted into the genome is
        now on the negative strande you must flip the orientation of everything 

    :Gff3Dict: TODO
    :AGPLoadedFile: TODO
    :returns: TODO
    [['PGA_scaffold0__1734_contigs__length_157329876', 'maker', 'mRNA', 3931950, 3933184, '.', '+', '.', 'ID=Spo11747'],
    ['PGA_scaffold0__1734_contigs__length_157329876', 'maker', 'exon', 3931950, 3933184, '.', '+', '.', 'Parent=Spo11747'],
    ['PGA_scaffold0__1734_contigs__length_157329876', 'maker', 'CDS', 3931950, 3933184, '.', '+', '0', 'Parent=Spo11747']]

    """
    FinalGffList = []
    for key, val in AGPLoadedFile.items():
        if key in Gff3Dict:
            TakeDirection = val[0][-1]
            TakePGSScafStart = int(val[0][1])
            TakePGSScafEnd = int(val[0][2]) +1
            TakePGSName = val[0][0]
            for Geneloc in Gff3Dict[key]:
                Reformateedgene = []
                for item in Geneloc:
                    #Below if the important processing step of reading thaadp
                    #File. Note that the negative flips the sign 
                    
                    if TakeDirection == '-':
                        copyitem = item
                        copyitem[0] = TakePGSName
                        TakeDifferenceInScafPos = int(val[0][7])
                        RelativeSt = TakeDifferenceInScafPos - \
                        int(copyitem[3])  
                        RelativeEnd = TakeDifferenceInScafPos - \
                        int(copyitem[4]) 

                        CorrectStart = RelativeEnd + TakePGSScafStart 
                        CorrectEnd = RelativeSt + TakePGSScafStart


                        copyitem[3] = CorrectStart
                        copyitem[4] = CorrectEnd
                        
                        #If the Scaffold is in the nefative direction 
                        #flip the signs
                        if copyitem[6] == '-':
                            copyitem[6] = '+'
                        elif copyitem[6] == '+':
                            copyitem[6] = '-'
                        
                        #Add the reformatted list to the gff3 
                        #Reformateedgene.append(copyitem)
                    elif TakeDirection == '+':
                        TakeDifferenceInScafPos = int(val[0][7])
                        DiffToAdd = (TakePGSScafEnd - TakeDifferenceInScafPos )

                        copyitem = item
                        copyitem[0] = TakePGSName
                        copyitem[3] =  int(copyitem[3])  
                        copyitem[4] = int(copyitem[4])
                        copyitem[3] += DiffToAdd 
                        copyitem[4] += DiffToAdd 

                        #Lets not add these, because they seem correct. 
                        #So, we will add them back later

                        #Add the reformatted list to the gff3 
                        Reformateedgene.append(copyitem)
                    else:

                        #You should assume that hte ? is alwsays on the
                        #posotive strand
                        TakeDifferenceInScafPos = int(val[0][7])
                        DiffToAdd = TakePGSScafEnd - TakeDifferenceInScafPos
                        copyitem = item
                        copyitem[0] = TakePGSName
                        copyitem[3] =  int(copyitem[3]) + 1
                        copyitem[4] = int(copyitem[4])
                        copyitem[3] += DiffToAdd 
                        copyitem[4] += DiffToAdd 


                        #Add the reformatted list to the gff3 
                        Reformateedgene.append(copyitem)
                FinalGffList.append(Reformateedgene)
    return FinalGffList 

def WriteGffFileOutput(NestedGffList,Output):
    """TODO: Docstring for WriteGffFileOutput.

    :NestedGffList: TODO
    :returns: TODO

    """
    try:
        os.remove(Output)
    except OSError:
        pass

    with open(Output, 'a') as r:
        for item in NestedGffList:
            for geneline in item:
                X = [str(i)for i in geneline]
                r.write('\t'.join(X))
                r.write('\n')



def get_parser():
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-f1','--file1', help='AGP file that indicates file \
            annotation to carry over', required=True, dest='f1')
    parser.add_argument('-gff','--gff1', help='Gff file to read in and adapt \
            based off of the AGP file', required=True,dest='gff')
    parser.add_argument('-o','--output', help='File to Write output to. Will \
            Remove file if finds a conflicting name', required=True, dest='o')

    args = vars(parser.parse_args())    
    return parser




if __name__ == "__main__":
    StartTime = datetime.now()
    args = get_parser().parse_args()

    AGPFileData = ReadInAGPFile(args.f1)
    GFFFileData = ReadInGffFile(args.gff)

    GffDict = CreateGffDict(GFFFileData)
    UpdatedGffLoc = PairGenesWithAgpScafs(GffDict,AGPFileData)
    WriteGffFileOutput(UpdatedGffLoc, args.o)



#Speed Things
EndTime = datetime.now()
FinalTime = EndTime - StartTime

print ("Total Time %s" % (FinalTime))

