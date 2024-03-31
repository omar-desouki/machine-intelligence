list = [1,2 ,3, 4, 5, 6, 7, 8, 9]
count = 0
while count <2:

    for num in list:
        print(num)
        if num == 5:
            list= [7,8,9,5]
            count +=1
            break
