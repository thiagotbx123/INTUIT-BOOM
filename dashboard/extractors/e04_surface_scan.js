() => {
  const t = document.body.innerText || '';
  const lines = t.split('\n').filter(l => l.trim().length > 2);
  return JSON.stringify({
    title: document.title.substring(0,50),
    lines: lines.length,
    hasData: lines.length > 10,
    has404: /not found|404|page doesn't exist/i.test(t),
    hasPH: /\b(TBX|Lorem|Foo|TODO|Sample|Dummy|Fake|Temp|tmp)\b/i.test(t) || /\b(test\s*\d|test[_\-\s]\w|testing\b|tester\b|IDT\b|demo\s*[\d.]|example\s+proj)/i.test(t) || /\bTest[A-Z]\w/.test(t),
    first5: lines.slice(2, 7).map(l => l.substring(0, 60))
  });
}
