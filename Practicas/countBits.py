def count_bits(n):
    list = []   
    while(n >= 1):
        list.append(int (n%2))
        n = n/2

    print(list.count(1))
    print(list)

    return list.count(1) 

count_bits(8)