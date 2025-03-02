def selectionSort(arr: list) -> list:
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

#test
print(selectionSort([5, 2, 4, 6, 1, 3])) #[1, 2, 3, 4, 5, 6]
print(selectionSort([31, 41, 59, 26, 41, 58])) #[26, 31, 41, 41, 58, 59]