def bubbleSort(arr: list) -> list:
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j +1]:
                arr[j],arr[j +1] = arr[j +1],arr[j]
    return arr

def bubbleSort2(my_array: list) -> list:
    n = len(my_array)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            if my_array[j] > my_array[j+1]:
                my_array[j], my_array[j+1] = my_array[j+1], my_array[j]
                swapped = True
        if not swapped:
            break
    return my_array

# Test
print(bubbleSort([64, 34, 25, 12, 22, 11, 90])) # [11, 12, 22, 25, 34, 64, 90]
print(bubbleSort([5, 1, 4, 2, 8])) # [1, 2, 4, 5, 8]

print(bubbleSort2([7, 12, 9, 11, 3])) # [3, 7, 9, 11, 12]
    