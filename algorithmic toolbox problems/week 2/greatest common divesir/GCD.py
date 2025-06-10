#mi solucion ates de ver el vido sobre la forma bruta y la forma optimizada

def GCD(a,b):
    current = 0
    if a == b:
        return a
    if a < b:
        n = b
    else:
        n = a
        
    for i in range(1,n):
        if a%i == 0 and b%i == 0:
            current = i
            
    return current
        
if __name__ == '__main__':
    a, b = map(int, input().split())
    print(GCD(a,b))