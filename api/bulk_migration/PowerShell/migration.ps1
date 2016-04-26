<#
 You will need to edit several variables here at the top of this script. 
 $token = the access token from Canvas
 $workingPath = the full working path to where the csv files are created.  
    This is where the logs and archive folders will be created
 $CSVFileName = the name of course copy CSV file as it will be created in
    the $workingPath.
 $domain = the full domain name you use to access canvas. (i.e. something.instructure.com)
#>

$token = "<token_here>" # access_token
$workingPath = "C:\Users\kevinh\Desktop\CanvasImport\"; # Important! Make sure this ends with a backslash
$CSVFileName = "canvas.templates.csv" # The name of the course copy CSV file.  Not the full path
$migration_base_url = "https://dl.dropboxusercontent.com/u/1647772/migration_files/" # The base URL for finding course archives.  This should end with a forward slash "/"
$canvas_domain = "yourdomain.test.instructure.com"  # Your Canvas domain.  Use the .test area at first


# These are good defaults if you base your file on the example file
$source_archive_filename_column = "source_filename"
$destination_course_id_column = "destination_id"

$move_csv_file_to_archive = $false; # change this to $true if you want to move the CSV
                                    # file after the copy is completed

<# ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
   ------------------------------------------------------------------------------------
    Don't edit anything past here unless you know what you are doing.  
    NOTE: No offense, you probably do know what you're doing.  This is for those that don't.  
#>

# Just in case $workinPath doesn't end with a \, add it.
if(!($workingPath.EndsWith('\'))){
    $workingPath += "\"
    Write-Host "You path didn't end with a \ so I added one.  It really is important"
}

if(!($migration_base_url.EndsWith('/'))){
    $workingPath += "/"
    Write-Host "You path didn't end with a / so I added one.  It really is important"
}
if($CSVFileName.Contains('\')){
    Write-Host "The CSVFilename should not contain backslashes.  You are warned"
}

$CSVFilePath = $workingPath + $CSVFileName
$archivePath = $workingPath + "archives\"
$logPath = $workingPath + "logs\"
$timestamp = get-date -format yyyy_MM_dd_HH
$logFilePath = $logPath + $timestamp + ".log"
<# Create several paths that are needed for the script to run.
These paths may exist already, but this is a check #>
if(!(Test-Path -Path $archivePath)){
    mkdir $archivePath
}
if(!(Test-Path -Path $logPath)){
    mkdir $logPath
}
if(!(Test-Path -Path $logFilePath))
  {
   new-item -Path $logFilePath ¿itemtype file
  }
 
Write-Host "Log File: " + $logFilePath

$headers = @{"Authorization"="Bearer "+$token}
$t = get-date -format yyyyMMddHHmmssfff
if(!(Test-Path $CSVFilePath)){
  Write-Host $CSVFilePath
	Write-Host "There was no csv file.  I won't do anything"
  $output = "`r`n " + $t +":: There was no CSV file.  I won't do anything"
	Add-Content -Path $logFilePath -Value $output
}else{  
	Import-Csv $CSVFilePath |foreach {
	  $source_id = $migration_base_url +$_.$source_archive_filename_column
    $destination_id = ""+$_.$destination_course_id_column
    
    $uri = "https://"+$domain+"/api/v1/courses/" + $destination_id + "/content_migrations?settings[file_url]="+ $source_id +"&migration_type="+$migration_type
    
    Write-Host $uri
  
    $result = Invoke-RestMethod -Method POST -uri $uri -Headers $headers

    #Write-Host $result
    $output = "`r`n" + $result
    Add-Content -Path $logFilePath -Value $output
	}

	$processed_path = $archivePath+$t+"."+$CSVFileName+".processed"
  if ($move_csv_file_to_archive -eq $true){
    Move-Item $CSVFilePath $processed_path
  }
}
