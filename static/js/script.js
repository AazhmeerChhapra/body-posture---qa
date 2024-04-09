const convertText = document.getElementById("convert_text");
const startButton = document.getElementById("click_to_record");
const stopButton = document.getElementById("click_to_stop");
let recognition;
let lastTranscript = '';

startButton.addEventListener('click', function() {
    recognition = new window.webkitSpeechRecognition();
    recognition.interimResults = true;
    recognition.continuous = true; // Enable continuous recognition

    recognition.addEventListener('result', e => {
        const transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('');

        if (transcript !== lastTranscript) {
            convertText.value = transcript; // Update textarea with new transcript
            lastTranscript = transcript; // Update lastTranscript
            console.log(transcript);
        }
    });

    recognition.start();
});


stopButton.addEventListener('click', function() {
    if (recognition) {
        recognition.stop();
    }
});
