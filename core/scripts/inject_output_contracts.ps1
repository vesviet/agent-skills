$skillDirs = @(
    "D:\myproject\agent-skills\core\skills\backend",
    "D:\myproject\agent-skills\core\skills\frontend",
    "D:\myproject\agent-skills\core\skills\platform"
)

$implementationContract = @"
## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"@

$deploymentContract = @"
## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/deployment-plan.json`** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

"@

foreach ($dir in $skillDirs) {
    $files = Get-ChildItem -Path $dir -Filter "SKILL.md" -Recurse
    foreach ($file in $files) {
        $path = $file.FullName
        $content = Get-Content -Path $path -Raw
        
        if ($content -match "## Output Contracts") {
            Write-Host "Skipping $path - already has Output Contracts"
            continue
        }
        
        $contractToInject = if ($dir -match "platform") { $deploymentContract } else { $implementationContract }
        
        if ($content -match "## Related Skills") {
            $content = $content -replace "## Related Skills", "$contractToInject`n## Related Skills"
        } else {
            $content = $content + "`n`n" + $contractToInject
        }
        
        Set-Content -Path $path -Value $content -NoNewline
        Write-Host "Injected Output Contracts into $path"
    }
}

Write-Host "Done."
