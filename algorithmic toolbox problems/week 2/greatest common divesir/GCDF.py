def EuclidGCD(a, b):
    if b == 0:
        return a
    aP = a%b
    print('A=',a,'| B=',b, "| A'=",aP)
    return EuclidGCD(b,aP)

if __name__ == '__main__':
    a, b = map(int, input().split())
    print(EuclidGCD(a,b))