document.addEventListener('DOMContentLoaded', function() {
  const emailInput = document.getElementById('email-input');
  const classifyBtn = document.getElementById('classify-btn');
  const categoryDisplay = document.getElementById('category');
  const cadUrlsDisplay = document.getElementById('cad-urls');

  const API_URL = 'http://localhost:5000/classify';  // Backend endpoint

  classifyBtn.addEventListener('click', async () => {
    const text = emailInput.value.trim();
    if (!text) {
      alert('Please enter some text.');
      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      categoryDisplay.textContent = `Category: ${data.category}`;
      cadUrlsDisplay.textContent = `CAD URLs: ${data.cad_urls.join(', ') || 'None detected'}`;
    } catch (error) {
      categoryDisplay.textContent = 'Category: Error';
      cadUrlsDisplay.textContent = `CAD URLs: ${error.message}`;
    }
  });
});