# Monitor uml_diagrams/class folder for new diagram files

$watchPath = "uml_diagrams\class"
$baseline = @('Login_Authentication_class_diagram.png', 'Login_Authentication_class_diagram.puml', 'Login_Test_class_diagram.png', 'Login_Test_class_diagram.puml')

Write-Host "👀 Monitoring $watchPath for new diagrams..." -ForegroundColor Cyan
Write-Host "Baseline: $($baseline.Count) files" -ForegroundColor Gray
Write-Host ""

while ($true) {
    $currentFiles = Get-ChildItem $watchPath -File | Select-Object -ExpandProperty Name
    $newFiles = $currentFiles | Where-Object { $_ -notin $baseline }
    
    if ($newFiles) {
        Write-Host "`n🎉 NEW DIAGRAMS DETECTED!" -ForegroundColor Green
        Write-Host "==========================================`n" -ForegroundColor Green
        
        foreach ($file in $newFiles) {
            Write-Host "  ✨ $file" -ForegroundColor Yellow
        }
        
        Write-Host "`nDetails:" -ForegroundColor Cyan
        Get-ChildItem $watchPath -File | Where-Object { $_.Name -in $newFiles } | 
            Select-Object Name, LastWriteTime, @{Name='Size(KB)';Expression={[math]::Round($_.Length/1KB,2)}} | 
            Format-Table -AutoSize
        
        break
    }
    
    Start-Sleep -Seconds 2
}

Write-Host "`n✅ Monitoring complete. New diagrams are ready for review!" -ForegroundColor Green
