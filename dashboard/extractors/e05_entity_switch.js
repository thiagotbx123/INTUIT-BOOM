() => {
  const t = (document.body.innerText || '').substring(0, 300);
  return JSON.stringify({
    url: window.location.href.substring(0, 80),
    company: t.match(/^.*(?:LLC|Inc|Corp|Ltd|Group|Solutions|Outfitters|Tire|Retail)/m)?.[0]?.substring(0, 60) || 'unknown',
    loaded: !(/loading|please wait/i.test(t))
  });
}
