() => {
  const t = document.body.innerText || '';
  const count = t.match(/(\d[\d,]*)\s*(?:results|customers|vendors|employees|items)/i)?.[1] || '0';
  const rows = t.match(/^.{3,60}$/gm)?.filter(l => !l.match(/Home|Feed|Create|Bookmarks|Skip/))?.slice(0, 8) || [];
  const hasPH = /\b(TBX|Lorem|Sample|Foo|Dummy|Fake|Temp|tmp)\b/i.test(t) || /\b(test\s*\d|test[_\-\s]\w|testing\b|tester\b|IDT\b|demo\s*[\d.]|example\s+proj)/i.test(t) || /\bTest[A-Z]\w/.test(t);
  return JSON.stringify({count, first8: rows, hasPlaceholder: hasPH, has404: /not found|404/i.test(t)});
}
