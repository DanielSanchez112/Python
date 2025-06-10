#naive form of fibonacci number

def FibRecurs(maxNum: int)-> int:
    n = maxNum
    if n <= 1:
        return n  
    
    return FibRecurs(n - 1) + FibRecurs(n - 2)

if __name__ == '__main__':
    n = int(input())
    print(FibRecurs(n))
    