
const form = document.getElementById('weather-form');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  resultDiv.textContent = 'Predicting...';

  const data = {
    temperature: parseFloat(form.temperature.value),
    humidity: parseFloat(form.humidity.value),
    pressure: parseFloat(form.pressure.value),
    wind_speed: parseFloat(form.wind_speed.value)
  };

  try {
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!resp.ok) {
      const txt = await resp.text();
      resultDiv.textContent = 'Error: ' + txt;
      return;
    }
    const json = await resp.json();
    // build friendly display
    let html = '<h3>Predictions</h3><ul>';
    for (const [label, info] of Object.entries(json)) {
      const yesno = info.pred ? 'Yes' : 'No';
      const prob = (info.prob * 100).toFixed(1) + '%';
      html += `<li><strong>${label}</strong>: ${yesno} (prob: ${prob})</li>`;
    }
    html += '</ul>';
    resultDiv.innerHTML = html;
  } catch (err) {
    resultDiv.textContent = 'Network error or backend not running. Start the backend (see README).';
  }
});
