let savedObj;
let savedSentiment;

function addPrompt(text) {
  document.getElementById("promptButton").disabled = true;
  let finalElement = document.getElementById("final");
  if (finalElement.innerText.length > 1)
    finalElement.innerHTML += "<br><br><br>";
  finalElement.innerHTML += "<h5></h5>";
  scrollJournalBottom();
  animateTyping(text, finalElement.id);
}

function scrollJournalBottom() {
  let journal = $("#journal-inner .simplebar-content-wrapper");
  journal.animate({ scrollTop: journal.prop("scrollHeight") }, 400);
}

function animateTyping(text, parentId) {
  let parent = document.getElementById(parentId);
  parent.lastElementChild.innerHTML += text.charAt(0);
  if (text.length == 1) {
    parent.innerHTML += "<br>";
    scrollJournalBottom();
    setEndOfContenteditable(parent);
    document.getElementById("promptButton").disabled = false;
    return;
  }
  let pauseMS = 10 + Math.floor(Math.random() * 100);
  window.setTimeout(function() { animateTyping(text.substring(1), parentId); }, pauseMS);
}

function getAndInsertPrompt() {
  $.get("/prompt/", {
    text: document.getElementById("final").innerText,
      lastObj: savedObj,
      lastSentiment: savedSentiment
  })
    .done(function(data) {
      addPrompt(data.question);
      savedObj = data.lastObj;
      savedSentiment = data.lastSentiment
    });
}

function setEndOfContenteditable(contentEditableElement) {
  let range, selection;
  range = document.createRange();
  range.selectNodeContents(contentEditableElement);
  range.collapse(false);
  selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}


/**
 * Begins a stream with rev.ai using the AudioContext from the browser. Stream will continue until the websocket 
 * connection is closed. Follows the protocol specficied in our documentation:
 * https://www.rev.ai/docs/streaming
 */
function doStream() {
    partialElement = document.getElementById("partial");
    finalElement = document.getElementById("final");
    finalsReceived = 0;
    audioContext = new (window.AudioContext || window.WebkitAudioContext)();

    const access_token = '02WfsoJ_CZ9RgmNoJh38wAO536lPR7-j0iO7461C9XMn3myA1KG9JeeeGTSGVt3Iy412YUV50aHWoGhdLt9TRbaNJfD6U';
    const content_type = `audio/x-raw;layout=interleaved;rate=${audioContext.sampleRate};format=S16LE;channels=1`;
    const baseUrl = 'wss://api.rev.ai/speechtotext/v1alpha/stream';
    const query = `access_token=${access_token}&content_type=${content_type}`;
    websocket = new WebSocket(`${baseUrl}?${query}`);

    websocket.onopen = onOpen;
    websocket.onclose = onClose;
    websocket.onmessage = onMessage;
    websocket.onerror = console.error;

    let button = document.getElementById("recordButton");
    button.onclick = endStream;
    button.innerHTML = "Stop";
}

/**
 * Gracefully ends the streaming connection with rev.ai. Signals and end of stream before closing and closes the 
 * browser's AudioContext
 */
function endStream() {
    if (websocket) {
        websocket.send("EOS");
        websocket.close();
    }
    if (audioContext) {
        audioContext.close();
    }

    partialElement.innerHTML = "";
    let button = document.getElementById("recordButton");
    button.onclick = doStream;
    button.innerHTML = "Record";
}

/**
 * Updates the display and creates the link from the AudioContext and the websocket connection to rev.ai
 * @param {Event} event 
 */
function onOpen(event) {
    console.log("Opened");
    navigator.mediaDevices.getUserMedia({ audio: true }).then((micStream) => {
        audioContext.suspend();
        let scriptNode = audioContext.createScriptProcessor(4096, 1, 1 );
        let input = input = audioContext.createMediaStreamSource(micStream);
        scriptNode.addEventListener('audioprocess', (event) => processAudioEvent(event));
        input.connect(scriptNode);
        scriptNode.connect(audioContext.destination);
        audioContext.resume();
    });
}

/**
 * Displays the close reason and code on the webpage
 * @param {CloseEvent} event
 */
function onClose(event) {
    console.log(`Closed with ${event.code}: ${event.reason}`);
}

/**
 * Handles messages received from the API according to our protocol
 * https://www.rev.ai/docs/streaming#section/Rev.ai-to-Client-Response
 * @param {MessageEvent} event
 */
function onMessage(event) {
    let data = JSON.parse(event.data);
    switch (data.type){
        case "connected":
            console.log(`Connected, job id is ${data.id}`);
            break;
        case "partial":
            partialElement.innerHTML = parseResponse(data);
            break;
        case "final":
            partialElement.innerHTML = "";
            if (data.type == "final"){
                finalsReceived++;
                finalElement.innerHTML += " " + parseResponse(data);
            }
            break;
        default:
            // We expect all messages from the API to be one of these types
            console.error("Received unexpected message");
            break;
    }
}

/**
 * Transform an audio processing event into a form suitable to be sent to the API. (S16LE or Signed 16 bit Little Edian).
 * Then send.
 * @param {AudioProcessingEvent} e 
 */
function processAudioEvent(e) {
    if (audioContext.state === 'suspended' || audioContext.state === 'closed' || !websocket) {
        return;
    }

    let inputData = e.inputBuffer.getChannelData(0);

    // The samples are floats in range [-1, 1]. Convert to PCM16le.
    let output = new DataView(new ArrayBuffer(inputData.length * 2));
    for (let i = 0; i < inputData.length; i++) {
        let multiplier = inputData[i] < 0 ? 0x8000 : 0x7fff; // 16-bit signed range is -32768 to 32767
        output.setInt16(i * 2, inputData[i] * multiplier | 0, true); // index, value, little edian
    }

    let intData = new Int16Array(output.buffer);
    let index = intData.length;
    while (index-- && intData[index] === 0 && index > 0) { }
    websocket.send(intData.slice(0, index + 1));
}

function parseResponse(response) {
    let message = "";
    for (let i = 0; i < response.elements.length; i++){
        message += response.type == "final" ?  response.elements[i].value : `${response.elements[i].value} `;
    }
    return message;
}
