#!/usr/bin/env python3
"""Challenge tests for the 2026-10 Data Engineer modernization round.

Guards the verified 2026-10-25 data-stack baseline:
- Iceberg v3 is the ratified, implementable spec (1.11+/1.12 line); the unratified
  v4 spec is roadmap-only and must never be pinned as a production table format.
- Variant is an Iceberg v3 feature ("Support for Variant is added in Iceberg v3").
- Engine lines: Delta Lake 4.4 (Aug 2026), Spark 4.2+ (Jul 2026), Flink 2.3 (Jun 2026),
  dbt Core 2.0 (Rust engine; 1.12+ active support until 2027-07), DuckDB 1.5+/2.0 LTS
  (GA 2026-10-21), ODCS v3.2.0, PostgreSQL 18 baseline.
- Apache Ossie is cited with its Apache Incubating status (ASF since 2026-07).
"""

from __future__ import annotations

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLE_FILE = REPO_ROOT / "core" / "roles" / "data-engineer.md"
CHECKLIST_FILE = REPO_ROOT / "core" / "roles" / "references" / "data-engineer-review-checklist.md"
SKILLS_DIR = REPO_ROOT / "core" / "skills" / "security-data"
SCHEMA_FILE = REPO_ROOT / "core" / "contracts" / "schemas" / "data-pipeline-spec.json"
CONTRACTS_README = REPO_ROOT / "core" / "contracts" / "README.md"


def read(path: Path) -> str:
    assert path.exists(), f"{path} must exist"
    return path.read_text(encoding="utf-8")


def frontmatter_version(path: Path) -> str | None:
    text = read(path)
    match = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


class TestIcebergSpecCurrency(unittest.TestCase):
    """The unratified Iceberg v4 spec must never be pinned as a production format."""

    @classmethod
    def setUpClass(cls):
        cls.role = read(ROLE_FILE)
        cls.pipeline_skill = read(SKILLS_DIR / "build-data-pipeline" / "SKILL.md")

    def test_01_v4_roadmap_framing_present(self):
        self.assertIn("**Iceberg v4 is roadmap, not current**", self.role)
        self.assertIn("never create v4-format tables", self.role)
        self.assertIn("unratified Iceberg v4", self.role)

    def test_02_no_v4_as_primary_standard(self):
        for banned in (
            "standardize on Apache Iceberg v4",
            "Iceberg v4 as the primary",
            "Iceberg v4 / v3",
            "Iceberg v4 (metadata-only restructuring)",
        ):
            self.assertNotIn(banned, self.role, f"v4 must not be pinned as current: {banned}")
            self.assertNotIn(banned, self.pipeline_skill)

    def test_03_v3_is_primary_with_release_line(self):
        self.assertIn("Apache Iceberg v3", self.role)
        self.assertIn("1.11+/1.12", self.role)
        self.assertIn("the current ratified spec", self.role)

    def test_04_variant_belongs_to_v3(self):
        self.assertIn("added in Iceberg v3", self.role)
        self.assertNotIn("`VARIANT` type (Iceberg v4)", self.role)
        self.assertIn("Support for Variant is added in Iceberg v3", read(CHECKLIST_FILE))

    def test_05_anti_pattern_unratified_spec(self):
        self.assertIn(
            "standardizing production tables on an unratified specification",
            self.role,
        )


class TestEngineLineCurrency(unittest.TestCase):
    """Stack pins must reference generally available engine lines (2026-10 baseline)."""

    @classmethod
    def setUpClass(cls):
        cls.role = read(ROLE_FILE)
        cls.pipeline_skill = read(SKILLS_DIR / "build-data-pipeline" / "SKILL.md")
        cls.olap_skill = read(SKILLS_DIR / "optimize-olap-database" / "SKILL.md")
        cls.query_skill = read(SKILLS_DIR / "query-analytical-engine" / "SKILL.md")
        cls.producer_ref = read(
            SKILLS_DIR / "build-data-pipeline" / "references" / "producer-contracts-and-lakehouse.md"
        )
        cls.query_guide = read(
            SKILLS_DIR / "query-analytical-engine" / "references" / "analytical-query-guide.md"
        )
        cls.olap_guide = read(
            SKILLS_DIR / "optimize-olap-database" / "references" / "olap-database-guide.md"
        )

    def test_01_delta_lake_44(self):
        for text in (self.role, self.pipeline_skill):
            self.assertIn("Delta Lake 4.4", text)
            self.assertNotIn("Delta Lake 4.0", text)
            self.assertNotIn("Delta 4.0", text)

    def test_02_spark_42(self):
        for text in (self.role, self.olap_skill):
            self.assertIn("Spark 4.2+", text)
            self.assertNotIn("Spark 4.1", text)

    def test_03_flink_23_current(self):
        self.assertIn("Flink 2.3", self.role)

    def test_04_dbt_core_2(self):
        self.assertIn("dbt Core 2.0", self.producer_ref)
        self.assertIn("1.12+", self.producer_ref)
        self.assertNotIn("dbt 1.9", self.producer_ref)
        self.assertIn("dbt Core 2.0", self.role)

    def test_05_duckdb_15_lts_20(self):
        self.assertIn("DuckDB v1.5+", self.role)
        self.assertIn("2.0 LTS", self.role)
        self.assertIn("2026-10-21", self.role)
        for text in (self.query_skill, self.query_guide, self.olap_guide):
            self.assertNotIn("DuckDB v1.1+", text)
            self.assertNotIn("DuckDB (v1.1+)", text)
        self.assertIn("DuckDB v1.5+", self.query_skill)
        self.assertIn("DuckDB v1.5+", self.query_guide)

    def test_06_spec_currency_lock(self):
        self.assertIn("SPEC-CURRENCY-LOCK", self.role)
        for pin in (
            "Iceberg v3 (1.11+/1.12 line)",
            "Delta Lake 4.4",
            "Spark 4.2+",
            "Flink 2.3",
            "dbt Core 2.0 (1.12 floor",
            "DuckDB 1.5+/2.0 LTS",
            "ODCS v3.2.0",
        ):
            self.assertIn(pin, self.role, f"SPEC-CURRENCY-LOCK must pin: {pin}")


