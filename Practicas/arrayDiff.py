def array_diff(a, b):
    for x in b:   
        for i in range(a.count(x)):
            a.remove(x)
    return a


array_diff([1,2,2,2,2,2,3,3,4,5,],[1,2])