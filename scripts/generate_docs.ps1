# PowerShell script to generate documentation structure from a markdown file.

# Function to sanitize a string for file/directory names
function Sanitize-Name {
    param (
        [string]$Name
    )

    # Remove markdown headers and list bullets
    $cleanName = $Name -replace '^\s*#+\s*|\s*-\s*'
    $cleanName = $cleanName.Trim()

    # Normalize characters (basic version)
    $normalized = $cleanName.ToLower()

    # Replace spaces and special characters with underscores
    $sanitized = $normalized -replace '[\s./-]+', '_'
    $sanitized = $sanitized -replace '[^a-z0-9_]', ''
    $sanitized = $sanitized -replace '^\d+(_\d+)*_?', ''
    $sanitized = $sanitized -replace '_+', '_'
    return $sanitized.Trim('_')
}

# --- Script Configuration ---
$sourceMd = "docs/CONTENIDOS_FE.md"
$targetDir = "docs/temario"

Write-Output "Iniciando la creación de la estructura desde '$sourceMd' en '$targetDir'..."

# --- Clean and create target directory ---
if (Test-Path $targetDir) {
    Remove-Item -Recurse -Force $targetDir
}
New-Item -ItemType Directory -Path $targetDir | Out-Null

# --- Parse Markdown and Build Structure ---
$content = Get-Content $sourceMd -Encoding UTF8
$structure = [ordered]@{}
$currentModule = ""

foreach ($line in $content) {
    if ($line -match "^##\s+(.*)") {
        $currentModule = $matches[1]
        $structure[$currentModule] = [System.Collections.ArrayList]@()
    } elseif ($line -match "^###\s+(.*)" -and $currentModule) {
        $section = $matches[1]
        $structure[$currentModule].Add($section) | Out-Null
    }
}

# --- Generate Files and Links ---

# Create root index.md
$rootIndexPath = Join-Path $targetDir "index.md"
$rootContent = "# Temario Principal`n`n## Módulos`n`n"
$moduleKeys = @($structure.Keys)

for ($i = 0; $i -lt $moduleKeys.Count; $i++) {
    $moduleName = $moduleKeys[$i]
    $moduleSanitized = Sanitize-Name $moduleName
    $rootContent += "- [$moduleName]($moduleSanitized/index.md)`n"
}
$rootContent | Out-File -FilePath $rootIndexPath -Encoding utf8

# Create module files
for ($i = 0; $i -lt $moduleKeys.Count; $i++) {
    $moduleName = $moduleKeys[$i]
    $moduleSanitized = Sanitize-Name $moduleName
    $modulePath = Join-Path $targetDir $moduleSanitized
    New-Item -ItemType Directory -Path $modulePath | Out-Null

    $moduleIndexPath = Join-Path $modulePath "index.md"
    $moduleIndexContent = "# $moduleName`n`n"

    # Navigation links
    $navLinks = @("[Volver al Temario](../index.md)")
    if ($i -gt 0) {
        $prevModuleName = $moduleKeys[$i-1]
        $prevModuleSanitized = Sanitize-Name $prevModuleName
        $navLinks += "[< Anterior: $prevModuleName](../$prevModuleSanitized/index.md)"
    }
    if ($i -lt $moduleKeys.Count - 1) {
        $nextModuleName = $moduleKeys[$i+1]
        $nextModuleSanitized = Sanitize-Name $nextModuleName
        $navLinks += "[Siguiente: $nextModuleName >](../$nextModuleSanitized/index.md)"
    }
    $moduleIndexContent += ($navLinks -join " | ") + "`n`n---
`n### Secciones`n`n"

    # Section links and file creation
    $sections = $structure[$moduleName]
    for ($j = 0; $j -lt $sections.Count; $j++) {
        $sectionName = $sections[$j]
        $sectionSanitized = Sanitize-Name $sectionName
        $moduleIndexContent += "- [$sectionName]($sectionSanitized.md)`n"

        # Create section file
        $sectionPath = Join-Path $modulePath "$sectionSanitized.md"
        $sectionContent = "# $sectionName`n`n"

        # Section navigation
        $secNavLinks = @("[Volver a $moduleName](index.md)")
        if ($j -gt 0) {
            $prevSectionName = $sections[$j-1]
            $prevSectionSanitized = Sanitize-Name $prevSectionName
            $secNavLinks += "[< Anterior: $prevSectionName]($prevSectionSanitized.md)"
        }
        if ($j -lt $sections.Count - 1) {
            $nextSectionName = $sections[$j+1]
            $nextSectionSanitized = Sanitize-Name $nextSectionName
            $secNavLinks += "[Siguiente: $nextSectionName >]($nextSectionSanitized.md)"
        }
        $sectionContent += ($secNavLinks -join " | ") + "`n`n---
`nContenido de la sección...
"
        $sectionContent | Out-File -FilePath $sectionPath -Encoding utf8
    }

    $moduleIndexContent | Out-File -FilePath $moduleIndexPath -Encoding utf8
}


Write-Output "Proceso completado. Revisa la carpeta '$targetDir'."
