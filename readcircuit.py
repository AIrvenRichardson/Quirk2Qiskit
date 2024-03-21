#Quirk stores circuits in the url, so I simply have to parse the string
#Heres a test link https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}
#Quantum Teleportation link "https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22,1,%22X^t%22],[%22%E2%80%A2%22,%22X%22,%22Bloch%22],[1,%22X%22,%22%E2%80%A2%22],[1,1,%22H%22],[1,%22Measure%22,%22Measure%22],[%22X%22,%22%E2%80%A2%22],[%22Z%22,1,%22%E2%80%A2%22]]}"
#It is the bell plus state
import re #gonna need this for parsing.

def parseURL():
    print('Hand over the link:')
    url = "https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}" #use input(), hardcoded is for testing quickly
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
            pureGate = gate.replace("[", "").replace("]", "").replace("%E2%80%A2","C")
            #Remove gates that dont exist in qiskit
            if((pureGate == "Bloch") | (pureGate == "X^t") | (pureGate == "Y^t") | (pureGate == "Z^t")):
                print("This gate is a no no: " + str(pureGate))
                line.append("1") #appends the identity gate so all columns have a number of gates = qubits
            else:
                line.append(pureGate)
        qubitOps.append(line)

    return qubitOps

def getNumQubits(qubitOps = []):
    if(qubitOps != []):
        numQubits = 0
        for col in qubitOps:
            qubitsinColumn = len(col)
            if qubitsinColumn > numQubits:
                numQubits = qubitsinColumn
        return(numQubits)
    else:
        print("No Circuit?")

def makeLines(numQubits, qubitOps):
    #Create the starting lines for any quantum circuit
    lines = []
    lines.append(f"q = QuantumRegister({numQubits})\n")
    lines.append(f"c = QuantumRegister({numQubits})\n")
    lines.append(f"circuit = QuantumCircuit(q,c)\n")
    #iterate over the gates to make the circuit
    for col in qubitOps:
        #check for control bits
        if("C" in col):
            cbit = col.index("C")
            for i in range(0,len(col)):
                if ((col[i]!="1") & (i!=cbit)):
                    lines.append(f"circuit.c{col[i].lower()}({cbit},{i})\n")
        #append normally otherwise (MEASUREMENT GATES ARE NOT YET ACCOUNTED FOR!)
        else:
            for i in range(0,len(col)):
                if (col[i]!="1"):
                    lines.append(f"circuit.{col[i].lower()}({i})\n")
    return lines

def makeCircuit():
    ops = parseURL()
    numQ = getNumQubits(ops)
    lines = makeLines(numQ, ops)
    f=open("out.txt", 'w')
    for line in lines:
        f.write(line)

makeCircuit()