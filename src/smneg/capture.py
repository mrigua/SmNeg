"""Trigger the configured Shoot shortcut in Nikon NX Tether on macOS."""

NX_TETHER_ID = "jp.co.nikon.NXTether"
NX_TETHER_PATH = "/Applications/Nikon Software/NXTether/NXTether.app"
SHOOT_SHORTCUT = "⌘K"
ACCESSIBILITY_REQUIRED = "SMNEG_ACCESSIBILITY_REQUIRED"
ACCESSIBILITY_SETTINGS = "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"

CAPTURE_SCRIPT = f"""
ObjC.import('ApplicationServices');
const options = $({{AXTrustedCheckOptionPrompt: true}});
if (!$.AXIsProcessTrustedWithOptions(options)) {{
    throw new Error('{ACCESSIBILITY_REQUIRED}');
}}

const events = Application('System Events');
const matching = events.applicationProcesses.whose({{bundleIdentifier: '{NX_TETHER_ID}'}});
let tether;
for (let attempt = 0; attempt < 40; attempt++) {{
    if (matching().length) {{
        if (!tether) {{
            tether = matching[0];
            tether.frontmost = true;
        }}
        if (tether.frontmost()) break;
    }}
    delay(0.25);
}}
if (!tether || !tether.frontmost()) throw new Error('NX Tether is not ready.');
events.keystroke('k', {{using: ['command down']}});
delay(0.3);
tether.visible = false;
"""
