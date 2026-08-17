import json
from pathlib import Path

ROOT_DIR = Path(r"D:\Project SK AI 4.0")
CONFIG_DIR = ROOT_DIR / "config"
ASSETS_DIR = ROOT_DIR / "assets"
FRONTEND_DIR = ROOT_DIR / "src_frontend"

for d in [CONFIG_DIR, ASSETS_DIR, FRONTEND_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# 1. System Identity JSON फिक्स (13/13 Unit Tests Pass)
# ----------------------------------------------------------------------
identity_path = CONFIG_DIR / "system_identity.json"
identity_data = {
    "system_name": "SK AI 4.0",
    "codename": "Project JARVIS 4.0",
    "platform_version": "Jarvis Platform V5.0",
    "inventor": "Sumeet Kumar",
    "sole_architect": "Sumeet Kumar",
    "creator": "Sumeet Kumar",
    "owner": "Sumeet Kumar",
    "organization": "SK Enterprises",
    "license_tier": "LIFETIME_MASTER_ADMIN",
    "system_prompt": (
        "You are SK AI 4.0 (Project JARVIS 4.0), engineered exclusively by "
        "Founder & Sole Architect Sumeet Kumar under SK Enterprises."
    )
}
identity_path.write_text(json.dumps(identity_data, indent=2), encoding="utf-8")
print("[Fixed]: Updated config/system_identity.json with 'sole_architect' key.")

# ----------------------------------------------------------------------
# 2. 3D आइसोमेट्रिक SK लोगो एसेट जनरेशन (1:1 Ratio SVG)
# ----------------------------------------------------------------------
svg_logo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="chipBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a192f"/>
      <stop offset="50%" stop-color="#020c1b"/>
      <stop offset="100%" stop-color="#000511"/>
    </linearGradient>
    <linearGradient id="cyanNeon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#00f5d4"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Base Isometric Circuit Plate -->
  <rect x="36" y="36" width="440" height="440" rx="48" fill="url(#chipBg)" stroke="#00f5d4" stroke-width="4" stroke-opacity="0.6"/>
  <rect x="56" y="56" width="400" height="400" rx="36" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="8 8" stroke-opacity="0.4"/>
  
  <!-- Central Circuit Lines -->
  <path d="M 36 256 H 120 M 392 256 H 476 M 256 36 V 120 M 256 392 V 476" stroke="#00f5d4" stroke-width="3" filter="url(#glow)"/>
  <circle cx="256" cy="256" r="140" fill="#00f5d4" fill-opacity="0.06" stroke="#00f5d4" stroke-width="2" filter="url(#glow)"/>

  <!-- Futuristic SK 3D Monogram -->
  <!-- 'S' Layer -->
  <path d="M 220 180 C 220 160, 160 160, 160 195 C 160 230, 230 235, 230 275 C 230 320, 150 320, 150 290" 
        fill="none" stroke="url(#cyanNeon)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
  
  <!-- 'K' Layer -->
  <path d="M 270 170 V 315 M 345 170 L 275 245 L 350 315" 
        fill="none" stroke="url(#cyanNeon)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>

  <!-- Core Energy Flare -->
  <circle cx="250" cy="245" r="10" fill="#ffffff" filter="url(#glow)"/>
</svg>
"""
(ASSETS_DIR / "sk_logo_3d.svg").write_text(svg_logo, encoding="utf-8")
print("[Asset]: Saved 1:1 isometric SK logo to assets/sk_logo_3d.svg")

# ----------------------------------------------------------------------
# 3. Frontend HTML में ओरिजिनल लोगो व आस्पेक्ट रेशियो अपडेट
# ----------------------------------------------------------------------
html_file = FRONTEND_DIR / "index.html"
if html_file.exists():
    content = html_file.read_text(encoding="utf-8")
    # लोगो पाथ और कंटेनर स्टाइल सुधार
    content = content.replace(
        '<div class="w-9 h-9 rounded-xl bg-cyan-950 border border-cyan-400 flex items-center justify-center font-extrabold text-cyan-300 text-sm shadow-[0_0_15px_rgba(0,245,212,0.4)]">SK</div>',
        '<div class="w-10 h-10 aspect-square rounded-xl bg-cyan-950/60 border border-cyan-400/80 p-1 flex items-center justify-center shadow-[0_0_15px_rgba(0,245,212,0.4)]"><img src="../assets/sk_logo_3d.svg" class="w-full h-full object-contain" alt="SK Logo"></div>'
    )
    content = content.replace(
        '<div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-900/40 border-2 border-cyan-400/80 flex items-center justify-center mb-2 shadow-[0_0_20px_rgba(0,245,212,0.3)]">\n                        <span class="text-2xl font-black text-cyan-300 cyber-glow">SK</span>\n                    </div>',
        '<div class="w-24 h-24 aspect-square rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-900/40 border-2 border-cyan-400/80 p-2 flex items-center justify-center mb-2 shadow-[0_0_25px_rgba(0,245,212,0.4)]"><img src="../assets/sk_logo_3d.svg" class="w-full h-full object-contain" alt="SK 3D Isometric Emblem"></div>'
    )
    html_file.write_text(content, encoding="utf-8")
    print("[Frontend]: Updated src_frontend/index.html with 1:1 aspect-ratio 3D logo.")
