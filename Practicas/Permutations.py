def permutations(num):
    numbers = []
    
    if(num == 2 or num == 3):
            print("NO SOLUTION")
            return
    
    for i in range(2, num + 1, 2):
        numbers.append(i)
    
    for i in range(1, num +1, 2):
        numbers.append(i)
        
    print(" ".join(map(str, numbers)))
    
permutations(int(input()))

