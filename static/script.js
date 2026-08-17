const form = document.querySelector('#predict-form');
const result = document.querySelector('#result');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = form.querySelector('button');
  button.disabled = true;
  button.textContent = 'Analizando...';
  result.hidden = true;

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        subject: document.querySelector('#subject').value,
        body: document.querySelector('#body').value,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The email could not be analyzed.');
    result.className = `result ${data.label === 'SPAM' ? 'spam' : ''}`;
    result.innerHTML = `<strong>${data.label}</strong><span>${data.message}</span><br><span>Confidence: ${data.confidence}%</span>`;
  } catch (error) {
    result.className = 'result spam';
    result.innerHTML = `<strong>Error</strong><span>${error.message}</span>`;
  } finally {
    result.hidden = false;
    button.disabled = false;
    button.innerHTML = 'Analyze email <span>→</span>';
  }
});
