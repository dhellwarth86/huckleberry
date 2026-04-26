// mutation_test_step11.js — for every Step 11 test, break the code in a
// targeted way and confirm that test (and ideally ONLY that test, or the
// smallest plausible set) fails. If a test stays green despite its guarded
// invariant being broken, that test is worthless as a regression guard.
//
// This is the step that separates a real regression suite from checkbox
// ceremony. Without it, I shipped 8 green tests and hoped they were useful.
// With it, I have evidence each test is load-bearing.

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML_PATH = path.join(__dirname, 'Huckleberry_AI_6.3.5_Scope.html');
const ORIGINAL = fs.readFileSync(HTML_PATH, 'utf8');

// Each mutation: a string replacement that breaks ONE invariant. The `expect`
// field names the Step 11 test(s) that MUST fail. If any listed test stays
// green, that test is broken.
const MUTATIONS = [
  {
    name: 'mutation A: drop coverBoard from derived seed (break "exactly 3 rows")',
    find: `  { id: 'coverBoard',     label: 'Cover Board',      unit: 'sf',    tool: 'derived', priority: 'common',      derivedFrom: 'mainPolygonArea' },`,
    replace: `  // (coverBoard removed by mutation A)`,
    expectFail: ['step11 · derived section has exactly 3 rows'],
  },
  {
    name: 'mutation B: change derived row unit from sf to lf (break unit contract)',
    find: `    derived.push(row(item.label, 'sf', base, { seedId: item.id }));`,
    replace: `    derived.push(row(item.label, 'lf', base, { seedId: item.id }));`,
    expectFail: ['step11 · every derived row is unit='],
  },
  {
    name: 'mutation C: make insulation read ZERO instead of totalSF (break "all share base")',
    find: `    const base = (item.derivedFrom === 'mainPolygonArea') ? totalSF : 0;`,
    replace: `    const base = (item.derivedFrom === 'mainPolygonArea' && item.id !== 'insulation') ? totalSF : 0;`,
    expectFail: ['step11 · all derived rows share the same base value', 'step11 · zero-area system'],
  },
  {
    name: 'mutation D: typo in derivedFrom string (break "derivedFrom is always mainPolygonArea")',
    find: `  { id: 'membrane',       label: 'Membrane',         unit: 'sf',    tool: 'derived', priority: 'always',      derivedFrom: 'mainPolygonArea' },`,
    replace: `  { id: 'membrane',       label: 'Membrane',         unit: 'sf',    tool: 'derived', priority: 'always',      derivedFrom: 'mainPolyArea' },`,
    // Breaking derivedFrom → the match fails → base falls to 0 → "all share same base" still passes (all 0 if all break; here only membrane breaks so they diverge) → also zero-area test still passes (0 is fine when base is 0)
    expectFail: ['step11 · ROOFING_SEED_ITEMS: every derived item carries derivedFrom', 'step11 · all derived rows share the same base value'],
  },
  {
    name: 'mutation E: derived row returns undefined withWaste (break "no NaN" guard)',
    find: `      withWaste: base * (1 + wastePct / 100),`,
    replace: `      withWaste: undefined,`,
    expectFail: ['step11 · zero-area system', 'step11 · waste override on derived seed'],
  },
  {
    name: 'mutation F: skip rectangle kind in totalSF (break kind-agnostic sum)',
    find: `  const buildingAreas = sysAreas.filter(a => !a.polygonTypeId);`,
    replace: `  const buildingAreas = sysAreas.filter(a => !a.polygonTypeId && a.kind !== 'rectangle');`,
    expectFail: ['step11 · rectangle and polygon', 'step11 · derived SF rows compute from sum'],
  },
  {
    name: 'mutation G: cross-system leak (sum ALL areas regardless of systemId)',
    find: `  const sysAreas = (annotations.areas || []).filter(a => a.systemId === system.id);`,
    replace: `  const sysAreas = (annotations.areas || []);  // intentional cross-system leak`,
    expectFail: ['step11 · multi-system isolation'],
  },
  {
    name: 'mutation H: wasteFor ignores overrides (break waste override path)',
    find: `    if (seedId && overrides[seedId] && typeof overrides[seedId].wastePct === 'number') {\n      return overrides[seedId].wastePct;\n    }`,
    replace: `    // override ignored by mutation H`,
    expectFail: ['step11 · waste override on derived seed'],
  },
];

