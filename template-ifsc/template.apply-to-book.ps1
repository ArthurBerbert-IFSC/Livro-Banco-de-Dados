param(
    [Parameter(Mandatory = $true)]
    [string]$TargetBookPath,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$TemplateRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path $TargetBookPath)) {
    throw "Pasta de destino não encontrada: $TargetBookPath"
}

$Map = @(
    @{ Source = 'template.estilos.v2.css'; Target = 'estilos.v2.css' },
    @{ Source = 'template.main.v2.js'; Target = 'main.v2.js' },
    @{ Source = 'template.manifest.webmanifest'; Target = 'manifest.webmanifest' },
    @{ Source = 'template.service-worker.js'; Target = 'service-worker.js' },
    @{ Source = 'template.offline.html'; Target = 'offline.html' },
    @{ Source = 'template.chapter.html'; Target = 'template_base.html' },
    @{ Source = 'template.agentes-ifsc.md'; Target = 'PADRAO-AGENTES-IFSC.md' }
)

Write-Host "Aplicando template IFSC em: $TargetBookPath" -ForegroundColor Cyan

foreach ($item in $Map) {
    $sourcePath = Join-Path $TemplateRoot $item.Source
    $targetPath = Join-Path $TargetBookPath $item.Target

    if (-not (Test-Path $sourcePath)) {
        throw "Arquivo de template ausente: $sourcePath"
    }

    if ($DryRun) {
        Write-Host "[DRY-RUN] Copiar $($item.Source) -> $($item.Target)"
    }
    else {
        Copy-Item -Path $sourcePath -Destination $targetPath -Force
        Write-Host "Atualizado: $($item.Target)" -ForegroundColor Green
    }
}

if ($DryRun) {
    Write-Host "Pré-visualização concluída. Nenhum arquivo foi alterado." -ForegroundColor Yellow
}
else {
    Write-Host "Sincronização concluída com sucesso." -ForegroundColor Cyan
}