class TestODCSAndPostgresBaseline(unittest.TestCase):
    """ODCS v3.2.0 is the current Bitol release; relational runbooks target PostgreSQL 18."""

    def test_01_odcs_32_everywhere_in_scope(self):
        for text in (
            read(ROLE_FILE),
            read(CHECKLIST_FILE),
            read(SKILLS_DIR / "build-data-pipeline" / "SKILL.md"),
            read(SKILLS_DIR / "build-data-pipeline" / "references" / "producer-contracts-and-lakehouse.md"),
            read(SCHEMA_FILE),
            read(CONTRACTS_README),
        ):
            self.assertIn("v3.2.0", text)
            self.assertNotIn("ODCS v3.1.0", text)

    def test_02_postgres_18_runbook(self):
        relational = read(
            SKILLS_DIR / "database-maintenance" / "references" / "relational-and-vector-maintenance.md"
        )
        self.assertIn("PostgreSQL 18 Zero-Downtime Upgrades", relational)
        self.assertIn("/var/lib/postgresql/18/data", relational)
        self.assertNotIn("PostgreSQL 17", relational)
        self.assertNotIn("Postgres 15/16", relational)


class TestSkillVersionsAndASITitles(unittest.TestCase):
    """Versioned skills and official OWASP ASI titles in the modernized files."""

    def test_01_skill_versions(self):
        expected = {
            "build-data-pipeline": "2.0.0",
            "optimize-olap-database": "2.0.0",
            "query-analytical-engine": "2.0.0",
            "database-maintenance": "1.0.0",
        }
        for name, version in expected.items():
            skill = SKILLS_DIR / name / "SKILL.md"
            self.assertEqual(
                frontmatter_version(skill),
                version,
                f"{name} SKILL.md must declare version {version}",
            )

    def test_02_official_asi_titles(self):
        official = [
            "ASI04 Agentic Supply Chain",
            "ASI05 Unexpected Code Execution",
            "ASI06 Memory & Context Poisoning",
            "ASI07 Insecure Inter-Agent Communication",
        ]
        invented = [
            "ASI04 Supply Chain",
            "ASI05 RCE Guard",
            "ASI06 Context & Memory Poisoning",
            "ASI07 Inter-Agent Communication",
        ]
        for name in ("build-data-pipeline", "optimize-olap-database", "query-analytical-engine"):
            text = read(SKILLS_DIR / name / "SKILL.md")
            for title in official:
                self.assertIn(title, text, f"{name} must use official title: {title}")
            for title in invented:
                self.assertNotIn(title, text, f"{name} must not use invented title: {title}")


class TestModernizationGatesAndFooter(unittest.TestCase):
    """Checklist gains the 2026-10 gates; role footer records the round."""

    def test_01_gates_section(self):
        checklist = read(CHECKLIST_FILE)
        self.assertIn("### 11. 2026-10 Modernization Gates", checklist)
        for gate in (
            "Spec-Currency Gate",
            "Variant-Spec Gate",
            "Engine-Currency Gate",
            "ODCS-Currency Gate",
            "PostgreSQL-Baseline Gate",
            "Semantic-Layer Gate",
        ):
            self.assertIn(gate, checklist)

    def test_02_ossie_incubating(self):
        role = read(ROLE_FILE)
        self.assertIn("Apache Ossie (Incubating, ASF since 2026-07)", role)

    def test_03_footer_date(self):
        lines = [line.strip() for line in read(ROLE_FILE).splitlines() if line.strip()]
        self.assertEqual(lines[-1], "Last updated: 2026-10-25")

    def test_04_guardrail_lock_count_text(self):
        role = read(ROLE_FILE)
        self.assertIn("12 immutable Data Guardrail Locks", role)


if __name__ == "__main__":
    unittest.main()
