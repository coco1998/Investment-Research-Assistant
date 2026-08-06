#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def load_config() -> dict:
    cfg = {}
    cfg_path = Path(os.getenv("IRA_CONFIG", ROOT / "config.yaml"))
    if cfg_path.exists():
        try:
            import yaml
            loaded = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            if isinstance(loaded, dict):
                cfg.update(loaded)
        except Exception:
            pass
    env_root = os.getenv("IRA_WORKSPACE_ROOT")
    if env_root:
        cfg["workspace_root"] = env_root
    cfg.setdefault("workspace_root", str(ROOT / "workspace"))
    return cfg


WORKSPACE = Path(load_config()["workspace_root"]).expanduser()
if not WORKSPACE.is_absolute():
    WORKSPACE = (ROOT / WORKSPACE).resolve()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        return {}, text
    raw, body = match.group(1), match.group(2)
    meta = {}
    try:
        import yaml
        parsed = yaml.safe_load(raw) or {}
        if isinstance(parsed, dict):
            meta = parsed
    except Exception:
        for line in raw.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip().strip('"')
    return meta, body


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return []
        if value.startswith("[") and value.endswith("]"):
            return [item.strip().strip('"').strip("'") for item in value[1:-1].split(",") if item.strip()]
        return [value]
    return [str(value)]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORKSPACE))
    except ValueError:
        return str(path)


def title_from_filename(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ")


def classify_material(path: Path) -> str:
    name = path.name.lower()
    parent = "/".join(part.lower() for part in path.parts)
    if any(k in name for k in ["bp", "pitch", "商业计划书"]):
        return "BP"
    if any(k in parent for k in ["datapack", "技术", "专利", "产品", "财务", "法务", "团队"]):
        return "Datapack"
    if any(k in parent for k in ["管理层访谈", "管访"]):
        return "管理层访谈"
    if any(k in parent for k in ["专家访谈", "专家"]):
        return "专家访谈"
    if any(k in parent for k in ["参考", "行业", "research"]):
        return "参考资料"
    return "其他材料"


def parse_meetings() -> list[dict]:
    out = []
    for path in sorted((WORKSPACE / "meetings").glob("*.md")):
        meta, body = parse_frontmatter(read(path))
        out.append({
            "file": path.name,
            "path": rel(path),
            "title": str(meta.get("title") or title_from_filename(path)),
            "date": str(meta.get("date") or ""),
            "type": str(meta.get("type") or ""),
            "company": str(meta.get("company") or ""),
            "person": str(meta.get("person") or ""),
            "role": str(meta.get("role") or ""),
            "track": as_list(meta.get("track")),
            "project": str(meta.get("project") or ""),
            "summary": str(meta.get("summary") or ""),
            "key_points": as_list(meta.get("key_points")),
            "follow_up": str(meta.get("follow_up") or ""),
            "body": body.strip(),
        })
    return out


def parse_projects(meetings: list[dict]) -> list[dict]:
    projects = []
    root = WORKSPACE / "projects"
    if not root.exists():
        return projects
    for pdir in sorted([p for p in root.iterdir() if p.is_dir()]):
        master = pdir / "master.md"
        meta, body = ({}, "")
        if master.exists():
            meta, body = parse_frontmatter(read(master))

        reports = []
        for report in sorted((pdir / "reports").glob("*.md")):
            rmeta, rbody = parse_frontmatter(read(report))
            reports.append({
                "file": report.name,
                "path": rel(report),
                "name": report.stem,
                "title": str(rmeta.get("title") or title_from_filename(report)),
                "date": str(rmeta.get("date") or rmeta.get("updated") or ""),
                "stage": str(rmeta.get("stage") or ""),
                "version": str(rmeta.get("version") or ""),
                "body": rbody.strip(),
            })

        materials = []
        mroot = pdir / "materials"
        if mroot.exists():
            for item in sorted([x for x in mroot.rglob("*") if x.is_file()]):
                materials.append({
                    "file": item.name,
                    "path": rel(item),
                    "category": classify_material(item),
                    "ext": item.suffix.lower().lstrip(".") or "file",
                    "size": item.stat().st_size,
                })

        related_meetings = [m for m in meetings if m.get("project") == pdir.name or m.get("company") == pdir.name]
        projects.append({
            "name": pdir.name,
            "path": rel(master) if master.exists() else "",
            "project": str(meta.get("project") or pdir.name),
            "track": as_list(meta.get("track")),
            "stage": str(meta.get("stage") or ""),
            "verdict": str(meta.get("verdict") or ""),
            "team": str(meta.get("team") or ""),
            "valuation": str(meta.get("valuation") or ""),
            "updated": str(meta.get("updated") or ""),
            "summary": str(meta.get("summary") or ""),
            "next_step": str(meta.get("next_step") or ""),
            "body": body.strip(),
            "reports": reports,
            "materials": materials,
            "meetings": related_meetings,
        })
    return projects


def parse_wiki(kind: str) -> list[dict]:
    out = []
    root = WORKSPACE / "knowledge" / "2_wiki" / kind
    if not root.exists():
        return out
    for path in sorted(root.glob("*.md")):
        meta, body = parse_frontmatter(read(path))
        first = ""
        for line in body.splitlines():
            stripped = line.strip().lstrip("#").strip()
            if stripped and not stripped.startswith("|") and not stripped.startswith("-"):
                first = stripped
                break
        out.append({
            "name": path.stem,
            "path": rel(path),
            "type": str(meta.get("type") or ""),
            "track": as_list(meta.get("track")),
            "summary": str(meta.get("summary") or first[:160]),
            "body": body.strip(),
        })
    return out


def main() -> None:
    meetings = parse_meetings()
    projects = parse_projects(meetings)
    data = {
        "workspace": str(WORKSPACE),
        "generated": datetime.now().isoformat(timespec="seconds"),
        "projects": projects,
        "interviews": meetings,
        "entities": parse_wiki("entities"),
        "concepts": parse_wiki("concepts"),
        "stats": {
            "project_count": len(projects),
            "meeting_count": len(meetings),
            "report_count": sum(len(p["reports"]) for p in projects),
            "material_count": sum(len(p["materials"]) for p in projects),
            "meeting_types": dict(Counter(m["type"] for m in meetings if m.get("type"))),
        },
    }
    (HERE / "data.js").write_text("window.RESEARCH_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(f"wrote {HERE / 'data.js'}")
    print(json.dumps(data["stats"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
