"""Simple code to count the number of lines in distinct.txt"""

count = 0
iFile = open("distinct.txt", "r+")
for line in iFile:
    count += 1
print("Total number of distinct articles: ", count)