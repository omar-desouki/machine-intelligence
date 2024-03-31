from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file, read_word_list

DechiperResult = Tuple[str, int, int]


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:

    str=ciphered
    strlist=[]
    outputstr = ""
    length = len(str)
    dictset = set(dictionary)

    #all 26 possible combination in strlist
    for j in range(26): 
        for i in range(length):
            if str[i] == " ":
                    outputstr += " "
            else:
                outputstr += chr((ord(str[i]) - 1 - 97)%26 + 97) #wrap around from 97 to 122

        strlist.append(outputstr)
        str=outputstr 
        outputstr = ""

    #loop on the 26 poosible combination and see which one has more incorrect words and save the exact number in max count list with the same index    
    maxcount = [0 for _ in range(26)]

    for j in range(26):
        strwordss = strlist[j].split()
        for i in range(len(strwordss)):  
            if strwordss[i] not in dictset:
                maxcount[j] += 1
            

    #3shan ageb el index bta3 as8r rakm fe maxcount list
    index = maxcount.index(min(maxcount))
    

    outputtuple = (strlist[index],index+1,min(maxcount)) 
    return outputtuple
   

# str = read_text_file('data/text1_ciphered.txt')
# List = read_word_list('data/english.txt')


# print(caesar_dechiper(str,List))
