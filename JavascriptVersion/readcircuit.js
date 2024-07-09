document.addEventListener("DOMContentLoaded", () => {

    const validGates = new Map([ //This is a list of currently supported gates, it can be easily expanded and the value stored in tha map can later be used for the qiskit version of the gate (for things like Y to rootZ)
        ["Z", "z"],
        ["X", "x"],
        ["C", "c"],
        ["AC", "ac"],
        ["H", "h"],
        ["Y", "y"],
        ["1", "1"],
        ["Measure", "measure"]
    ]);

    let url = "https://algassert.com/quirk#circuit={%22cols%22:[[%22~k9dc%22],[%22~acen%22],[%22~jjp8%22]],%22gates%22:[{%22id%22:%22~k9dc%22,%22name%22:%22ent%22,%22circuit%22:{%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}},{%22id%22:%22~jjp8%22,%22name%22:%22unent%22,%22circuit%22:{%22cols%22:[[%22X%22,%22%E2%80%A2%22],[1,%22H%22]]}},{%22id%22:%22~acen%22,%22name%22:%22xz%22,%22circuit%22:{%22cols%22:[[%22X%22],[%22Z%22]]}}]}";
    const uButton = document.querySelector("#UrlButton");
    const out = document.querySelector('#pycode');

    uButton.addEventListener("click", getUrl);
    
    function getUrl(){
        url = prompt("Please paste your Quirk link here.");
        //I should probably put text that says "please wait" on the page since larger circuits can get a little slow
        let res = parseURL(url);
        res = makeLines(res);
        res = textFromLines(res);
        out.textContent = res;

    }
   
    function parseURL(s){
        //Replace the odd bracket replacements that happen sometimes
        s = s.replaceAll("%7B", "{").replaceAll("%7D","}");

        //This regex extracts only the circuit and gate portions of the URL
        let re = /\{.*?\}/;
        s = re.exec(s)[0];

        //Now that we have just the circuit and gates, replace the % characters with the actual ones for readability.
        s = s.replaceAll("%22",""); //delete quotation marks
        circuitandgates = s.split("gates"); //split the string into the actual circuit and the custom gates

        //Check if there are custom gates in the circuit, replacing their names with their actual gates into the original string if needed.
        if(circuitandgates.length > 1){
            return "ERROR: CUSTOM GATES NOT IMPLEMENTED";
        }
        else{
            re = /\[.*?\]/g;
            const gates = [...s.matchAll(re)];
            let cols = [];
            for (gate of gates){
                cols.push(gate[0]);
            }
            //TODO: cols needs to be parsed as a circuit
           let qubitOps = parseCircuit(cols);
           return qubitOps;
        }
        return s;
    }

    function parseCircuit(cols){
        //Making a 2d array for the circuit that looks like [Column][Qubit]
        let qubitOps = [];
        //Iterate over cols, adding each gate into the array as a simple codes for reading
        for (col of cols){
            line = [];
            ops = col.split(",") ;//make a list of gates
            for (op of ops){
                //Remove brackets, replace gate identifiers with their simpler ones
                clean = op.replaceAll("[", "").replaceAll("]", "").replaceAll("%E2%80%A2","C").replaceAll("%E2%97%A6","AC");
                //If the gate is valid, add it to the line
                if(validGates.has(clean)){
                    line.push(clean);
                }
                //otherwise log it and replace it with an identity gate (so the resulting code still has the gates in the right spots)
                else{
                    console.log("ERROR: " + clean + " is not a valid gate!");
                    line.push("1");
                }
            }
            qubitOps.push(line);
        }
        return qubitOps;
    }

    function makeCustomGates(){
        //Unimplemented, not sure if I will implement this one unless I get a huge burst of motivation, the python version has some problems so I will need to figure out what I can do about it first.
    }

    function getNumQubits(qubitOps){
        //make sure things have been working so far
        if (qubitOps == []){
            console.log("There's no circuit here? Please check your url.");
            return 0;
        }
        //simply get the max length of the columns
        let numQubits = 0;
        for (col of qubitOps){
            numQubits = Math.max(numQubits, col.length);
        }
        return numQubits;
    }

    function makeLines(qubitOps){
        //get the number of qubits needed
        let numQubits = getNumQubits(qubitOps);
        //Create the starting lines for the circuit
        lines = [];
        lines.push("q = QuantumRegister("+numQubits+")\n");
        lines.push("c = ClassicalRegister("+numQubits+")\n");
        lines.push("circuit = QuantumCircuit(q,c)\n");
        //Iterate over the gates to make the circuit
        for (col of qubitOps){
            console.log(col)
            //Check for controls and anti-controls
            if ((col.includes("C")) || (col.includes("AC"))){
                //Get the indicies of the controls and anti-controls
                es = col.entries();
                controls = [];
                antis = [];
                for (e of es){
                    if (e[1] == "C"){
                        controls.push(e[0]);
                    }
                    else if (e[1] == "AC"){
                        //We still need the anti-controls in the controls list, the antis list is for knowing which qubits need to be hit with an X gate before and after being controls
                        controls.push(e[0]);
                        antis.push(e[0]);
                    }
                }
                //Add an x gate before all the anti-controls
                for(i of antis){
                    lines.push("circuit.x("+i+")\n");
                }
                for (let i = 0; i < col.length; i++){
                    //if the gate is NOT a control or identity, sorry about the nested ifs but they need to happen because multi-controls are super complicated in qiskit for some reason
                    if ((col[i]!="1") && (col[i]!="AC") && (col[i]!="C")){
                        //do we need to make a multi-control gate?
                        if (controls.length > 1){
                            //X needs to be treated differently than the other basic gates
                            if(col[i] == "X"){
                                lines.push("circuit.mc"+validGates.get(col[i])+"(["+controls+"],"+i+")\n");
                            }
                            //If it isn't an X, we must use an MCMT gate
                            else{
                                lines.push("#WARNING, AER SIMULATOR CANNOT SIMULATE THIS GATE. PLEASE DECOMPOSE THE CIRCUIT WITH circuit.decompose(reps = some number until it works)!\n");
                                lines.push("mcmt = MCMT('"+validGates.get(col[i])+"',"+controls.length+",1)\n");
                                lines.push("mcmt.name = \"mc"+col[i]+"\"\n");
                                let mcmtList = controls.slice();
                                mcmtList.push(i);
                                lines.push("circuit.append(mcmt, ["+mcmtList+"] )\n");
                            }
                        }
                        //do a much simpler gate type if its just one control
                        else{
                            lines.push("circuit.c"+validGates.get(col[i])+"("+controls[0]+","+i+")\n");
                        }
                    }
                }
                //finally, flip the anti controls back
                for(i of antis){
                    lines.push("circuit.x("+i+")\n");
                }

            }
            //if there are no controls present, append normally.
            else{
                for (let i = 0; i < col.length; i++){
                    if(col[i] == "Measure"){
                        lines.push("circuit.measure(["+i+"],["+i+"])\n");
                    }
                    else if (col[i] != "1"){
                        lines.push("circuit."+validGates.get(col[i])+"("+i+")\n")
                    }
                }
            }
        }
        return lines
    }
    
    function textFromLines(lines){
        let out = "";
        for (line of lines){
            out += line;
        }
        return out;
    }
});