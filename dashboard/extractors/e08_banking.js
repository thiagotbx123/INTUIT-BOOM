() => {
  const rows = [...document.querySelectorAll('tr, [role="row"]')].filter(r => {
    const t = r.innerText || '';
    return t.includes('Categorize') || t.includes('Match');
  });
  const txns = rows.slice(0, 10).map((r, i) => {
    const cells = [...r.querySelectorAll('td, [role="cell"], [role="gridcell"], div[class*="cell"]')];
    if (cells.length < 3) return null;
    return {
      idx: i,
      date: (cells[1]?.innerText || '').substring(0, 12),
      desc: (cells[2]?.innerText || '').substring(0, 40),
      amount: (cells[3]?.innerText || cells[4]?.innerText || '').substring(0, 15),
      account: (cells[5]?.innerText || cells[6]?.innerText || '').split('\n')[0]?.substring(0, 40) || '',
      vendor: (cells[7]?.innerText || '').substring(0, 30),
      hasPost: !!(r.querySelector('button') && [...r.querySelectorAll('button')].find(b => b.innerText?.trim() === 'Post'))
    };
  }).filter(Boolean);
  const pending = document.body.innerText.match(/(\d+)\s*(?:for review|pending|uncategorized)/i)?.[1] || '?';
  return JSON.stringify({pending, txnCount: txns.length, txns});
}
