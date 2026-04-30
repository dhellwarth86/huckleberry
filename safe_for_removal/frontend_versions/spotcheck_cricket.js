// spotcheck_cricket.js — realistic cricket-on-TPO scenario, end-to-end.
// Confirms that:
//   - cricket tagged areas feed sf.cricket
//   - building area feeds derived membrane / insulation / cover board
//   - the two NEVER cross-contaminate

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML_PATH = path.join(__dirname, 'Huckleberry_AI_6.3.3_Scope.html');
let html = fs.readFileSync(HTML_PATH, 'utf8');

html = html.replace('</body>', `
<script>
  window.__EXT__ = {
    App, Viewer, TOOL_HANDLERS,
    seedSystem, makeScopeSystem, buildTakeoffModel,
    viewerSetActivePolygon, persistAreaFromPoints,
    ROOFING_SEED_ITEMS, ROOFING_CONSTANTS,
  };
</script>
</body>`);

const vc = new VirtualConsole();
vc.on('jsdomError', (err) => process.stderr.write('[jsdomError] ' + err.message + '\\n'));

const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: vc });
const { window } = dom;
window.prompt = () => 'Building 1';  // for the one building-area prompt

(async () => {
  await new Promise(r => setTimeout(r, 300));
  const X = window.__EXT__;
  if (!X || !X.App) { console.error('hoist failed'); process.exit(2); }

  const { App, Viewer, seedSystem, makeScopeSystem, buildTakeoffModel,
          viewerSetActivePolygon, persistAreaFromPoints } = X;

  // Scenario: a 5,000 sqft TPO roof with two crickets (one 25 sf, one 40 sf)
  // on the high sides of two RTU curbs. At scale 1 ft/in (1"=1'), 72pt = 1ft.
  const sys = seedSystem(makeScopeSystem('TPO_MA', ''));
  App.project.scope = { systems: [sys], rawText: '', lastScanAt: 0 };
  App.project.annotations = { byPage: {}, areas: [], pins: [], lineSegments: [] };
  App.currentSystemId = sys.id;
  Viewer.currentPage = 0;
  App.manualScale = 1.0;

  const cricket = sys.polygonTypes.find(p => p.seedId === 'cricket');
  if (!cricket) { console.log('FAIL: cricket not seeded'); process.exit(1); }

  // Helper — build a rect at scale-1 that yields a given sqft
  function rectForSqft(targetSqft) {
    const side = Math.sqrt(targetSqft) * 72; // pt per ft = 72 at scale 1
    return [
      {x:0, y:0},
      {x:side, y:0},
      {x:side, y:side},
      {x:0, y:side},
    ];
  }

  // Step A: draw building area (untagged polygon) — 5000 sqft
  App.activePolygonTypeId = null;
  persistAreaFromPoints('polygon', rectForSqft(5000));

  // Step B: flip to cricket, draw two crickets
  viewerSetActivePolygon(cricket.id);
  persistAreaFromPoints('polygon', rectForSqft(25));
  persistAreaFromPoints('polygon', rectForSqft(40));

  // --- Verify state ---
  const areas = App.project.annotations.areas;
  console.log(`Areas persisted: ${areas.length}`);
  for (const a of areas) {
    const tag = a.polygonTypeId ? `cricket (${a.name})` : `building (${a.name})`;
    console.log(`  [${tag}]  ${a.sqft.toFixed(1)} sqft`);
  }

  const model = buildTakeoffModel(sys, App.project.annotations);
  const cricketRow = model.sf.find(r => r.seedId === 'cricket');
  const membrane = model.derived.find(r => r.seedId === 'membrane');
  const insulation = model.derived.find(r => r.seedId === 'insulation');

  const checks = [
    { label: 'cricket SF base', actual: cricketRow && cricketRow.base, expected: 65, tol: 0.1 },
    { label: 'cricket SF with 10% waste', actual: cricketRow && cricketRow.withWaste, expected: 71.5, tol: 0.1 },
    { label: 'membrane derived SF (building only, cricket excluded)', actual: membrane && membrane.base, expected: 5000, tol: 0.5 },
    { label: 'insulation derived SF (building only)', actual: insulation && insulation.base, expected: 5000, tol: 0.5 },
  ];

  let pass = 0, fail = 0;
  for (const c of checks) {
    const ok = c.actual != null && Math.abs(c.actual - c.expected) <= c.tol;
    console.log(`${ok ? 'OK  ' : 'FAIL'}  ${c.label}: expected=${c.expected}, got=${c.actual}`);
    if (ok) pass++; else fail++;
  }
  console.log('');
  console.log(`RESULT: ${pass}/${pass+fail} passed`);
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error(e.stack || e); process.exit(2); });
