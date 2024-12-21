def weirdAlgorithm(n):
    while True:
        if (n % 2) == 0:
            n = n/2
        elif (n % 2) != 0:
            n = (n*3) + 1
        elif n == 1:
            print(n)
            break
        

weirdAlgorithm(3) 
