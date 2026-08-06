#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
PATTERNS = {
    "absolute_user_path": re.compile(r"/Users/[A-Za-z0-9_.-]+"),
    "api_key_like": re.compile(r"(sk-[A-Za-z0-9_\-]{20,}|api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-]{12,})", re.I),
    "local_secret_file": re.compile(r"(settings\.local\.json|\.env\.local|credentials\.json|token\.json)", re.I),
    "private_data_hint": re.compile(r"(客户真实名称|未脱敏|不要外传|confidential)", re.I),
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", "workspace"}
LOCAL_BLOCKLIST = ".privacy_blocklist.local"
SKIP_FILES = {"privacy_scan.py", LOCAL_BLOCKLIST}

local_blocklist = ROOT / LOCAL_BLOCKLIST
if local_blocklist.exists():
    terms = [line.strip() for line in local_blocklist.read_text(encoding="utf-8").splitlines()]
    terms = [term for term in terms if term and not term.startswith("#")]
    if terms:
        PATTERNS["local_private_blocklist"] = re.compile("|".join(re.escape(term) for term in terms), re.I)

hits = []
for path in ROOT.rglob("*"):
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    if path.name in SKIP_FILES or not path.is_file():
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for name, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            hits.append((name, path.relative_to(ROOT), line, m.group(0)[:80]))

if hits:
    for name, path, line, sample in hits:
        print(f"{name}: {path}:{line}: {sample}")
    sys.exit(1)

print("privacy scan passed")
