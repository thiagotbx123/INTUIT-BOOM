() => {
  const t = document.body.innerText || '';
  const count = t.match(/(\d[\d,]*)\s*(?:results|customers|vendors|employees|items)/i)?.[1] || '0';
  const rows = t.match(/^.{3,60}$/gm)?.filter(l => !l.match(/Home|Feed|Create|Bookmarks|Skip/))?.slice(0, 8) || [];
  const hasPH = /\b(TBX|Test|TESTER|Lorem|Sample|Foo)\b/i.test(t);
  return JSON.stringify({count, first8: rows, hasPlaceholder: hasPH, has404: /not found|404/i.test(t)});
}
