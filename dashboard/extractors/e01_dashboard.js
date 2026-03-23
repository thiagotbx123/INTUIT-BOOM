() => {
  const t = document.body.innerText || '';
  const co = document.querySelector('[class*="company"]')?.innerText || t.match(/^.*LLC|^.*Inc|^.*Corp/m)?.[0] || '';
  const nums = t.match(/\$[\d,.]+[KMB]?/g)?.slice(0, 8) || [];
  return JSON.stringify({co: co.substring(0,80), nums, has404: /not found|404/i.test(t), hasTBX: /\bTBX\b/.test(t)});
}
