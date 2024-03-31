import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    # string = string.lower()
    # reverse = ""
    # i=0
    # j=len(string)

    # for char in string:
    #     reverse += string[j-1]
    #     j=j-1

    # i=0
    # palindrome = 1
    # for char in string:
    #     if reverse[i] != string[i] :
    #         palindrome = 0

    # return palindrome

    string = string.lower()
    length=len(string)
    for i in range(length):
        if string[i] != string[length -1 -i] : # -1 3shan bybd2 mn zero
            return 0
        
    return 1

