def FibRecurs(n: int)-> int:
    fib = [0,1]
    if n <= 1:
        return n
    for i in range(2, n+1):
        fib.append((fib[i-1]+fib[i-2]))
    
    return fib[n]

if __name__ == '__main__':
    n = int(input())
    print(FibRecurs(n))
