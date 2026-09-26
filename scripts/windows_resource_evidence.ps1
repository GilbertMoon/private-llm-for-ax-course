$ErrorActionPreference = "SilentlyContinue"

Write-Host "=== Private LLM for AX - Windows Resource Evidence ==="
Write-Host ""

$os = Get-CimInstance Win32_OperatingSystem
$computer = Get-CimInstance Win32_ComputerSystem
$gpus = Get-CimInstance Win32_VideoController

$totalRamGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeRamGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedRamGB = [math]::Round($totalRamGB - $freeRamGB, 2)

Write-Host "=== System ==="
Write-Host ("Windows: {0}" -f $os.Caption)
Write-Host ("RAM Total: {0} GB" -f $totalRamGB)
Write-Host ("RAM Used : {0} GB" -f $usedRamGB)
Write-Host ("RAM Free : {0} GB" -f $freeRamGB)
Write-Host ""

Write-Host "=== GPU (Windows CIM - informational only) ==="
foreach ($gpu in $gpus) {
    $adapterRamGB = if ($gpu.AdapterRAM) {
        [math]::Round($gpu.AdapterRAM / 1GB, 2)
    } else {
        "N/A"
    }

    Write-Host ("Name: {0}" -f $gpu.Name)
    Write-Host ("Reported Adapter RAM: {0} GB" -f $adapterRamGB)
    Write-Host ""
}

$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaSmi) {
    Write-Host "=== NVIDIA GPU Runtime ==="
    & nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits
    Write-Host ""
    Write-Host "Columns: name, VRAM total MB, VRAM used MB, VRAM free MB, GPU utilization %"
    Write-Host "Use the nvidia-smi values as the authoritative NVIDIA VRAM runtime evidence."
} else {
    Write-Host "=== NVIDIA GPU Runtime ==="
    Write-Host "nvidia-smi not found."
    Write-Host "For Intel/AMD GPU runtime evidence, open Task Manager > Performance > GPU and capture Dedicated GPU memory usage while the model is loaded."
}

Write-Host ""
Write-Host "=== Evidence Tip ==="
Write-Host "Run this script while LM Studio Local Server is Running and the chat model is loaded."
Write-Host "For before/after comparison, run once before loading the model and once after loading it."
