async function loadWatchlist() {
  const response = await fetch('./data/sample-watchlist.json');
  return response.json();
}

function diffSummary(item) {
  const signals = [];
  if (item.lastTitle !== item.currentTitle) signals.push('homepage/title positioning changed');
  if (item.lastMeta !== item.currentMeta) signals.push('offer/meta messaging changed');
  if (item.currentReviewRating < item.lastReviewRating - 0.2) signals.push('review rating dropped');
  if (item.currentReviewCount > item.lastReviewCount + 10) signals.push('review volume spiked');
  if (item.currentHiring > item.lastHiring) signals.push('hiring activity increased');
  return signals;
}

function salesAngle(item, signals) {
  if (signals.includes('review rating dropped')) {
    return `Reputation issue: ${item.company} fell from ${item.lastReviewRating}★ to ${item.currentReviewRating}★. Good opening for review recovery, CX, or lead-conversion help.`;
  }
  if (signals.includes('hiring activity increased')) {
    return `Growth signal: ${item.company} is hiring (${item.lastHiring} → ${item.currentHiring}). Likely investing in demand capture or operational scale.`;
  }
  if (signals.includes('homepage/title positioning changed') || signals.includes('offer/meta messaging changed')) {
    return `Messaging shift: ${item.company} changed positioning/offers on-site. Good moment to pitch SEO, CRO, paid media, or sales support.`;
  }
  return `Change detected at ${item.company}. Worth a human look.`;
}

function render(items) {
  const tbody = document.getElementById('rows');
  tbody.innerHTML = items.map((item) => {
    const signals = diffSummary(item);
    const angle = salesAngle(item, signals);
    return `<tr>
      <td><strong>${item.company}</strong><br><span class="muted">${item.category}</span></td>
      <td>${signals.map(s => `<div>${s}</div>`).join('') || '<div>No major change</div>'}</td>
      <td>${angle}</td>
      <td><button data-company="${item.company}">Save lead</button></td>
    </tr>`;
  }).join('');

  tbody.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      const company = button.getAttribute('data-company');
      const saved = JSON.parse(localStorage.getItem('signalsift-leads') || '[]');
      saved.push({ company, createdAt: new Date().toISOString() });
      localStorage.setItem('signalsift-leads', JSON.stringify(saved));
      button.textContent = 'Saved';
      button.disabled = true;
    });
  });
}

loadWatchlist().then(render);
