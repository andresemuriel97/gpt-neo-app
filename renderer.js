const btn = document.getElementById('send');
const promptEl = document.getElementById('prompt');
const outputEl = document.getElementById('output');

btn.addEventListener('click', async () => {
  const prompt = promptEl.value;
  outputEl.textContent = 'Generando…';
  try {
    const resp = await fetch('http://127.0.0.1:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    const { text } = await resp.json();
    outputEl.textContent = text;
  } catch (err) {
    outputEl.textContent = 'Error: ' + err.message;
  }
});