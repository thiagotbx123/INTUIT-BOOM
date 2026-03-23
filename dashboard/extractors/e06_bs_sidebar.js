() => {
  const links = [...document.querySelectorAll('a, button')];
  const bsLink = links.find(l => /balance.?sheet/i.test(l.innerText));
  const reports = links.filter(l => /profit|loss|aging|cash.?flow|balance/i.test(l.innerText)).map(l => l.innerText.substring(0,40));
  return JSON.stringify({bsLink: bsLink?.innerText?.substring(0,50) || null, bsHref: bsLink?.href?.substring(0,120) || null, reports});
}
