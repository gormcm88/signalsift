const currency = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

async function loadMarkets() {
  const response = await fetch('../data/sample-markets.json');
  return response.json();
}

function trendWord(value, positiveWord = 'up', negativeWord = 'down') {
  if (value > 0) return positiveWord;
  if (value < 0) return negativeWord;
  return 'flat';
}

function pct(value) {
  const sign = value > 0 ? '+' : '';
  return `${sign}${value.toFixed(1)}%`;
}

function generateNarrative(market, brand = 'LocalSignal AI', audience = 'buyers and sellers', tone = 'professional') {
  const priceDirection = trendWord(market.medianPriceChangeYoY, 'increased', 'declined');
  const invDirection = trendWord(market.inventoryChangeYoY, 'expanded', 'contracted');
  const domDirection = trendWord(market.daysOnMarketChangeYoY, 'slowed', 'sped up');
  const toneLine = {
    professional: 'Here is the clearest story from this month’s housing data.',
    friendly: 'Here’s the plain-English version of what the market is doing right now.',
    punchy: 'The market shifted, and clients will feel it immediately.'
  }[tone] || 'Here is the clearest story from this month’s housing data.';

  const headline = `${market.city} housing market: prices ${priceDirection}, inventory ${invDirection}`;
  const summary = `${toneLine} Median home prices in ${market.city} are ${pct(market.medianPriceChangeYoY)} year over year at ${currency.format(market.medianPrice)}, while inventory is ${pct(market.inventoryChangeYoY)} with ${market.inventoryMonths.toFixed(1)} months of supply. Homes are taking ${market.daysOnMarket} days to sell on average, and the sale-to-list ratio sits at ${market.saleToListRatio.toFixed(1)}%.`;

  const bullets = [
    `Median home price: ${currency.format(market.medianPrice)} (${pct(market.medianPriceChangeYoY)} YoY)`,
    `Median rent: ${currency.format(market.medianRent)} (${pct(market.medianRentChangeYoY)} YoY)`,
    `Inventory: ${market.inventoryMonths.toFixed(1)} months (${pct(market.inventoryChangeYoY)} YoY)`,
    `Days on market: ${market.daysOnMarket} (${pct(market.daysOnMarketChangeYoY)} YoY)`,
    `New listings: ${market.newListings.toLocaleString()} (${pct(market.newListingsChangeYoY)} YoY)`
  ];

  const social = [
    `${market.city} market update: prices are ${pct(market.medianPriceChangeYoY)} YoY and inventory is ${pct(market.inventoryChangeYoY)}. Buyers have more leverage than last year. Want the full breakdown?`,
    `${market.city} agents: the easy take is “market’s weird.” The useful take is this: ${currency.format(market.medianPrice)} median price, ${market.inventoryMonths.toFixed(1)} months inventory, ${market.daysOnMarket} DOM.`,
    `If you’re buying or selling in ${market.city}, this is a market for strategy, not guesswork. Data > vibes.`
  ];

  const newsletter = `Subject: ${market.city} market update for your clients\n\nHi there,\n\nThis month in ${market.city}, median home prices are ${pct(market.medianPriceChangeYoY)} year over year at ${currency.format(market.medianPrice)}. Inventory has ${invDirection} to ${market.inventoryMonths.toFixed(1)} months of supply, and homes are averaging ${market.daysOnMarket} days on market.\n\nWhat this means for ${audience}: ${market.buyerAngle} ${market.sellerAngle}\n\nReply if you want a custom strategy for your move.\n\n- ${brand}`;

  return { headline, summary, bullets, social, newsletter, angles: [market.buyerAngle, market.sellerAngle, market.investorAngle], metadata: { priceDirection, invDirection, domDirection } };
}

function renderReport(market, output) {
  document.getElementById('headline').textContent = output.headline;
  document.getElementById('summary').textContent = output.summary;

  const metrics = document.getElementById('metrics');
  metrics.innerHTML = output.bullets.map(item => `<li>${item}</li>`).join('');

  const angles = document.getElementById('angles');
  angles.innerHTML = output.angles.map(item => `<li>${item}</li>`).join('');

  const social = document.getElementById('social');
  social.innerHTML = output.social.map(item => `<li>${item}</li>`).join('');

  document.getElementById('newsletter').value = output.newsletter;
  document.getElementById('raw-data').textContent = JSON.stringify(market, null, 2);
}

function populateSelect(markets) {
  const select = document.getElementById('market');
  select.innerHTML = markets.map((market, index) => `<option value="${index}">${market.city}, ${market.state}</option>`).join('');
}

async function init() {
  const markets = await loadMarkets();
  populateSelect(markets);

  const form = document.getElementById('generator-form');
  const rerender = () => {
    const market = markets[Number(document.getElementById('market').value)];
    const brand = document.getElementById('brand').value || 'MarketPulse AI';
    const audience = document.getElementById('audience').value || 'buyers and sellers';
    const tone = document.getElementById('tone').value || 'professional';
    const output = generateNarrative(market, brand, audience, tone);
    renderReport(market, output);
  };

  form.addEventListener('input', rerender);
  rerender();
}

init();
