async function sendToClassifier() {
    const textInput = document.getElementById("emailInput").value;
    const btn = document.getElementById("scanBtn");
    const resultsCard = document.getElementById("resultsCard");
    const verdictText = document.getElementById("verdictText");

    // Block empty entries
    if (!textInput.trim()) {
        alert("Please paste some text content before scanning.");
        return;
    }

    // Update UI button state to loading
    btn.innerText = "Analyzing Context via Server...";
    btn.disabled = true;

    try {
        // Send a POST request containing the email text payload to FastAPI
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();

        // Clear previous alert designs
        resultsCard.classList.remove("hidden", "danger-verdict", "safe-verdict");
        
        // Populate layout fields with response metadata
        verdictText.innerText = data.prediction;
        document.getElementById("phishBar").innerText = data.phishing_probability;
        document.getElementById("safeBar").innerText = data.safe_probability;

        // Apply color based on threat analysis verdict
        if (data.prediction === "Phishing") {
            resultsCard.classList.add("danger-verdict");
        } else {
            resultsCard.classList.add("safe-verdict");
        }

    } catch (err) {
        console.error(err);
        alert("Could not connect to the FastAPI backend framework.");
    } finally {
        // Reset button state
        btn.innerText = "Scan Email Content";
        btn.disabled = false;
    }
}