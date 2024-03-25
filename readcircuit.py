#Quirk stores circuits in the url, so I simply have to parse the string
#Test links can now be found in the testlinks.txt file
import re #gonna need this for parsing.

def parseURL():
    print('Hand over the link:')
    url = input() #use input(), hardcoded is for testing quickly
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
            pureGate = gate.replace("[", "").replace("]", "").replace("%E2%80%A2","C").replace("%E2%97%A6","AC")
            #Remove gates that dont exist in qiskit
            if((pureGate == "Bloch") | (pureGate == "X^t") | (pureGate == "Y^t") | (pureGate == "Z^t")):
                print("This gate is not in Qiskit: " + str(pureGate))
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

#TODO: manage custom gates from quirk
def makeLines(numQubits, qubitOps):
    #Create the starting lines for any quantum circuit
    lines = []
    lines.append(f"q = QuantumRegister({numQubits})\n")
    lines.append(f"c = ClassicalRegister({numQubits})\n")
    lines.append(f"circuit = QuantumCircuit(q,c)\n")
    #iterate over the gates to make the circuit
    for col in qubitOps:
        #check for control bits
        if("C" in col) or ("AC" in col):
            #Grab the index of each control-type gate, we need to know the location of the anti controls separately since they need to be handled.
            controls = [i for i, x in enumerate(col) if x == "C"]
            antis = [i for i, x in enumerate(col) if x == "AC"]
            #combine the control indexes together for the multi-control gate.
            for a in antis: controls.append(a)
            #Flip all anti-controls on the x axis, this is because a |0> in an anti control is just a |1> in a normal control
            for index in antis:                      
                                lines.append(f"circuit.x({index})\n")
            #apply the controls to all non-control gates in the circuit.
            for i in range(0,len(col)):
                if ((col[i]!="1") & (col[i]!="AC") & (col[i]!="C")):
                    if (len(controls) > 1):                    
                        lines.append(f"circuit.mc{col[i].lower()}({controls},{i})\n")
                    else:
                        lines.append(f"circuit.c{col[i].lower()}({controls[0]},{i})\n") #Do a simpler gate type if there is onyl one control in the column.
            #flip the anti-controls back to their orignal state after they were used in a normal control.
            for index in antis:                      
                                lines.append(f"circuit.x({index})\n")

        #append normally otherwise 
        else:
            for i in range(0,len(col)):
                if(col[i] == "Measure"):
                    lines.append(f"circuit.measure([{i}],[{i}])\n")
                elif (col[i]!="1"):
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