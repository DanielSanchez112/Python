def minVal(arr: list) -> int:
    minVal = arr[0]
    for i in arr:
        if i < minVal:
            minVal = i
    return minVal