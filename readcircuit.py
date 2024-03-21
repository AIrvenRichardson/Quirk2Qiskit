#Quirk stores circuits in the url, so I simply have to parse the string
#Heres a test link https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}
#It is the bell plus state
import re #gonna need this for parsing.

print('Hand over the link:')
url = "https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}" #use input(), hardcoded is for testing quickly
print("thanks") 

#https://www.geeksforgeeks.org/python-extract-substrings-between-brackets/
regsult = re.findall(r'\{.*?\}', url)
circuitString = regsult[0]
circuitString = circuitString.replace("%22", "")
ees = re.findall(r'\[.*?\]', circuitString)

#Now grab each gate for each circuit, make a 2d array of [Qubit][Gate]
qubitOps = []
for wire in ees:
    line = []
    operations = wire.split(',')
    for gate in operations:
        pureGate = gate.replace("[", "").replace("]", "")
        line.append(pureGate)
    qubitOps.append(line)

print(qubitOps)