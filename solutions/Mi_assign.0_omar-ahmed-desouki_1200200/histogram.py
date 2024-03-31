from typing import Any, Dict, List
import utils


def histogram(values: List[int]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the
    list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} 
    since 3 appears twice while 5 appears once 
    '''
    unique_values = set(values)
    output_dict = {}

    for sett in unique_values:
        j=-1
        count =0
        length = len(values)-1
        for item in values:

            j+=1
            if j > length:     #condition 3shan lw mtb2ash 8er element wahed
                output_dict[sett] = 1
                return output_dict

            if sett == values[j]:
                count += 1 
        
            if j == length:  #zawed 3dd el element fe el output_dictionary
                output_dict[sett] = count

    return output_dict 
#lazem  tzwed condition en lw msek nafs el value tany

# values :list = input("Enter the list : ")
# #values :list = [3,5,3,3,3,3,5,5,5,5,6,7,8,9,10]
# histogram(values)
# print(histogram(values))


