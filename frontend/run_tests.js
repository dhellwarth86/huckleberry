// run_tests.js — jsdom 29 harness
// Inline `const` declarations don't attach to window. We inject a hoist script before
// </body> that runs in the same scope and pushes what we need onto window.

const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const HTML_PATH = process.argv[2] || path.join(__dirname, 'extracted/Huckleberry_AI_6.3.0_Scope.html');
console.log(`[harness] loading ${HTML_PATH}`);

let html = fs.readFileSync(HTML_PATH, 'utf8');

const hoistScript = `
<script>
  try {
    window.__TESTS__ = {
      UNIT_TESTS: (typeof UNIT_TESTS !== 'undefined') ? UNIT_TESTS : null,
      INTEGRATION_TESTS: (typeof INTEGRATION_TESTS !== 'undefined') ? INTEGRATION_TESTS : null,
    };
    window.__HOIST_OK__ = true;
  } catch (e) {
    window.__HOIST_ERR__ = String(e && e.message || e);
  }
</script>
`;
if (html.indexOf('</body>') === -1) {
  console.error('[harness] FATAL: no </body> found in HTML');
  process.exit(2);
}
html = html.replace('</body>', hoistScript + '</body>');

const vc = new VirtualConsole();
vc.on('jsdomError', (err) => {
  process.stderr.write('[jsdomError] ' + (err && err.message ? err.message : String(err)) + '\n');
  if (err && err.detail) process.stderr.write('  detail: ' + (err.detail.message || err.detail) + '\n');
});

const dom = new JSDOM(html, {
  url: 'http://localhost/test.html',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  virtualConsole: vc,
});

const { window } = dom;

if (!window.performance) window.performance = { now: () => Date.now() };
if (!window.requestAnimationFrame) {
  window.requestAnimationFrame = (cb) => setTimeout(cb, 0);
  window.cancelAnimationFrame = (id) => clearTimeout(id);
}

(async function main() {
  await new Promise(r => setTimeout(r, 400));

  if (window.__HOIST_ERR__) {
    console.error('[harness] hoist script errored:', window.__HOIST_ERR__);
    process.exit(2);
  }
  if (!window.__HOIST_OK__) {
    console.error('[harness] hoist script never ran — inline scripts aborted early');
    process.exit(2);
  }

  const T = window.__TESTS__;
  if (!T.UNIT_TESTS || !T.INTEGRATION_TESTS) {
    console.error('[harness] FATAL: UNIT_TESTS / INTEGRATION_TESTS not hoisted');
    console.error('  __TESTS__ keys:', Object.keys(T));
    process.exit(2);
  }

  const { UNIT_TESTS, INTEGRATION_TESTS } = T;
  console.log(`[harness] UNIT_TESTS: ${UNIT_TESTS.length} | INTEGRATION_TESTS: ${INTEGRATION_TESTS.length} | total: ${UNIT_TESTS.length + INTEGRATION_TESTS.length}`);
  console.log('');

  let pass = 0, fail = 0;
  const failures = [];

  async function runOne(t, kind) {
    try {
      await t.fn();
      pass++;
    } catch (e) {
      fail++;
      failures.push({ kind, name: t.name, message: String(e && e.message || e) });
      console.log(`  FAIL  [${kind}]  ${t.name}\n        -> ${String(e && e.message || e)}`);
    }
  }

  for (const t of UNIT_TESTS)        await runOne(t, 'UNIT');
  for (const t of INTEGRATION_TESTS) await runOne(t, 'INTEG');

  const total = pass + fail;
  console.log('');
  console.log(`[harness] RESULT: ${pass}/${total} passed, ${fail} failed`);
  if (fail > 0) {
    console.log('[harness] FAILURES SUMMARY:');
    for (const f of failures) console.log(`   - [${f.kind}] ${f.name}`);
    process.exit(1);
  }
  process.exit(0);
})().catch(e => {
  console.error('[harness] uncaught:', e && e.stack || e);
  process.exit(2);
});
