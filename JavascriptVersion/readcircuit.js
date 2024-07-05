document.addEventListener("DOMContentLoaded", () => {

    let url = "https://algassert.com/quirk#circuit={%22cols%22:[[%22~k9dc%22],[%22~acen%22],[%22~jjp8%22]],%22gates%22:[{%22id%22:%22~k9dc%22,%22name%22:%22ent%22,%22circuit%22:{%22cols%22:[[%22H%22],[%22%E2%80%A2%22,%22X%22]]}},{%22id%22:%22~jjp8%22,%22name%22:%22unent%22,%22circuit%22:{%22cols%22:[[%22X%22,%22%E2%80%A2%22],[1,%22H%22]]}},{%22id%22:%22~acen%22,%22name%22:%22xz%22,%22circuit%22:{%22cols%22:[[%22X%22],[%22Z%22]]}}]}";
    const uButton = document.querySelector("#UrlButton");
    const out = document.querySelector('#pycode');

    uButton.addEventListener("click", getUrl);
    
    function getUrl(){
        url = prompt("Please paste your Quirk link here.");
        out.textContent = parseURL(url);

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
            gates = [...s.matchAll(re)]
            ees = [] //I am so sorry for this name, I legitmately don't know what it stood for in the original code, my bad
            for (gate of gates){
                ees.push(gate[0])
            }
            //TODO: ees needs to be parsed as a circuit
        }
        return s;
    }

    function parseCircuit(){
        //Unimplemented
    }

    function makeCustomGates(){
        //Unimplemented
    }

    
});