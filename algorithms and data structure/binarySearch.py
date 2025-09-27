def binarySearch(arr, target) -> int:
    """
    Binary Search Algorithm
    This function performs a binary search on a sorted list to find the index of a target value.
    If the target is not found, it returns -1.
    """
    # Initialize the left and right pointers
    left = 0
    right = len(arr) - 1

    # Perform binary search
    while left <= right:
        mid = (left + right) // 2

        # Check if the target is present at mid
        if arr[mid] == target:
            return mid
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        # If target is smaller, ignore right half
        else:
            right = mid - 1

    # Target was not found in the array
    return -1

# Example usage
if __name__ == "__main__":
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    target = 5
    result = binarySearch(arr, target)
    if result != -1:
        print(f"Element found at index {result}")
    else:
        print("Element not found in the array")