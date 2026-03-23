() => {
  const t = document.body.innerText || '';
  const income = t.match(/Total\s+(?:for\s+)?Income[\s\S]{0,20}\$([\d,.]+)/i)?.[1] || t.match(/Gross\s+(?:for\s+)?Income[\s\S]{0,20}\$([\d,.]+)/i)?.[1] || 'N/A';
  const expenses = t.match(/Total\s+(?:for\s+)?Expenses[\s\S]{0,20}\$([\d,.]+)/i)?.[1] || 'N/A';
  const net = t.match(/Net\s+(?:Income|Operating\s+Income|Profit)[\s\S]{0,20}\$?([\-]?[\d,.]+)/i)?.[1] || 'N/A';
  const neg = t.includes('-$') || /Net\s+(?:Income|Profit).*-/.test(t);
  const cogs = t.match(/Cost\s+of\s+Goods\s+Sold[\s\S]{0,20}\$([\d,.]+)/i)?.[1] || null;
  return JSON.stringify({income, expenses, net, cogs, negative: !!neg, title: document.title.substring(0,60)});
}
