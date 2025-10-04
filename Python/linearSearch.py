def linear_search(arr, target):
    """
    Performs a linear search for 'target' in the list 'arr'.
    Returns the index of target if found, else returns -1.
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i  # Element found, return its index
    return -1  # Element not found

# Example usage
numbers = [10, 20, 30, 40, 50]
target = 30

result = linear_search(numbers, target)

if result != -1:
    print(f"Element {target} found at index {result}.")
else:
    print(f"Element {target} not found in the list.")
