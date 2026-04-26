// spotcheck_durolast.js — exercises Duro-Last + TPO + PVC against the real
// CLAUDE.md bidset strings (Panda Express, Taco Bell) to confirm the new
// vocab entry doesn't regress neighbors.

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML_PATH = path.join(__dirname, 'Huckleberry_AI_6.3.1_Scope.html');
let html = fs.readFileSync(HTML_PATH, 'utf8');

html = html.replace('</body>', `
<script>
  window.__EXT__ = {
    extractScope: (typeof extractScope !== 'undefined') ? extractScope : null,
    ROOF_VOCAB: (typeof ROOF_VOCAB !== 'undefined') ? ROOF_VOCAB : null,
  };
</script>
</body>`);

const vc = new VirtualConsole();
vc.on('jsdomError', (err) => process.stderr.write('[jsdomError] ' + err.message + '\n'));

const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: vc });
const { window } = dom;

(async () => {
  await new Promise(r => setTimeout(r, 300));
  const { extractScope } = window.__EXT__;
  if (!extractScope) { console.error('extractScope not hoisted'); process.exit(2); }

  const cases = [
    // Real CLAUDE.md phrasing
    { label: 'Panda Express Margate',
      text: 'Membrane: Duro-Last 40-mil PVC, mechanically fastened',
      expect: 'Duro-Last' },
    { label: 'Taco Bell Weeki Wachee',
      text: 'Duro-Last 40-mil PVC Class C fully adhered, wood framing',
      expect: 'Duro-Last' },
    { label: 'AutoZone-style misspelling',
      text: 'Roof: Duralast 50-mil PVC, fully adhered.',
      expect: 'Duro-Last' },
    { label: 'Plain TPO (regression)',
      text: 'TPO roof, 60 mil, fully adhered.',
      expect: 'TPO' },
    { label: 'Plain PVC (regression)',
      text: 'PVC roof membrane, 50 mil, mechanically attached.',
      expect: 'PVC' },
    { label: 'Plain EPDM (regression)',
      text: 'EPDM ballasted roof system.',
      expect: 'EPDM' },
    { label: 'No-hyphen variant',
      text: 'DuroLast 40-mil, fully adhered.',
      expect: 'Duro-Last' },
    { label: 'Spaced variant',
      text: 'Duro Last membrane system.',
      expect: 'Duro-Last' },
  ];

  let pass = 0, fail = 0;
  for (const c of cases) {
    const planSet = { pages: [{ idx: 0, texts: [{ text: c.text }] }] };
    const scope = extractScope(planSet);
    const got = scope.systems[0] && scope.systems[0].systemType;
    const ok = got === c.expect;
    console.log(`${ok ? 'OK  ' : 'FAIL'}  ${c.label}: expected=${c.expect}, got=${got}`);
    if (ok) pass++; else fail++;
  }
  console.log('');
  console.log(`RESULT: ${pass}/${pass+fail} passed`);
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
