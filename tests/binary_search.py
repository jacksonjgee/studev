numbers = list(map(int, input().split()))
target = int(input())

def binarysearch(numbers, target, bottom, top):
    if bottom > top:          # nothing left to search
        return -1

    middle = (bottom + top) // 2
    if numbers[middle] == target:
        return middle
    elif numbers[middle] > target:
        return binarysearch(numbers, target, bottom, middle - 1)
    else:
        return binarysearch(numbers, target, middle + 1, top)

print(binarysearch(numbers, target, 0, len(numbers) - 1))