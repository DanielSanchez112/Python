#solucion lenta del video

def GCD(a,b):
    current = 0        
    for i in range(1,a+b):
        if a%i == 0 and b%i == 0:
            current = i
            
    return current
        
if __name__ == '__main__':
    a, b = map(int, input().split())
    print(GCD(a,b))