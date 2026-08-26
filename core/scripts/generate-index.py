#!/usr/bin/env python3
"""Generate complete INDEX.md and role-skill-index.json for agent-skills.

Indexes every role, skill, workflow, and schema found on disk (counts are
computed, never hard-coded) with alias mapping for seamless @role @skill
invocation in Antigravity.

Run with --check to verify that the generated artifacts are up to date
without writing; exits 1 when any artifact is stale.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CORE_ROOT = ROOT / "core"
ROLES_DIR = CORE_ROOT / "roles"
SKILLS_DIR = CORE_ROOT / "skills"
WORKFLOWS_DIR = CORE_ROOT / "workflows"
SCHEMAS_DIR = CORE_ROOT / "contracts" / "schemas"
REGISTRY_DIR = CORE_ROOT / "a2a" / ".well-known"
VERSION_PATH = ROOT / "VERSION"


def pack_version() -> str:
    return VERSION_PATH.read_text(encoding="utf-8").strip()

# Comprehensive Role Aliases
ROLE_ALIASES = {
    # Content & Writing
    "writer": "content-writer",
    "copywriter": "content-writer",
    "author": "content-writer",
    "article-writer": "content-writer",
    "blog-writer": "content-writer",
    "tech-writer": "technical-writer",
    "doc-writer": "technical-writer",
    "docs": "technical-writer",
    "documentation-writer": "technical-writer",
    
    # Engineering / Development
    "backend": "backend-developer",
    "be": "backend-developer",
    "backend-dev": "backend-developer",
    "frontend": "frontend-developer",
    "fe": "frontend-developer",
    "frontend-dev": "frontend-developer",
    "ui-developer": "frontend-developer",
    "mobile": "mobile-engineer",
    "flutter": "mobile-engineer",
    "react-native": "mobile-engineer",
    "ecommerce": "ecommerce-engineer",
    "ecom": "ecommerce-engineer",
    "3d": "3d-graphics-engineer",
    "r3f": "3d-graphics-engineer",
    "threejs": "3d-graphics-engineer",
    
    # DevOps, Cloud & Platform
    "devops": "devops-engineer",
    "infra": "devops-engineer",
    "infrastructure": "devops-engineer",
    "sre": "sre",
    "reliability": "sre",
    "sysadmin": "system-engineer",
    "system": "system-engineer",
    "systems-engineer": "system-engineer",
    "cloudflare": "cloudflare-engineer",
    "cf": "cloudflare-engineer",
    "workers": "cloudflare-engineer",
    "aws": "aws-engineer",
    "cloud": "aws-engineer",
    
    # AI & Agent Swarm
    "ai": "ai-systems-engineer",
    "ml": "ai-systems-engineer",
    "llm": "ai-systems-engineer",
    "coordinator": "agent-coordinator",
    "swarm-coordinator": "agent-coordinator",
    "discovery": "agent-discovery-engineer",
    "agent-discovery": "agent-discovery-engineer",
    
    # Design & Product
    "designer": "ui-ux-designer",
    "ui": "ui-ux-designer",
    "ux": "ui-ux-designer",
    "ui-ux": "ui-ux-designer",
    "uiux": "ui-ux-designer",
    "pm": "product-manager",
    "prod-mgr": "product-manager",
    "product-owner": "product-manager",
    "po": "product-manager",
    "pjm": "project-manager",
    "proj-mgr": "project-manager",
    "scrum-master": "project-manager",
    "planner": "task-planner",
    "task-scheduler": "task-planner",
    
    # Architecture & Leadership
    "architect": "solution-architect",
    "solution-arch": "solution-architect",
    "solutions-architect": "solution-architect",
    "tech-architect": "technical-architect",
    "enterprise-architect": "technical-architect",
    "lead": "technical-lead",
    "tech-lead": "technical-lead",
    "engineering-lead": "technical-lead",
    
    # QA & Security & Review
    "qa": "qa-engineer",
    "tester": "qa-engineer",
    "test-engineer": "qa-engineer",
    "security": "security-engineer",
    "sec": "security-engineer",
    "appsec": "security-engineer",
    "secops": "security-engineer",
    "reviewer": "reviewer",
    "code-reviewer": "reviewer",
    "pr-reviewer": "reviewer",
    
    # Data & Analytics & SEO
    "da": "data-analyst",
    "data-analytics": "data-analyst",
    "de": "data-engineer",
    "data-eng": "data-engineer",
    "ba": "business-analyst",
    "business": "business-analyst",
    "seo": "seo-analyst",
    "seo-specialist": "seo-analyst",
    "seo-expert": "seo-analyst",
    "research": "researcher",
    "deep-research": "researcher",
    
    # Business & Domain
    "accounting": "vietnam-accounting-specialist",
    "accountant": "vietnam-accounting-specialist",
    "ke-toan": "vietnam-accounting-specialist",
    "vietnam-accounting": "vietnam-accounting-specialist",
    "mmo": "mmo-engineer",
    "affiliate": "mmo-engineer",
    "growth": "mmo-engineer",
    "teacher": "teacher",
    "instructor": "teacher",
    "educator": "teacher",
    "mentor": "teacher"
}

# Skill Aliases and Composite Mappings
SKILL_ALIASES = {
    # Composite combinations
    "research_and_writing": ["conduct-research", "write-article"],
    "research-and-writing": ["conduct-research", "write-article"],
    "research_writing": ["conduct-research", "write-article"],
    
    # Common Short Names / Snake Case
    "research": ["conduct-research"],
    "conduct_research": ["conduct-research"],
    "deep_research": ["conduct-research"],
    "writing": ["write-article"],
    "write_article": ["write-article"],
    "write_article_vietnamese": ["write-article"],
    "docs": ["write-documentation"],
    "documentation": ["write-documentation"],
    "write_doc": ["write-documentation"],
    "write_docs": ["write-documentation"],
    "write_documentation": ["write-documentation"],
    "tech_radar": ["write-tech-radar"],
    "write_tech_radar": ["write-tech-radar"],
    "seo": ["optimize-seo"],
    "optimize_seo": ["optimize-seo"],
    "seo_optimization": ["optimize-seo"],
    "audit_content": ["audit-content"],
    "content_audit": ["audit-content"],
    "repurpose_content": ["repurpose-content"],
    
    # Backend & API
    "api": ["add-api-endpoint"],
    "add_api_endpoint": ["add-api-endpoint"],
    "create_api": ["add-api-endpoint"],
    "new_endpoint": ["add-api-endpoint"],
    "event_handler": ["add-event-handler"],
    "add_event_handler": ["add-event-handler"],
    "service_client": ["add-service-client"],
    "add_service_client": ["add-service-client"],
    "structured_outputs": ["implement-structured-outputs"],
    "implement_structured_outputs": ["implement-structured-outputs"],
    "mcp_server": ["build-mcp-server"],
    "build_mcp_server": ["build-mcp-server"],
    "scaffold_service": ["scaffold-new-service"],
    "scaffold_new_service": ["scaffold-new-service"],
    
    # Database & Migrations
    "migration": ["create-migration"],
    "create_migration": ["create-migration"],
    "database": ["database-maintenance"],
    "db_maintenance": ["database-maintenance"],
    "data_pipeline": ["build-data-pipeline"],
    "build_data_pipeline": ["build-data-pipeline"],
    
    # Frontend & UI
    "ui_component": ["add-ui-component"],
    "add_ui_component": ["add-ui-component"],
    "page_route": ["add-page-route"],
    "add_page_route": ["add-page-route"],
    "design_system": ["setup-design-system"],
    "setup_design_system": ["setup-design-system"],
    "visual_regression": ["setup-visual-regression"],
    "setup_visual_regression": ["setup-visual-regression"],
    "frontend_testing": ["frontend-testing"],
    
    # Testing & QA
    "tests": ["write-tests"],
    "write_tests": ["write-tests"],
    "unit_tests": ["write-tests"],
    "e2e_tests": ["write-tests"],
    "test_report": ["write-tests"],
    
    # Security & Policy
    "security": ["security-audit"],
    "security_audit": ["security-audit"],
    "secrets": ["manage-secrets"],
    "manage_secrets": ["manage-secrets"],
    "supply_chain": ["supply-chain-security"],
    
    # DevOps & Cloud
    "deploy": ["setup-deployment"],
    "deployment": ["setup-deployment"],
    "setup_deployment": ["setup-deployment"],
    "wrangler": ["wrangler"],
    "workers_best_practices": ["workers-best-practices"],
    "aws_infra": ["aws-infrastructure"],
    "aws_infrastructure": ["aws-infrastructure"],
    "perf": ["performance-profiling"],
    "performance": ["performance-profiling"],
    "performance_profiling": ["performance-profiling"],
    "telemetry": ["add-telemetry-instrumentation"],
    "instrumentation": ["add-telemetry-instrumentation"],
    
    # A2A & Swarm
    "a2a": ["agent-a2a-protocol"],
    "a2a_protocol": ["agent-a2a-protocol"],
    "delegation": ["agent-delegation"],
    "agent_delegation": ["agent-delegation"],
    "orchestration": ["agent-graph-orchestration"],
    "graph_orchestration": ["agent-graph-orchestration"],
    "handoff": ["agent-handoff"],
    "model_routing": ["agent-model-routing"],
    "quality_gate": ["agent-quality-gate"],
    "semantic_memory": ["agent-semantic-memory"],
    "tool_orchestration": ["agent-tool-orchestration"],
    
    # Business & Vietnam Domain
    "accounting": ["manage-vietnam-accounting"],
    "vietnam_accounting": ["manage-vietnam-accounting"],
    "product_brief": ["write-product-brief"],
    "write_product_brief": ["write-product-brief"],
    "business_requirements": ["analyze-business-requirements"],
    "analyze_business_requirements": ["analyze-business-requirements"],
    "analyze_data": ["analyze-data"]
}


def parse_roles() -> dict:
    roles = {}
    for r_file in sorted(ROLES_DIR.glob("*.md")):
        if r_file.name in ["README.md", "role-standard.md"]:
            continue
        content = r_file.read_text(encoding="utf-8")
        title_m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        desc_m = re.search(r">\s*(.+)$", content, re.MULTILINE)
        skills = re.findall(r"- `([a-z0-9-]+)`", content)
        
        irrev_m = re.search(r"## Irreversible Actions\s*\n((?:[^\n]+\n)+)", content)
        irreversible = []
        if irrev_m:
            irreversible = [line.strip("- *").strip() for line in irrev_m.group(1).strip().splitlines() if line.strip()]

        roles[r_file.stem] = {
            "name": r_file.stem,
            "title": title_m.group(1).strip() if title_m else r_file.stem,
            "description": desc_m.group(1).strip() if desc_m else "",
            "file": str(r_file.relative_to(ROOT)).replace("\\", "/"),
            "skills": skills,
            "irreversible_actions": irreversible
        }
    return roles


def parse_skills() -> dict:
    skills = {}
    for s_file in sorted((CORE_ROOT / "skills").glob("*/*/SKILL.md")):
        cat = s_file.parent.parent.name
        name = s_file.parent.name
        content = s_file.read_text(encoding="utf-8")
        desc_m = re.search(r"description:\s*(?:>-\s*)?([^\n\r]+(?:\n\s+[^\n\r]+)*)", content)
        desc = desc_m.group(1).replace("\n", " ").strip() if desc_m else ""
        skills[name] = {
            "name": name,
            "category": cat,
            "type": "core",
            "file": str(s_file.relative_to(ROOT)).replace("\\", "/"),
            "description": desc
        }

    for s_file in sorted(ROOT.glob("overlays/*/skills/*/SKILL.md")):
        ov_name = s_file.parent.parent.parent.name
        name = s_file.parent.name
        content = s_file.read_text(encoding="utf-8")
        desc_m = re.search(r"description:\s*(?:>-\s*)?([^\n\r]+(?:\n\s+[^\n\r]+)*)", content)
        desc = desc_m.group(1).replace("\n", " ").strip() if desc_m else ""
        skills[name] = {
            "name": name,
            "category": f"overlay/{ov_name}",
            "type": "overlay",
            "file": str(s_file.relative_to(ROOT)).replace("\\", "/"),
            "description": desc
        }
    return skills


def parse_workflows() -> dict:
    workflows = {}
    for w_file in sorted(WORKFLOWS_DIR.glob("*.md")):
        if w_file.name == "README.md":
            continue
        content = w_file.read_text(encoding="utf-8")
        title_m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        workflows[w_file.stem] = {
            "name": w_file.stem,
            "title": title_m.group(1).strip() if title_m else w_file.stem,
            "file": str(w_file.relative_to(ROOT)).replace("\\", "/")
        }
    return workflows


def parse_schemas() -> dict:
    schemas = {}
    for s_file in sorted(SCHEMAS_DIR.glob("*.json")):
        try:
            data = json.loads(s_file.read_text(encoding="utf-8"))
            title = data.get("title", s_file.stem)
        except Exception:
            title = s_file.stem
        schemas[s_file.name] = {
            "name": s_file.name,
            "stem": s_file.stem,
            "title": title,
            "file": str(s_file.relative_to(ROOT)).replace("\\", "/")
        }
    return schemas


def generate_markdown_index(roles: dict, skills: dict, workflows: dict, schemas: dict) -> str:
    version = pack_version()
    core_count = sum(1 for s in skills.values() if s.get("type") == "core")
    overlay_count = sum(1 for s in skills.values() if s.get("type") == "overlay")
    md = []
    md.append("# Agent-Skills Master Index & Router")
    md.append("")
    md.append(f"> **Location:** `core/` & `overlays/` | **Version:** `{version}` (A2A 1.0 + Antigravity)")
    md.append(f"> **Total Catalog:** **{len(roles)} Roles** | **{len(skills)} Skills** ({core_count} Core + {overlay_count} Overlays) | **{len(workflows)} Workflows** | **{len(schemas)} Data Contracts**")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## ⚡ Fast Invocation Protocol (`@<role>` & `@<skill>`)")
    md.append("")
    md.append("When you mention `@<role>` and/or `@<skill>` in chat, Antigravity resolves them immediately using this index:")
    md.append("")
    md.append("```markdown")
    md.append("# Single Role + Skill Example")
    md.append("@writer @research_and_writing - Viết bài hướng dẫn về Antigravity 2.0")
    md.append("")
    md.append("# Developer Example")
    md.append("@backend @add_api_endpoint - Tạo REST API endpoint quản lý user orders")
    md.append("")
    md.append("# Swarm Coordinator Example")
    md.append("@coordinator @a2a - Phối hợp @frontend và @backend hoàn thiện tính năng checkout")
    md.append("```")
    md.append("")
    md.append("### Resolution Rules")
    md.append("1. **Role Matching:** `@<role>` resolves by exact name (e.g., `@content-writer`) or common alias (e.g., `@writer` → `content-writer`, `@be` → `backend-developer`).")
    md.append("2. **Skill Matching:** `@<skill>` resolves by exact name (e.g., `@conduct-research`), snake_case (e.g., `@conduct_research`), or composite alias (e.g., `@research_and_writing` → `conduct-research` + `write-article`).")
    md.append("3. **Automatic Loading:** The agent loads `core/roles/<role>.md` and all resolved `core/skills/<cat>/<skill>/SKILL.md` before executing.")
    md.append("4. **Contract Output:** Structured outputs must validate against `core/contracts/schemas/<schema>.json`.")
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"## 🎭 Role Directory ({len(roles)} Roles)")
    md.append("")
    md.append("| Role Slug | Title | Common Aliases | Primary Skills | Role File |")
    md.append("|:---|:---|:---|:---|:---|")
    
    role_to_aliases = {}
    for alias, target in ROLE_ALIASES.items():
        if alias != target:
            role_to_aliases.setdefault(target, []).append(f"`@{alias}`")

    for role_name, r in roles.items():
        aliases_str = ", ".join(role_to_aliases.get(role_name, [])) or "—"
        skills_str = ", ".join(f"`{s}`" for s in r["skills"][:3])
        if len(r["skills"]) > 3:
            skills_str += f" *(+{len(r['skills']) - 3} more)*"
        md.append(f"| **`@{role_name}`** | {r['title']} | {aliases_str} | {skills_str} | [`{r['file']}`](./{r['file']}) |")

    md.append("")
    md.append("---")
    md.append("")
    md.append(f"## 🛠️ Skill Directory ({len(skills)} Skills)")
    md.append("")
    
    by_cat = {}
    for sk_name, s in skills.items():
        by_cat.setdefault(s["category"], []).append(s)

    for cat_name in sorted(by_cat.keys()):
        cat_skills = by_cat[cat_name]
        md.append(f"### Category: `{cat_name}` ({len(cat_skills)} skills)")
        md.append("")
        md.append("| Skill Slug | Description | File |")
        md.append("|:---|:---|:---|")
        for s in sorted(cat_skills, key=lambda x: x["name"]):
            desc = s["description"][:100] + ("..." if len(s["description"]) > 100 else "")
            md.append(f"| **`@{s['name']}`** | {desc} | [`{s['file']}`](./{s['file']}) |")
        md.append("")

    md.append("---")
    md.append("")
    md.append("## 🔀 Composite & Short Skill Aliases Matrix")
    md.append("")
    md.append("| Mention / Shortcut | Resolves To Core Skills | Typical Role |")
    md.append("|:---|:---|:---|")
    for alias, targets in sorted(SKILL_ALIASES.items()):
        targets_str = ", ".join(f"`{t}`" for t in targets)
        md.append(f"| **`@{alias}`** | {targets_str} | Active `@role` |")

    md.append("")
    md.append("---")
    md.append("")
    md.append(f"## 🔄 Workflows ({len(workflows)} Workflows)")
    md.append("")
    md.append("| Workflow | Title | File |")
    md.append("|:---|:---|:---|")
    for wf_name, w in workflows.items():
        md.append(f"| **`/{wf_name}`** | {w['title']} | [`{w['file']}`](./{w['file']}) |")

    md.append("")
    md.append("---")
    md.append("")
    md.append(f"## 📑 Data Contracts & Schemas ({len(schemas)} Schemas)")
    md.append("")
    md.append("| Schema File | Schema Title | Path |")
    md.append("|:---|:---|:---|")
    for sc_name, sc in schemas.items():
        md.append(f"| `{sc['name']}` | {sc['title']} | [`{sc['file']}`](./{sc['file']}) |")

    return "\n".join(md)


def generate_json_index(roles: dict, skills: dict, workflows: dict, schemas: dict) -> dict:
    return {
        "version": pack_version(),
        "protocol": "A2A 1.0 + Antigravity",
        "root": ".",
        "stats": {
            "roles": len(roles),
            "skills": len(skills),
            "workflows": len(workflows),
            "schemas": len(schemas)
        },
        "role_aliases": ROLE_ALIASES,
        "skill_aliases": SKILL_ALIASES,
        "roles": roles,
        "skills": skills,
        "workflows": workflows,
        "schemas": schemas
    }


def build_artifacts(roles: dict, skills: dict, workflows: dict, schemas: dict) -> dict[str, tuple[Path, str]]:
    md = (ROOT / "INDEX.md", generate_markdown_index(roles, skills, workflows, schemas))
    json_payload = json.dumps(generate_json_index(roles, skills, workflows, schemas), indent=2, ensure_ascii=False) + "\n"
    registry_json = (REGISTRY_DIR / "role-skill-index.json", json_payload)
    adapter_json = (ROOT / "adapters" / "antigravity" / "role-skill-index.json", json_payload)
    return {"INDEX.md": md, "role-skill-index.json": registry_json, "adapters/antigravity/role-skill-index.json": adapter_json}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate INDEX.md and role-skill-index.json.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated artifacts are up to date without writing; exit 1 when stale",
    )
    args = parser.parse_args()

    print("Parsing agent-skills pack...")
    roles = parse_roles()
    skills = parse_skills()
    workflows = parse_workflows()
    schemas = parse_schemas()

    print(f"Loaded {len(roles)} roles, {len(skills)} skills, {len(workflows)} workflows, {len(schemas)} schemas.")

    artifacts = build_artifacts(roles, skills, workflows, schemas)

    if args.check:
        stale = []
        for label, (path, expected) in artifacts.items():
            actual = path.read_text(encoding="utf-8") if path.is_file() else ""
            if actual != expected:
                stale.append(label)
        if stale:
            print("Stale generated artifacts: " + ", ".join(stale))
            print("Run: python3 core/scripts/generate-index.py")
            return 1
        print("Generated artifacts are up to date.")
        return 0

    for label, (path, content) in artifacts.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Generated {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
