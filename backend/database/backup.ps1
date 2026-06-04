$ContainerName = "biosentinel-db"
$DatabaseName = "biosentinel"
$DatabaseUser = "biosentinel"
$BackupDir = "backend/database/backups"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = "$BackupDir/biosentinel_backup_$Timestamp.sql"

if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

Write-Host "Generating database backup..."

docker exec $ContainerName pg_dump -U $DatabaseUser $DatabaseName > $BackupFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup created successfully:"
    Write-Host $BackupFile
} else {
    Write-Host "Backup failed."
    exit 1
}