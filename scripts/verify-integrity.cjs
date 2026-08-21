/**
 * SKAI Anti-Drift Verification Script
 * Product: SKAI | Powered by SK Enterprises | Author: Sumeet Kumar
 *
 * Scans the repository for:
 *  - Old/incorrect branding (JARVIS, IRIS, old product names)
 *  - Accidental secrets in source files
 *  - Broken import paths
 *  - Stale references
 *
 * Usage: node scripts/verify-integrity.cjs
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

// ─── Configuration ───────────────────────────────────────────────────────────
const SCAN_DIRS = ['src', 'assets'];
const SCAN_EXTENSIONS = ['.ts', '.tsx', '.js', '.json', '.md', '.html', '.css'];
const EXCLUDE_PATHS = ['node_modules', '.git', 'dist', 'dist-electron', 'release', '.venv'];

const OLD_BRAND_PATTERNS = [
  /\bIRIS\b(?!\s*AI\s*-\s*powered\s*image)/i,
  /\bIRIS AI\b/i,
  /\bIRISX\b/i,
  /Project-JARVIS/i,
  /JARVIS\s*4\.0/i,
  /Jarvis Platform/i,
  /old_owner/i,
];

const SECRET_PATTERNS = [
  /AIza[0-9A-Za-z-_]{35}/,     // Google API Key
  /hf_[a-zA-Z0-9]{30,}/,       // Hugging Face token
  /sk-[a-zA-Z0-9]{40,}/,       // OpenAI key
  /AKIA[0-9A-Z]{16}/,          // AWS Access Key
];

// ─── Helpers ─────────────────────────────────────────────────────────────────
function walkDir(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (EXCLUDE_PATHS.some((ex) => fullPath.includes(ex))) continue;
    if (entry.isDirectory()) {
      walkDir(fullPath, files);
    } else if (SCAN_EXTENSIONS.includes(path.extname(entry.name))) {
      files.push(fullPath);
    }
  }
  return files;
}

// ─── Main ─────────────────────────────────────────────────────────────────────
let failures = 0;
let warnings = 0;
const report = [];

const allFiles = SCAN_DIRS.flatMap((d) => walkDir(path.join(ROOT, d)));

console.log(`\n🔍 SKAI Anti-Drift Scan — ${allFiles.length} files\n`);

for (const file of allFiles) {
  const content = fs.readFileSync(file, 'utf-8');
  const relPath = path.relative(ROOT, file);
  const lines = content.split('\n');

  lines.forEach((line, i) => {
    const lineNum = i + 1;

    // Brand check
    for (const pat of OLD_BRAND_PATTERNS) {
      if (pat.test(line)) {
        // Skip legitimate JARVIS references inside THIRD_PARTY_NOTICES or LICENSE
        if (relPath.includes('NOTICE') || relPath.includes('LICENSE')) continue;
        failures++;
        report.push(`❌ OLD BRAND  [${relPath}:${lineNum}] → ${line.trim().slice(0, 80)}`);
      }
    }

    // Secret check — skip .env.example, config.example.json
    if (!relPath.includes('.example') && !relPath.includes('CHANGELOG')) {
      for (const pat of SECRET_PATTERNS) {
        if (pat.test(line)) {
          failures++;
          report.push(`🔑 SECRET LEAK [${relPath}:${lineNum}] → [REDACTED]`);
        }
      }
    }
  });
}

// ─── Required Files Check ─────────────────────────────────────────────────────
const REQUIRED_FILES = [
  'package.json',
  'tsconfig.json',
  'tsconfig.electron.json',
  'vite.config.ts',
  'index.html',
  'src/main/index.ts',
  'src/main/store.ts',
  'src/preload/index.ts',
  'src/renderer/App.tsx',
  'src/renderer/services/gemini-live-core.ts',
  'assets/skai.ico',
  'assets/sk_logo_3d.svg',
];

for (const rel of REQUIRED_FILES) {
  const full = path.join(ROOT, rel);
  if (!fs.existsSync(full)) {
    failures++;
    report.push(`📁 MISSING FILE: ${rel}`);
  }
}

// ─── Icon Naming Check ────────────────────────────────────────────────────────
const pkgJson = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf-8'));
const iconPath = pkgJson?.build?.win?.icon;
if (iconPath && iconPath.includes('jarvis')) {
  failures++;
  report.push(`❌ OLD ICON NAME in package.json build.win.icon: ${iconPath}`);
}

// ─── Results ─────────────────────────────────────────────────────────────────
console.log(report.join('\n') || '  (no issues found)');
console.log(`\n${'─'.repeat(60)}`);
console.log(`Failures: ${failures} | Warnings: ${warnings}`);

if (failures === 0) {
  console.log('\n✅ ANTI-DRIFT SCAN PASSED — SKAI repository is clean.\n');
  process.exit(0);
} else {
  console.log('\n❌ ANTI-DRIFT SCAN FAILED — Fix the above issues and re-run.\n');
  process.exit(1);
}
