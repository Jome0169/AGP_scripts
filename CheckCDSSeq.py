import getopt
import sys
import os
import re
import copy
from sys import argv
from datetime import datetime
import Bio
from Bio import SeqIO, SeqFeature
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq


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


def ParseGenomeFile(FastaFile):
    """Parses large genome file using biopyton

    :FastaFile: TODO
    :returns: TODO

    """
    record_iterator = SeqIO.to_dict(SeqIO.parse(FastaFile, "fasta"))
    return record_iterator


def ExtractGenomicLocation(GffFileList, FullGenome):
    """TODO: Docstring for ExtractGenomicLocation.

    :GffFileList: TODO
    :FullGenome: TODO
    :returns: TODO

    """
    GeneNameCds = []
    for genes in GffFileList:
        CreatedSeq = ""
        for singlegene in genes:
            if singlegene[2] == "CDS" and singlegene[6] == '+':
                ScafInfo = singlegene[0]
                LocationStart = int(singlegene[3]) -1 
                Locationend = int(singlegene[4]) +1 
                X = FullGenome[ScafInfo].seq[LocationStart:Locationend]
                CreatedSeq += X
            elif singlegene[2] == "CDS" and singlegene[6] == '-':
                ScafInfo = singlegene[0]
                LocationStart = int(singlegene[3]) -1
                Locationend = int(singlegene[4]) +1 
                X = FullGenome[ScafInfo].seq[LocationStart:Locationend]
                CreatedSeq += X[::-1]


        Direction = genes[0][6]
        if Direction == '-':
            CorrectSeq = CreatedSeq[::-1].reverse_complement()
            MiniList = [genes[0],CorrectSeq, CreatedSeq]
            GeneNameCds.append(MiniList)
        else:
            MiniList = [genes[0],CreatedSeq]
            GeneNameCds.append(MiniList)
    return GeneNameCds


def FindMatchingCDS(ListOfGeneswithCDs, CDSGenesfromFile):
    """TODO: Docstring for FindMatchingCDS.

    :ListOfGeneswithCDs: TODO
    :CDSGenesfromFile: TODO
    :returns: TODO

    """
    try:
        os.remove("CorrectCDS.gff")
        os.remove("IncorrectCDS.gff")
    except OSError:
        pass

    Z = open("CorrectCDS.gff", 'a+')
    Y= open("IncorrectCDS.gff", 'a+')
    
    for geneseqname in ListOfGeneswithCDs:
        FindGeneName = geneseqname[0][8].split('=')
        GeneName = FindGeneName[1]
        if len(geneseqname) == 3:
        #Neg Strand Seq have both non Revcomp and Revcomp DNA
            if CDSGenesfromFile[GeneName].seq != geneseqname[1]:
                print("FROM CDS FILE")
                print(CDSGenesfromFile[GeneName].seq)
                print("From Assembly")
                print(geneseqname[0])
                print(geneseqname[1])
                print("Non Reverse Com")
                print(geneseqname[0])
                print(geneseqname[2])
                print('\t'.join(geneseqname[0]))
                print('\n')
                input()
                #Y.write('\t'.join(geneseqname[0]))
                #Y.write('\n')
            elif CDSGenesfromFile[GeneName].seq == geneseqname[1]:
                #Z.write('\t'.join(geneseqname[0]))
                pass
                #Z.write('\n')

        else:
            if CDSGenesfromFile[GeneName].seq != geneseqname[1]:
                print("FROM CDS FILE")
                print(CDSGenesfromFile[GeneName].seq)
                print("From Assembly")
                print(geneseqname[0])
                print(geneseqname[1])
                print('\t'.join(geneseqname[0]))
                print('\n')
                input()
                #Y.write('\t'.join(geneseqname[0]))
                #Y.write('\n')
            elif CDSGenesfromFile[GeneName].seq == geneseqname[1]:
                pass
                #Z.write('\t'.join(geneseqname[0]))
                #Z.write('\n')
    Y.close()
    Z.close()


StartTime = datetime.now()

ReadGenome = ParseGenomeFile(argv[1])
ReadCDSFile = ParseGenomeFile(argv[2])
EditedGFFFile = ReadInGffFile(argv[3])
GeneCDSWNames = ExtractGenomicLocation(EditedGFFFile,ReadGenome)
FindMatchingCDS(GeneCDSWNames,ReadCDSFile)




EndTime = datetime.now()
FinalTime = EndTime - StartTime
print ("Total Time %s" % (FinalTime))





