# Inject Output Contracts section into SKILL.md files that are missing it.
#
# Resolves the repo root dynamically from the script's own location — no
# hardcoded paths. Works on any Windows machine and under PowerShell on macOS/Linux.
#
# Usage:
#   .\core\scripts\inject_output_contracts.ps1
#   .\core\scripts\inject_output_contracts.ps1 -DryRun

param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Resolve repo root two levels above this script (scripts/ -> core/ -> root)
$ScriptDir = $PSScriptRoot
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..\..\")).Path

$SkillDirs = @(
    (Join-Path $RepoRoot "core\skills\backend"),
    (Join-Path $RepoRoot "core\skills\frontend"),
    (Join-Path $RepoRoot "core\skills\platform")
)

$ImplementationContract = @"
## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **``contracts/schemas/implementation-result.json``** -- Required fields: ``change_summary``, ``files_touched[]``, and ``validation_run``. Set ``produced_by_role`` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"@

$DeploymentContract = @"
## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **``contracts/schemas/deployment-plan.json``** -- Required fields: ``infrastructure_changes[]``, ``config_updates[]``, and ``validation_run``. Set ``produced_by_role`` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"@

$totalInjected = 0
$totalSkipped = 0

foreach ($dir in $SkillDirs) {
    if (-not (Test-Path $dir -PathType Container)) {
        Write-Warning "Skill dir not found: $dir"
        continue
    }

    $relDir = [System.IO.Path]::GetRelativePath($RepoRoot, $dir)
    Write-Host "`n$relDir/"

    $isPlatform = $dir -match "platform$"
    $contractToInject = if ($isPlatform) { $DeploymentContract } else { $ImplementationContract }

    $files = Get-ChildItem -Path $dir -Filter "SKILL.md" -Recurse
    foreach ($file in $files) {
        $path = $file.FullName
        $relPath = [System.IO.Path]::GetRelativePath($RepoRoot, $path)
        $content = Get-Content -Path $path -Raw

        if ($content -match "## Output Contracts") {
            Write-Host "  skip  $relPath -- already has Output Contracts"
            $totalSkipped++
            continue
        }

        if ($DryRun) {
            Write-Host "  would inject  $relPath"
        } else {
            if ($content -match "## Related Skills") {
                $content = $content -replace "## Related Skills", "$contractToInject`n## Related Skills"
            } else {
                $content = $content.TrimEnd() + "`n`n" + $contractToInject
            }
            Set-Content -Path $path -Value $content -NoNewline -Encoding UTF8
            Write-Host "  injected  $relPath"
        }
        $totalInjected++
    }
}

$verb = if ($DryRun) { "Would inject" } else { "Done." }
Write-Host "`n${verb}: $totalInjected files injected, $totalSkipped skipped."
