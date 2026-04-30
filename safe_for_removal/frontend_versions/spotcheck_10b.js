// spotcheck_10b.js — exact reproduction of the user's Chipotle workflow that
// produced the triangle-with-shifted-bottom bug. Simulates:
//   1. A 4-corner rectangle drawn at realistic PDF-point coordinates
//   2. onMove between each click (mimicking mouse motion)
//   3. snap-close click near the first vertex
// Confirms the saved area has 4 distinct corner vertices (not 3, not self-intersecting).

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML_PATH = path.join(__dirname, 'Huckleberry_AI_6.3.4_Scope.html');
let html = fs.readFileSync(HTML_PATH, 'utf8');
html = html.replace('</body>', `
<script>
  window.__EXT__ = {
    App, Viewer, TOOL_HANDLERS,
    seedSystem, makeScopeSystem, persistAreaFromPoints,
  };
</script>
</body>`);

const vc = new VirtualConsole();
vc.on('jsdomError', (err) => process.stderr.write('[jsdomError] ' + err.message + '\n'));
const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: vc });
const { window } = dom;
window.prompt = () => 'Building 1';

(async () => {
  await new Promise(r => setTimeout(r, 300));
  const { App, Viewer, TOOL_HANDLERS, seedSystem, makeScopeSystem } = window.__EXT__;

  const sys = seedSystem(makeScopeSystem('ChipoleRepro', ''));
  App.project.scope = { systems: [sys], rawText: '', lastScanAt: 0 };
  App.project.annotations = { byPage: {}, areas: [], pins: [], lineSegments: [] };
  App.currentSystemId = sys.id;
  Viewer.currentPage = 0;
  App.manualScale = 4.0;     // Chipotle's 1" = 4' scale
  App.activePolygonTypeId = null;
  Viewer.tempState = null;

  // Realistic rectangle at ~Chipotle-plan coordinates. PDF points.
  const TL = { x:  370, y: 290 };
  const TR = { x: 1260, y: 290 };
  const BR = { x: 1260, y: 780 };
  const BL = { x:  370, y: 780 };

  const h = TOOL_HANDLERS.polygon;

  // Simulate browser mouse flow: several onMoves between each onDown (because
  // real browsers fire mousemove continuously at ~60Hz).
  h.onDown(TL);
  h.onMove({x: 400, y: 290}); h.onMove({x: 800, y: 290}); h.onMove({x: 1200, y: 290});
  h.onDown(TR);
  h.onMove({x: 1260, y: 400}); h.onMove({x: 1260, y: 600});
  h.onDown(BR);
  h.onMove({x: 1000, y: 780}); h.onMove({x: 600, y: 780});
  h.onDown(BL);
  h.onMove({x: 370, y: 600}); h.onMove({x: 370, y: 400}); h.onMove({x: 375, y: 295});
  // Snap-close click near TL (within snapTolPx=12)
  h.onDown({ x: 373, y: 293 });

  const areas = App.project.annotations.areas;
  const checks = [
    { label: 'exactly 1 area persisted', actual: areas.length, expected: 1 },
    { label: 'polygon has exactly 4 vertices', actual: areas[0] && areas[0].pointsPt.length, expected: 4 },
    { label: 'vertex 0 is TL', actual: JSON.stringify(areas[0] && areas[0].pointsPt[0]), expected: JSON.stringify(TL) },
    { label: 'vertex 1 is TR', actual: JSON.stringify(areas[0] && areas[0].pointsPt[1]), expected: JSON.stringify(TR) },
    { label: 'vertex 2 is BR', actual: JSON.stringify(areas[0] && areas[0].pointsPt[2]), expected: JSON.stringify(BR) },
    { label: 'vertex 3 is BL', actual: JSON.stringify(areas[0] && areas[0].pointsPt[3]), expected: JSON.stringify(BL) },
  ];

  // And the sqft should be a sensible rectangle area.
  // Rectangle 890pt × 490pt at scale 4 ft/in: (890/72)*4 × (490/72)*4 ≈ 49.4 × 27.2 ≈ 1345 sqft
  const sqft = areas[0] && areas[0].sqft;
  const expectedSqft = (890/72 * 4) * (490/72 * 4);
  checks.push({
    label: `sqft ≈ ${expectedSqft.toFixed(0)} (rectangle area math)`,
    actual: sqft && sqft.toFixed(0),
    expected: expectedSqft.toFixed(0),
  });

  let pass = 0, fail = 0;
  for (const c of checks) {
    const ok = c.actual == c.expected;
    console.log(`${ok ? 'OK  ' : 'FAIL'}  ${c.label}`);
    if (!ok) {
      console.log(`         expected: ${c.expected}`);
      console.log(`         got:      ${c.actual}`);
    }
    if (ok) pass++; else fail++;
  }
  console.log('');
  console.log(`RESULT: ${pass}/${pass+fail} passed`);
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error(e.stack || e); process.exit(2); });
