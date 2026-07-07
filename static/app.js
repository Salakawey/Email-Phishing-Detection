async function sendToClassifier() {
    const textInput = document.getElementById("emailInput").value.trim();
    const btn = document.getElementById("scanBtn");
    const resultsCard = document.getElementById("resultsCard");
    const verdictText = document.getElementById("verdictText");
    const phishBar = document.getElementById("phishBar");
    const safeBar = document.getElementById("safeBar");
    const phishProgress = document.getElementById("phishProgress");
    const safeProgress = document.getElementById("safeProgress");
    const verdictIcon = document.getElementById("verdictIcon");

    if (!textInput) {
        alert("⚠️ Please paste email content before scanning.");
        return;
    }

    // Loading state
    const originalBtnText = btn.innerHTML;
    btn.innerHTML = `
        <i class="fas fa-spinner fa-spin"></i> 
        <span>Analyzing with AI...</span>
    `;
    btn.disabled = true;

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textInput })
        });

        if (!response.ok) {
            throw new Error("Server responded with error");
        }

        const data = await response.json();

        // Show results
        resultsCard.classList.remove("hidden");
        
        verdictText.innerText = data.prediction;
        
        const phishPct = parseFloat(data.phishing_probability);
        const safePct = parseFloat(data.safe_probability);

        phishBar.innerText = data.phishing_probability;
        safeBar.innerText = data.safe_probability;

        // Animate progress bars
        phishProgress.style.width = '0%';
        safeProgress.style.width = '0%';

        // Trigger reflow
        void phishProgress.offsetWidth;

        phishProgress.style.width = `${phishPct}%`;
        safeProgress.style.width = `${safePct}%`;

        // Set verdict styling and icon
        resultsCard.classList.remove("danger-verdict", "safe-verdict");
        
        if (data.prediction === "Phishing") {
            resultsCard.classList.add("danger-verdict");
            verdictIcon.innerHTML = `<i class="fas fa-exclamation-triangle" style="color: #f87171;"></i>`;
        } else {
            resultsCard.classList.add("safe-verdict");
            verdictIcon.innerHTML = `<i class="fas fa-shield-alt" style="color: #34d399;"></i>`;
        }

    } catch (err) {
        console.error(err);
        alert("❌ Could not connect to the AI backend. Make sure the server is running.");
    } finally {
        // Reset button
        btn.innerHTML = originalBtnText;
        btn.disabled = false;
    }
}

function resetAnalysis() {
    const resultsCard = document.getElementById("resultsCard");
    const emailInput = document.getElementById("emailInput");
    
    resultsCard.classList.add("hidden");
    emailInput.value = "";
    emailInput.focus();
}

// Allow pressing Enter in textarea to scan (Ctrl+Enter)
document.addEventListener('keydown', function(e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        sendToClassifier();
    }
});