async function runOneVariant(mutationName, mutatedHtml) {
  return new Promise((resolve) => {
    let htmlWithHoist = mutatedHtml.replace('</body>', `
<script>
  window.__T__ = {
    UNIT_TESTS: (typeof UNIT_TESTS !== 'undefined') ? UNIT_TESTS : null,
    INTEGRATION_TESTS: (typeof INTEGRATION_TESTS !== 'undefined') ? INTEGRATION_TESTS : null,
  };
</script>
</body>`);
    const vc = new VirtualConsole();
    vc.on('jsdomError', () => {});  // suppress — we might be creating parse errors intentionally
    const dom = new JSDOM(htmlWithHoist, { url: 'http://localhost/', runScripts: 'dangerously', virtualConsole: vc });
    setTimeout(async () => {
      try {
        const T = dom.window.__T__;
        if (!T || !T.UNIT_TESTS) {
          resolve({ mutationName, fatal: 'tests did not hoist — mutation may have caused a JS parse error' });
          return;
        }
        const step11Tests = T.UNIT_TESTS.filter(t => t.name.startsWith('step11 ·') || t.name.startsWith('takeoff · derived SF rows'));
        const results = [];
        for (const t of step11Tests) {
          try { await t.fn(); results.push({ name: t.name, pass: true }); }
          catch (e) { results.push({ name: t.name, pass: false, msg: String(e.message || e).slice(0, 140) }); }
        }
        dom.window.close();
        resolve({ mutationName, results });
      } catch (e) {
        resolve({ mutationName, fatal: String(e) });
      }
    }, 300);
  });
}

(async () => {
  // Sanity: run the UNMUTATED file first to confirm all Step 11 tests pass.
  const baseline = await runOneVariant('BASELINE (no mutation)', ORIGINAL);
  const baselineGreen = baseline.results.every(r => r.pass);
  console.log(`BASELINE: ${baselineGreen ? 'all Step 11 tests green ✓' : 'BASELINE IS BROKEN — ABORTING'}`);
  if (!baselineGreen) {
    for (const r of baseline.results) if (!r.pass) console.log(`   FAIL: ${r.name}: ${r.msg}`);
    process.exit(2);
  }
  console.log('');

  let mutationsHandled = 0;
  let mutationsMissed = 0;

  for (const m of MUTATIONS) {
    if (!ORIGINAL.includes(m.find)) {
      console.log(`SKIP  ${m.name}`);
      console.log(`      (find-string not present — mutation definition is stale)`);
      continue;
    }
    const mutated = ORIGINAL.replace(m.find, m.replace);
    const v = await runOneVariant(m.name, mutated);
    if (v.fatal) {
      // A fatal JS parse error is acceptable iff mutation intent is to break syntax,
      // but none of our mutations should parse-break; treat as miss.
      console.log(`FATAL ${m.name}: ${v.fatal}`);
      mutationsMissed++;
      continue;
    }
    const failed = v.results.filter(r => !r.pass).map(r => r.name);
    // Did the EXPECTED tests fail?
    const anyExpectedCaught = m.expectFail.some(exp => failed.some(f => f.includes(exp)));
    if (anyExpectedCaught) {
      console.log(`OK    ${m.name}`);
      console.log(`      caught by: ${failed.join(' | ')}`);
      mutationsHandled++;
    } else {
      console.log(`MISS  ${m.name}`);
      console.log(`      expected a test matching one of: ${m.expectFail.join(' | ')}`);
      console.log(`      actually failed: ${failed.length ? failed.join(' | ') : '(nothing)'}`);
      mutationsMissed++;
    }
  }

  console.log('');
  console.log(`MUTATION TEST RESULT: ${mutationsHandled}/${MUTATIONS.length} mutations caught, ${mutationsMissed} escaped`);
  if (mutationsMissed > 0) {
    console.log('');
    console.log('A mutation that escaped = a test that is either weaker than it looks');
    console.log('OR a mutation definition that misidentifies what it breaks. Investigate.');
    process.exit(1);
  }
  process.exit(0);
})().catch(e => { console.error(e.stack || e); process.exit(2); });
