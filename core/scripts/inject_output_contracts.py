import os
import glob

# Define directories to scan
skill_dirs = [
    "D:/myproject/agent-skills/core/skills/backend",
    "D:/myproject/agent-skills/core/skills/frontend",
    "D:/myproject/agent-skills/core/skills/platform"
]

implementation_contract = """## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"""

deployment_contract = """## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"""

for d in skill_dirs:
    # Find all SKILL.md files
    for root, _, files in os.walk(d):
        for file in files:
            if file == "SKILL.md":
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if it already has Output Contracts
                if "## Output Contracts" in content:
                    print(f"Skipping {path} - already has Output Contracts")
                    continue
                
                # Decide which contract to use based on the parent folder
                contract_to_inject = deployment_contract if "platform" in d else implementation_contract
                
                # Inject right before ## Related Skills, or at the end if not found
                if "## Related Skills" in content:
                    content = content.replace("## Related Skills", contract_to_inject + "## Related Skills")
                else:
                    content = content + "\n\n" + contract_to_inject
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Injected Output Contracts into {path}")

print("Done.")
