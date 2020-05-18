import random
import difflib

DNALettersDict = {0: "A", 1: "T", 2: "C", 3: "G"}

#===============================================================================================
#Generate DNA sequence for the test
#===============================================================================================
OriginalDNALength = 1000

OriginalDNASeq = [DNALettersDict[random.randint(0, 3)] for i in range(OriginalDNALength)]

#print(OriginalDNASeq)

#===============================================================================================
#Generate Fragments
#===============================================================================================
NumberOfFragments = 100
MinLength = 50
MaxLength = 400

def SelFragment(DNASeq):
  startPos = random.randint(0, OriginalDNALength-1-MinLength)
  length = random.randint(MinLength, MaxLength)
  return DNASeq[startPos:startPos+length]

def ToString(input):
    str1 = ""
    return(str1.join(input))

def ReconstructFragment(FragmentsRemaining):
    Match = difflib.get_close_matches(FragmentsRemaining[0],FragmentsRemaining[1:len(FragmentsRemaining)-1],n=2)
    print('found 2 matching indexes')
    index1 = FragmentsRemaining.index(Match[0])
    index2 = FragmentsRemaining.index(Match[1])
    print(index1, 'and', index2)
    new_s = sorted(Match, key=lambda x:Match[0].index(x[0]))
    a = new_s[0]
    b = new_s[-1]
    New_fragment = a[:a.index(b[0])]+b
    del FragmentsRemaining[index1]
    del FragmentsRemaining[index2]
    FragmentsRemaining.insert(0,New_fragment)
    

ListOfFragments = [ SelFragment(OriginalDNASeq) for i in range(NumberOfFragments)]

#convert to list of strings
for i in range(len(ListOfFragments)):
    ListOfFragments[i] = ToString(ListOfFragments[i])

while(len(ListOfFragments)>1):
    ReconstructFragment(ListOfFragments)

print(ListOfFragments[0],OriginalDNASeq)
        



