() => {
  const t = document.body.innerText || '';
  const lines = t.split('\n').filter(l => l.trim().length > 2);
  const is404 = /not found|404|page doesn't exist|we can't find/i.test(t);
  const isEmpty = lines.length < 5;
  const hasPH = /\b(TBX|Lorem|Foo|TODO|Test Company)\b/i.test(t);
  const hasData = lines.length > 10 && !is404;
  return JSON.stringify({
    status: is404 ? 'X' : isEmpty ? 'EMPTY' : hasPH ? 'WARN' : 'OK',
    lines: lines.length,
    title: document.title.substring(0, 40),
    snippet: lines.slice(2, 5).map(l => l.substring(0, 40)).join(' | ')
  });
}
