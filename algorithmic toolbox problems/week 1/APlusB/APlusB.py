def sum_of_two_digits(num1: int, num2: int) -> int:
    sum = num1 + num2
    return sum


if __name__ == '__main__':
    a, b = map(int, input().split())
    print(sum_of_two_digits(a, b))