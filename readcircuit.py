#Quirk stores circuits in the url, so I simply have to parse the string
#Heres a test link https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}
#It is the bell plus state
import re #gonna need this for parsing.

def parseURL():
    print('Hand over the link:')
    url = "https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22,1,%22X^t%22],[%22%E2%80%A2%22,%22X%22,%22Bloch%22],[1,%22X%22,%22%E2%80%A2%22],[1,1,%22H%22],[1,%22Measure%22,%22Measure%22],[%22X%22,%22%E2%80%A2%22],[%22Z%22,1,%22%E2%80%A2%22]]}" #use input(), hardcoded is for testing quickly
    print("thanks") 

    #https://www.geeksforgeeks.org/python-extract-substrings-between-brackets/
    regsult = re.findall(r'\{.*?\}', url)
    circuitString = regsult[0]
    circuitString = circuitString.replace("%22", "")
    ees = re.findall(r'\[.*?\]', circuitString)

    #Now grab each gate for each circuit, make a 2d array of [Column][Qubit]
    qubitOps = []
    for wire in ees:
        line = []
        operations = wire.split(',')
        for gate in operations:
            pureGate = gate.replace("[", "").replace("]", "")
            #Remove gates that dont exist in qiskit
            if((pureGate == "Bloch") | (pureGate == "X^t") | (pureGate == "Y^t") | (pureGate == "Z^t")):
                print("This gate is a no no: " + str(pureGate))
                line.append("1") #appends the identity gate so all columns have a number of gates = qubits
            else:
                line.append(pureGate)
        qubitOps.append(line)

    return qubitOps

ops = parseURL()
print(ops)