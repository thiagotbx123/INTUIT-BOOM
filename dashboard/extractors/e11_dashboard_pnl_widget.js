() => {
  const result = {widgets: [], currentFilter: null, negative: false};

  // Find the P&L widget region
  const pnlRegion = document.querySelector('[aria-label*="Profit"], region[class*="profit"]')
    || [...document.querySelectorAll('h2')].find(h => /profit.*loss/i.test(h.textContent))?.closest('[class*="widget"], [class*="region"], region');

  if (!pnlRegion) {
    // Fallback: scan full page for P&L widget data
    const t = document.body.innerText || '';
    const netMatch = t.match(/Net profit.*?(?:is\s+)?([\-–]?\$?[\d,.]+)/i);
    const incMatch = t.match(/Income[\s\n]*\$([\d,.]+)/);
    const expMatch = t.match(/Expenses[\s\n]*\$([\d,.]+)/);
    const filterMatch = t.match(/(Last 30 days|This month|This quarter|This year|Last fiscal year)/i);

    result.currentFilter = filterMatch ? filterMatch[1] : 'unknown';
    result.widgets.push({
      filter: result.currentFilter,
      net: netMatch ? netMatch[1] : 'N/A',
      income: incMatch ? '$' + incMatch[1] : 'N/A',
      expenses: expMatch ? '$' + expMatch[1] : 'N/A'
    });
    result.negative = netMatch ? /[\-–]/.test(netMatch[1]) : false;
    return JSON.stringify(result);
  }

  // Extract from the widget region
  const widgetText = pnlRegion.innerText || '';
  const netMatch = widgetText.match(/Net profit.*?(?:is\s+)?([\-–]?\$?[\d,.]+)/i);
  const incMatch = widgetText.match(/Income[\s\n]*\$([\d,.]+)/);
  const expMatch = widgetText.match(/Expenses[\s\n]*\$([\d,.]+)/);
  const filterEl = pnlRegion.querySelector('[role="combobox"]');
  result.currentFilter = filterEl ? filterEl.textContent.trim() : 'unknown';

  result.widgets.push({
    filter: result.currentFilter,
    net: netMatch ? netMatch[1] : 'N/A',
    income: incMatch ? '$' + incMatch[1] : 'N/A',
    expenses: expMatch ? '$' + expMatch[1] : 'N/A'
  });
  result.negative = netMatch ? /[\-–]/.test(netMatch[1]) : false;
  return JSON.stringify(result);
}
