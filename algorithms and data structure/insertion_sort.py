def insertionSort(arr: list) -> list:
    n = len(arr)
    for i in range(1, n):
        index = arr[i]
        currentValue = arr.pop(i)
        for j in range(i-1,-1,-1):
            if arr[j] > currentValue:
                index = j
        arr.insert(index, currentValue)
    return arr

#test
print(insertionSort([5, 2, 4, 6, 1, 3])) #[1, 2, 3, 4, 5, 6]
print(insertionSort([31, 41, 59, 26, 41, 58])) #[26, 31, 41, 41, 58, 59]
