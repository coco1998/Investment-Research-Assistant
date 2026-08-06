#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
workspace = ROOT / "workspace"
example = ROOT / "workspace.example"

if workspace.exists():
    print(f"workspace already exists: {workspace}")
else:
    shutil.copytree(example, workspace)
    print(f"created workspace from example: {workspace}")
