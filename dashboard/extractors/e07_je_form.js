() => {
  const inputs = [...document.querySelectorAll('input[type="text"], input[type="number"], textarea')];
  const vals = inputs.slice(0, 10).map(i => ({id: i.id?.substring(0,30), val: i.value?.substring(0,30), ph: i.placeholder?.substring(0,20)}));
  const saveBtn = !!document.querySelector('[data-automation-id*="save"], button[class*="save"]');
  return JSON.stringify({fields: vals, saveVisible: saveBtn});
}
