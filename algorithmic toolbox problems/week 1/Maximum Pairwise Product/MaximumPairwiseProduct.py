#here using the sorting method to find the maximum pairwise product provided by python

import time

def maximum_pairwise_product(n: int, numbers: list):
    numbers.sort(reverse=True)
    result = numbers[0] * numbers[1]
    return result

if __name__ == '__main__':
    _ = int(input())
    numbers = list(map(int, input().split()))

    start_time = time.time()
    result = maximum_pairwise_product(_, numbers)
    end_time = time.time()

    print(result)
    print(f"Tiempo de ejecución: {end_time - start_time:.6f} segundos")
