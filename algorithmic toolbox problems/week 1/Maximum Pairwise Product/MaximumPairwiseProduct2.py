#here scaning 2 times to find the tow largest numbers

def maximum_pairwise_product(n: int, numbers: list):
    max1 = 0
    max2 = 0
    for i in range(n):
        if max1 < numbers[i]:
            max2 = max1
            max1 = numbers[i]
        elif max2 < numbers[i]:
            max2 = numbers[i]
            
    return max1 * max2

if __name__ == '__main__':
    _ = int(input())
    numbers = list(map(int, input().split()))
    print(maximum_pairwise_product(_, numbers))