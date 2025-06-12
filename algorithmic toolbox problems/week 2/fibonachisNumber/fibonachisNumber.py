import time
#la forma mia de hacer este sin ver los videos 

def FibNum(n):
    sum = 0
    first = 1
    second = 0
    if n <= 1:
        return n
    for i in range(2, n+1):
        sum = first + second
        second =  first
        first = sum
        #print("itreacion: ",i,"|suma: ", sum,"|primero: ", first,"|segundo: ", second)
        
    return sum

if __name__ == '__main__':
    n = int(input())
    start = time.time()
    print(FibNum(n))
    end = time.time()
    print(f"Tiempo de ejecucion: {end - start:.8f} segundos")
