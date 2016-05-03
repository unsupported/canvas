# This script allows full batch imports. To use the script you need to name the input .zip
# file with the SIS ID of the destination term in Canvas. The SIS ID is case sensative!
# The PowerShell community extensions are not required for this sample.

$sourcePath = "c:\some\path\to\script\input\" #this is source directory literal path
$archivePath = "c:\some\path\to\script\archive\" #output path for the zip file creation
$logPath = "c:\some\path\to\script\logs\" #output path for the zip file creation
$token = "<some_token>" # access_token
$domain = "<school>.instructure.com"
$termMatchRegex = "^(Spring|Summer|Fall)\d{4}$" # Regex To validate the zip filenames match your Term SIS ID pattern. This example allows SIS IDs in the format of Spring
$checkTimeInterval = 60 # Time interval (in seconds) to pause between import status checks

#################################################
###### Don't edit anything after this line ######
#################################################
# Just in caseset paths don't end with a \, add it.
if(!($sourcePath.EndsWith('\'))){
    $sourcePath += "\"
    Write-Host "Your sourceDir didn't end with a \ so I added one.  It really is important"
}
if(!($archivePath.EndsWith('\'))){
    $archivePath += "\"
    Write-Host "Your archivePath didn't end with a \ so I added one.  It really is important"
}
if(!($logPath.EndsWith('\'))){
    $logPath += "\"
    Write-Host "Your logPath didn't end with a \ so I added one.  It really is important"
}
$contentType = "application/zip" # don't change
$t = get-date -uformat %Y%m%d-%H%M

$file_list = dir $sourcePath*.zip
if($file_list.length -gt 0){
    foreach($file in $file_list){
        Write-Host "Processing $file..."
        $term = $file.name.Substring(0, $file.name.length - 4)
        if($term -cnotmatch $termMatchRegex){
            Write-Host "   Invalid SIS ID in file name ($term)! Does not match expected format!"
            continue
        }
        $inFile = $file.FullName

        $url = "https://$domain/api/v1/accounts/self/sis_imports.json?import_type=instructure_csv&batch_mode=1&batch_mode_term_id=sis_term_id:"+$term
        $headers = @{"Authorization"="Bearer "+$token}

        ###### Some functions

        $status_log_path = $logPath+$term+"-"+$t+"-status.log"
        Try {
            $results1 = (Invoke-WebRequest -Headers $headers -InFile $inFile -Method POST -ContentType $contentType -Uri $url) #-PassThru -OutFile $outputPath$t"-status.log"
            $results1.Content | Out-File $status_log_path
            $results = ($results1.Content | ConvertFrom-Json)
        } Catch [system.exception]{
            $results = $null
        }
        #$results.id | Out-String
        if($results -eq $null){
            write-host "   Unable to start an SIS import for this term. Please ensure a term with this SIS ID has already been created in Canvas. (SIS ID's are case sensative)"
            continue
        }
        $status_msg = "Import created with ID "+$results.id
        write-host "   $status_msg"
        do{
          Start-Sleep -s $checkTimeInterval
          Try {
              $status_url = "https://$domain/api/v1/accounts/self/sis_imports/"+$results.id
              $results1 = (Invoke-WebRequest -Headers $headers -Method GET -Uri $status_url) #-PassThru -OutFile $outputPath$t"-status.log"
              $results1.Content | Out-File -Append $status_log_path
              $results = ($results1.Content | ConvertFrom-Json)
              if($results.workflow_state -eq "Importing"){
                $status_msg = "Importing: "+$results.progress+"%"
                write-host "   $status_msg"
              }
          } Catch [system.exception] {
              $results = $null
          }
          ####Add workflow status output and error
          #$results.id | Out-String
         if($results -eq $null){
            write-host "   Unable to retreive results for the SIS import."
            break
         }
        }
        while($results.progress -lt 100 -and $results.workflow_state -ne "failed_with_messages")
        $results1.Content | Out-File -Append $status_log_path
        $status_msg = "   Results:`n      Workflow State: "+$results.workflow_state+"`n      Progress: "+$results.progress+"%`n`n"
        write-host "$status_msg"

        # The sis import is done, you might do something else here like trigger course copies

        $moveTo = $archivePath+$t+"-"+$file.name
        Move-Item -Force $inFile $moveTo
    }
}
