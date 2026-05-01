/**
 * TZP FB Grabber Build Script
 * Copies index.html to www/ directory for Capacitor
 */
const fs = require('fs');
const path = require('path');

const wwwDir = path.join(__dirname, 'www');
const srcFile = path.join(__dirname, 'index.html');
const destFile = path.join(wwwDir, 'index.html');

// Create www dir if not exists
if (!fs.existsSync(wwwDir)) {
  fs.mkdirSync(wwwDir, { recursive: true });
  console.log('[✓] Created www/ directory');
}

// Copy index.html
fs.copyFileSync(srcFile, destFile);
console.log('[✓] Copied index.html → www/index.html');

// Create a simple .gitkeep in www
fs.writeFileSync(path.join(wwwDir, '.gitkeep'), '');
console.log('[✓] Build complete. Run: npx cap sync');