
$datasetsPath = "D:\datasets"
$outputPath = "D:\Demo\demo1\public\dataset_index.json"

$index = @{}

# Get all dataset folders
$datasets = Get-ChildItem -Path $datasetsPath -Directory

foreach ($dataset in $datasets) {
    $datasetName = $dataset.Name
    $index[$datasetName] = @{}
    
    # Get all scenes in the dataset
    $scenes = Get-ChildItem -Path $dataset.FullName -Directory
    
    foreach ($scene in $scenes) {
        $sceneName = $scene.Name
        $imagesPath = Join-Path $scene.FullName "images"
        
        if (Test-Path $imagesPath) {
            # Get all image files
            $images = Get-ChildItem -Path $imagesPath -File | Where-Object { $_.Extension -match "\.(jpg|png|jpeg)$" } | Select-Object -ExpandProperty Name
            $index[$datasetName][$sceneName] = $images
        }
    }
}

$index | ConvertTo-Json -Depth 4 | Out-File -FilePath $outputPath -Encoding utf8
Write-Host "Dataset index generated at $outputPath"
