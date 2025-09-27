#sorting one number
def insertion_sort(arr, j) -> list:
    for i in range(j-1, -1, -1):
        n1 = arr[i+1]
        n2 = arr[i]
        if n1 < n2:
            arr[i+1] = n2
            arr[i] = n1
        else:
            break
    return arr

print(insertion_sort([1,2,4,6,8,3], 5))

#sortin mor than one
def insertion_full_sorted(arr) -> list:
    for i in range(len(arr)-2, 0, -1):
        print(arr[i], "  ", arr[i+1])
        n1 = arr[i+1]
        n2 = arr[i]
        if n1 < n2:
            arr[i+1] = n2
            arr[i] = n1
        else: continue
        
    return arr

print(insertion_full_sorted([1,2,4,6,8,3,7,12,10,13,15,16,19,17]))
