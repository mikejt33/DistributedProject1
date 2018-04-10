"""For cleaning data from datagrab.py into an SQL friendly form.

Author: Joe
"""

iFile = open("data_of_interest.csv", "r+")
oFile = open("clean.csv", "w+")

for line in iFile:
    output = ""
    splt = line.split("")
    for field in splt:
        row = field.split()
        if row[0] == "REVISION":
            output = output + row[3] + "|" + row[4] + "|" + row[5] + "|" + row[6] + "|"
            #print("end of revision loop", output)
        if row[0] == "COMMENT":
            for stuff in row[1:]:
                output = output + stuff + " "
            #output = output[:-1]
            #print("end of comment loop", output)
    output = output + "|" + line[-2] + "\n"
    oFile.write(output)