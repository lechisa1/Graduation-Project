var caretPosition = 0; // Define caretPosition

function tokenizeText() {
    var inputText = document.getElementById("inputText");
    caretPosition = getCaretPosition(inputText); // Update caretPosition
    var text = inputText.innerText;

    // Send the input text to the server for tokenization
    fetch("/tokenize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            text: text,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Returned Tokens:", data.tokens);

        fetch("/detect_errors", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tokens: data.tokens,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Detected Errors:", data.errors);
            applyErrorStyling(data.errors);
            fetch("/correct_errors",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                },
                body: JSON.stringify({
                    errors: data.errors,
                }),
            })
            
            .then(response=>response.json())
            .then(data=>{
                console.log('Returned Corrections:', data.corrections);
                // Send the corrected words to the morphological generator route
                fetch("/generate_words",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                    },
                    body: JSON.stringify({
                        morphemes: data.corrections,
                    }),
                })
                .then(response=>response.json())
                .then(data=>{
                    console.log('Generated Words:', data.words);
                })
                .catch(error=>console.log('Error: ',error));
            })
            .catch(error=>console.log("Error: ",error));
        })
        .catch(error => console.error("Error:", error));
    })
    .catch(error => console.error("Error:", error));
}

function applyErrorStyling(errors) {
    var inputTextContainer = document.getElementById("inputText");
    var words = inputTextContainer.innerText.split(" ");
    
    inputTextContainer.innerHTML = "";

    words.forEach(word => {
        var span = document.createElement("span");
        span.textContent = word + " ";
        if (errors.includes(word.trim())) {
            span.classList.add("misspelled");
        }
        inputTextContainer.appendChild(span);
    });

    setCaretPosition(inputTextContainer);
}


function handlePaste(e) {
    e.preventDefault();
    var text = (e.originalEvent || e).clipboardData.getData('text/plain');
    document.execCommand("insertText", false, text);
}

function handleDrop(e) {
    e.preventDefault();
    var text = e.dataTransfer.getData("text");
    var selection = window.getSelection();
    if (!selection.rangeCount) return false;
    selection.deleteFromDocument();
    selection.getRangeAt(0).insertNode(document.createTextNode(text));
}

function getCaretPosition(editableDiv) {
    var caretPos = 0, sel, range;
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.rangeCount) {
            range = sel.getRangeAt(0);
            if (range.commonAncestorContainer.parentNode === editableDiv) {
                caretPos = range.endOffset;
            }
        }
    } else if (document.selection && document.selection.createRange) {
        range = document.selection.createRange();
        if (range.parentElement() === editableDiv) {
            var tempEl = document.createElement("span");
            editableDiv.insertBefore(tempEl, editableDiv.firstChild);
            var tempRange = range.duplicate();
            tempRange.moveToElementText(tempEl);
            tempRange.setEndPoint("EndToEnd", range);
            caretPos = tempRange.text.length;
        }
    }
    return caretPos;
}

function setCaretPosition(editableDiv) {
    var range = document.createRange();
    var sel = window.getSelection();
    range.selectNodeContents(editableDiv);
    range.collapse(false); // Collapse the range to the end point. false means collapse to end rather than the start
    sel.removeAllRanges();
    sel.addRange(range);
}


function handleInput(event) {
    var char = event.data; // The character that was inserted
    if (char === ' ' || char === '.' || char === ',' || char === '!' || char === '?') {
        tokenizeText();
    }
}
