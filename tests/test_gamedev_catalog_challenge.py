import hashlib
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GAMEDEV_SKILLS_DIR = REPO_ROOT / "core" / "skills" / "gamedev"
ROLES_DIR = REPO_ROOT / "core" / "roles"
REGISTRY_DIR = REPO_ROOT / "core" / "a2a" / "registry"
WELL_KNOWN_DIR = REPO_ROOT / "core" / "a2a" / ".well-known"
ADAPTERS_DIR = REPO_ROOT / "adapters"

EXPECTED_20_GAMEDEV_SKILLS = [
    # Pillar 1: Core Architecture & Engine Lifecycles (5)
    "integrate-game-engine",
    "develop-gameplay-systems",
    "architect-ecs-systems",
    "manage-scene-lifecycle",
    "implement-save-persistence",
    # Pillar 2: Game Feel, Physics & Interaction (4)
    "tune-game-feel",
    "configure-physics-collision",
    "abstract-input-actions",
    "direct-camera-systems",
    # Pillar 3: AI, Gameplay Mechanics & UI/UX (4)
    "author-game-ai",
    "design-procedural-generation",
    "build-game-ui-ux",
    "integrate-dialogue-narrative",
    # Pillar 4: Graphics, Shaders & Technical Art (4)
    "program-game-shaders",
    "inspect-blender-rigs-motion",
    "render-webgl-threejs",
    "generate-game-assets-pipeline",
    # Pillar 5: Audio, Performance & Publishing (3)
    "mix-dynamic-game-audio",
    "profile-game-performance",
    "automate-game-publishing",
]

EXPECTED_LOCKS = [
    "GAME-LOOP-TIMESTEP-LOCK",
    "STATE-MACHINE-ISOLATION-LOCK",
    "MEMORY-ASSET-LIFECYCLE-LOCK",
    "INPUT-ACTION-ABSTRACTION-LOCK",
]


class TestGameDev20SkillCatalogChallenge(unittest.TestCase):
    """Verifies the 20-skill GameDev catalog, game-developer role, review checklist, A2A card, and twin parity."""

    def test_01_all_20_gamedev_skill_directories_exist(self):
        self.assertTrue(GAMEDEV_SKILLS_DIR.is_dir(), f"Missing directory: {GAMEDEV_SKILLS_DIR}")
        found_dirs = sorted([d.name for d in GAMEDEV_SKILLS_DIR.iterdir() if d.is_dir()])
        self.assertEqual(found_dirs, sorted(EXPECTED_20_GAMEDEV_SKILLS))

    def test_02_all_20_skill_md_files_adhere_to_open_standard(self):
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            skill_file = GAMEDEV_SKILLS_DIR / skill_name / "SKILL.md"
            self.assertTrue(skill_file.is_file(), f"Missing SKILL.md for {skill_name}")
            content = skill_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            self.assertLess(len(lines), 200, f"{skill_name}/SKILL.md exceeds 200 lines ({len(lines)})")
            self.assertGreaterEqual(len(lines), 40, f"{skill_name}/SKILL.md is too short ({len(lines)})")
            self.assertIn(f"name: {skill_name}", content)
            self.assertIn("description:", content)
            self.assertIn("allowed-tools:", content)
            self.assertIn("## Core Rules", content)
            self.assertIn("## Suggested Process", content)
            self.assertIn("## Output Contracts", content)
            self.assertIn("## Checklist", content)
            self.assertIn("## Related Skills", content)

    def test_03_skills_readme_lists_all_20_gamedev_skills(self):
        readme_path = REPO_ROOT / "core" / "skills" / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8")
        self.assertIn("### Game Development (20)", readme_text)
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            self.assertIn(f"`{skill_name}`", readme_text)

    def test_04_game_developer_role_links_all_20_skills_and_4_locks(self):
        role_path = ROLES_DIR / "game-developer.md"
        self.assertTrue(role_path.is_file())
        role_text = role_path.read_text(encoding="utf-8")
        for lock in EXPECTED_LOCKS:
            self.assertIn(lock, role_text, f"Missing lock {lock} in game-developer.md")
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            self.assertIn(f"`{skill_name}`", role_text, f"Missing skill {skill_name} in game-developer.md")

    def test_05_game_developer_review_checklist_completeness(self):
        checklist_path = ROLES_DIR / "references" / "game-developer-review-checklist.md"
        self.assertTrue(checklist_path.is_file())
        text = checklist_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertGreater(len(lines), 60)
        for lock in EXPECTED_LOCKS:
            self.assertIn(lock, text, f"Missing lock {lock} in game-developer-review-checklist.md")
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            self.assertIn(f"`{skill_name}`", text, f"Missing skill {skill_name} in review checklist")

    def test_06_a2a_agent_card_and_registry_sync(self):
        card_path = REGISTRY_DIR / "game-developer.agent-card.json"
        self.assertTrue(card_path.is_file())
        card = json.loads(card_path.read_text(encoding="utf-8"))
        card_skill_ids = [s.get("id") for s in card.get("skills", [])]
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            self.assertIn(skill_name, card_skill_ids, f"Missing {skill_name} in game-developer.agent-card.json")

        for s in card.get("skills", []):
            self.assertEqual(s.get("tags"), ["gamedev", "pack"], f"Skill {s.get('id')} tags mismatch")

        reg_path = WELL_KNOWN_DIR / "agent-registry.json"
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        roles = [a.get("role") for a in reg.get("agents", [])]
        self.assertIn("game-developer", roles)

    def test_07_twin_index_sha256_bitwise_parity(self):
        core_idx_path = WELL_KNOWN_DIR / "role-skill-index.json"
        adapter_idx_path = ADAPTERS_DIR / "antigravity" / "role-skill-index.json"
        core_bytes = core_idx_path.read_bytes()
        adapter_bytes = adapter_idx_path.read_bytes()
        self.assertEqual(
            hashlib.sha256(core_bytes).hexdigest(),
            hashlib.sha256(adapter_bytes).hexdigest(),
            "SHA-256 mismatch between core and adapter role-skill-index.json",
        )
        index_data = json.loads(core_bytes.decode("utf-8"))
        gd_role = index_data.get("roles", {}).get("game-developer", {})
        gd_primary = gd_role.get("primary_skills", [])
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            self.assertIn(skill_name, gd_primary, f"Missing {skill_name} in game-developer primary_skills")
            self.assertIn(skill_name, index_data.get("skills", {}), f"Missing {skill_name} in skills index")
            self.assertEqual(index_data["skills"][skill_name].get("category"), "gamedev")

    def test_08_index_md_references_all_20_skills(self):
        index_path = REPO_ROOT / "INDEX.md"
        self.assertTrue(index_path.is_file())
        text = index_path.read_text(encoding="utf-8")
        for skill_name in EXPECTED_20_GAMEDEV_SKILLS:
            self.assertIn(f"`{skill_name}`", text, f"Missing `{skill_name}` in INDEX.md")


if __name__ == "__main__":
    unittest.main()
