# Online Python Playground
import math
# Use the online IDE to write, edit & run your Python code
# Create, edit & delete files ondef
def findMid(arr):
    nums = sorted(arr)
    number = nums[math.ceil(len(nums)/2)-1]
    return number

anwser = findMid([5,1,3,2,4])
print(anwser)