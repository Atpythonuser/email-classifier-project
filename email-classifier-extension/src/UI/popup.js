// popup.js
const API_BASE = "http://localhost:8000"; // Change if backend runs elsewhere

document.getElementById("classifyBtn").addEventListener("click", async () => {
  const text = document.getElementById("emailText").value.trim();
  if (!text) {
    alert("Please paste or select email text first.");
    return;
  }

  // show loading text
  document.getElementById("labelList").innerText = "Classifying...";
  document.getElementById("cadList").innerText = "Checking...";

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text })
    });

    if (!res.ok) throw new Error("Server error: " + res.status);

    const data = await res.json();

    // Backend now returns labels as a STRING
    const labelString = data.labels || "";

    // Show label string directly
    document.getElementById("labelList").innerText =
      labelString.trim() !== "" ? labelString : "None";

    // CAD URLs (list)
    const cadUrls = data.cad_urls || [];

    if (cadUrls.length > 0) {
      const frag = document.createDocumentFragment();

      cadUrls.forEach(url => {
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.innerText = url;
        a.style.display = "block";
        frag.appendChild(a);
      });

      const cadListEl = document.getElementById("cadList");
      cadListEl.innerHTML = "";
      cadListEl.appendChild(frag);
    } else {
      document.getElementById("cadList").innerText = "None";
    }

  } catch (err) {
    console.error(err);
    document.getElementById("labelList").innerText = "Error";
    document.getElementById("cadList").innerText = "Error";
    alert("Error contacting backend: " + err.message);
  }
});
