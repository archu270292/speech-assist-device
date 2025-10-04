function setPreset(text) {
  document.getElementById("userInput").value = text;
  sendText(); // auto-speak when clicked
}

async function sendText() {
  const input = document.getElementById("userInput").value;
  const lang = document.getElementById("language").value;
  const status = document.getElementById("status");
  const player = document.getElementById("audioPlayer");
  const expandedTextElem = document.getElementById("expandedText");

  status.textContent = "Processing...";
  expandedTextElem.textContent = "";
  player.src = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/speak", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: input, lang: lang })
    });

    if (!response.ok) {
      throw new Error("Server error: " + response.status);
    }

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    // ✅ Show message + English translation in a styled card
    expandedTextElem.innerHTML = `
      <div style="
        margin-top: 20px; 
        padding: 15px; 
        border-radius: 10px; 
        background: #f9f9f9; 
        box-shadow: 0 2px 6px rgba(0,0,0,0.1); 
        text-align: center;
      ">
        <p style="font-size: 18px; font-weight: bold; margin: 5px 0;">
          Message (${lang}): ${data.expanded_text}
        </p>
        <p style="color: gray; font-style: italic; margin: 5px 0;">
          English Translation: ${data.english_translation}
        </p>
      </div>
    `;

    // ✅ Play audio
    player.src = "http://127.0.0.1:5000" + data.audio_url;
    player.play();

    status.textContent = "Done!";
    status.className = "";
  } catch (err) {
    status.textContent = "Error: " + err.message;
    status.className = "error";
  }
}
