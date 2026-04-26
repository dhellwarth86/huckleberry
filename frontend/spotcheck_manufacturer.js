// spotcheck_manufacturer.js — exercises the new sys.manufacturer + fallback
// against real-world bidset strings from CLAUDE.md + regression cases.

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML_PATH = path.join(__dirname, 'Huckleberry_AI_6.3.2_Scope.html');
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
    // --- REAL CLAUDE.md bidset strings (Duro-Last) ---
    { label: 'Panda Express Margate (real)',
      text: 'Membrane: Duro-Last 40-mil PVC, mechanically fastened',
      expectMfr: 'Duro-Last', expectSys: 'PVC' },
    { label: 'Taco Bell Weeki Wachee (real)',
      text: 'Duro-Last 40-mil PVC Class C fully adhered, wood framing',
      expectMfr: 'Duro-Last', expectSys: 'PVC' },
    { label: 'AutoZone-style misspelling',
      text: 'Roof: Duralast 50-mil PVC, fully adhered.',
      expectMfr: 'Duro-Last', expectSys: 'PVC' },
    { label: 'No-hyphen variant',
      text: 'DuroLast 40-mil, fully adhered.',
      expectMfr: 'Duro-Last', expectSys: 'PVC' },

    // --- Other manufacturers ---
    { label: 'Sika Sarnafil (PVC specialist)',
      text: 'Sika Sarnafil PVC 60 mil membrane',
      expectMfr: 'Sika Sarnafil', expectSys: 'PVC' },
    { label: 'Sarnafil shorthand',
      text: 'Sarnafil membrane, fully adhered',
      expectMfr: 'Sika Sarnafil', expectSys: 'PVC' },
    { label: 'GAF EverGuard TPO',
      text: 'GAF EverGuard TPO 60 mil, fully adhered',
      expectMfr: 'GAF', expectSys: 'TPO' },      // explicit TPO wins over GAF fallback
    { label: 'GAF brand with no chemistry',
      text: 'GAF roofing system throughout',
      expectMfr: 'GAF', expectSys: 'TPO' },      // falls back to GAF.systems[0]
    { label: 'Carlisle Sure-Weld',
      text: 'Carlisle Sure-Weld TPO 60 mil, mechanically attached',
      expectMfr: 'Carlisle', expectSys: 'TPO' },
    { label: 'Firestone RubberGard EPDM',
      text: 'Firestone RubberGard EPDM ballasted',
      expectMfr: 'Firestone', expectSys: 'EPDM' },

    // --- No-mfr regression cases: manufacturer must stay null ---
    { label: 'Plain TPO (no mfr)',
      text: 'TPO roof, 60 mil, fully adhered.',
      expectMfr: null, expectSys: 'TPO' },
    { label: 'Plain PVC (no mfr)',
      text: 'PVC roof membrane, 50 mil, mechanically attached.',
      expectMfr: null, expectSys: 'PVC' },
    { label: 'Plain EPDM (no mfr)',
      text: 'EPDM ballasted roof system.',
      expectMfr: null, expectSys: 'EPDM' },

    // --- Precedence edge case: Duro-Last mentioned but explicit TPO too ---
    { label: 'Spec edge: Duro-Last mentioned but TPO explicit',
      text: 'Alternate: Duro-Last may be substituted for TPO roof system.',
      expectMfr: 'Duro-Last', expectSys: 'TPO' },  // TPO wins (it was detected first via stHits)
  ];

  let pass = 0, fail = 0;
  for (const c of cases) {
    const planSet = { pages: [{ idx: 0, texts: [{ text: c.text }] }] };
    const scope = extractScope(planSet);
    const s = scope.systems[0] || {};
    const mfrOk = s.manufacturer === c.expectMfr;
    const sysOk = s.systemType === c.expectSys;
    const ok = mfrOk && sysOk;
    const marker = ok ? 'OK  ' : 'FAIL';
    console.log(`${marker}  ${c.label}`);
    if (!ok) {
      console.log(`         expected: mfr=${JSON.stringify(c.expectMfr)} sys=${JSON.stringify(c.expectSys)}`);
      console.log(`         got:      mfr=${JSON.stringify(s.manufacturer)} sys=${JSON.stringify(s.systemType)}`);
    }
    if (ok) pass++; else fail++;
  }
  console.log('');
  console.log(`RESULT: ${pass}/${pass+fail} passed`);
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
