() => {
  const rows = [...document.querySelectorAll('tr')];
  const data = {};
  rows.forEach(r => {
    const text = (r.innerText || '').replace(/\n/g, ' ').trim();
    const match = text.match(/^(Total\s+(?:for\s+)?[\w\s&\/()-]+?)\s+\$?(-?[\d,.]+)/i);
    if (match) data[match[1].trim().substring(0, 50)] = match[2];
  });
  const t = document.body.innerText || '';
  const fallbacks = {
    'AR': t.match(/Accounts\s+Receivable[\s\S]{0,30}\$([\d,.]+)/i)?.[1],
    'AP': t.match(/Accounts\s+Payable[\s\S]{0,30}\$([\d,.]+)/i)?.[1],
    'Bank': t.match(/(?:Total for )?Bank Accounts[\s\S]{0,20}\$([\d,.]+)/i)?.[1],
    'OBE': t.match(/Opening\s+Balance\s+Equity[\s\S]{0,20}\$([\d,.]+)/i)?.[1],
    'Retained': t.match(/Retained\s+Earnings[\s\S]{0,20}\$?(-?[\d,.]+)/i)?.[1],
    'NetIncome': t.match(/Net\s+Income[\s\S]{0,20}\$?(-?[\d,.]+)/i)?.[1]
  };
  const negatives = t.match(/-\$[\d,.]+/g)?.slice(0, 5) || [];
  const period = t.match(/As of[\s\S]{0,30}/i)?.[0]?.substring(0, 40) || 'N/A';
  const totalRows = rows.length;
  return JSON.stringify({totals: data, fallbacks, negatives, period, totalRows});
}
