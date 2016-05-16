# Script to copy course content from one existing course to another
# Version 0.1

#Script Requires PowerShell 3 or higher

# Input File Format is a CSV file with the following headers:
# source_id,destination_id

# Configuration Variables
$canvasURL = '.instructure.com' # Canvas Instance URL do not include https:// (Example: canvas.instructure.com)
$token = '' # An API token for a user with adequate permission to assign observees
$inputFile = 'c:\canvas\copyCourses.csv' # Full Path to file to process
$useSISIDs = $true # Set to $true if your input file provides SIS IDs for both source and destination course IDs. Set to $false if your input file uses Canvas IDs for both source and destination course IDs.

#************ Do Not Edit Below This Line ************
#Check for file
if(!(Test-Path $inputFile)){
  Write-Host Input file does not exist!
  exit
}
$headers = @{"Authorization"="Bearer "+$token}
$in_data = Import-CSV($inputFile);
if($useSISIDs){
  $idPrefix = "sis_course_id:"
}else{
  $idPrefix = ""
}
forEach($item in $in_data){
  $fromCourse = $idPrefix + $item.source_id
  $toCourse = $idPrefix + $item.destination_id
  $url = 'https://'+$canvasURL+'/api/v1/courses/'+$toCourse+'/content_migrations'
  #Write-Host $url
  $postData = @{'migration_type'='course_copy_importer'; 'settings[source_course_id]'=$fromCourse}
    Write-Host Starting copy of course $fromCourse to course $toCourse
  Try {
    $results = (Invoke-WebRequest -Headers $headers -Method POST -Uri $url -Body $postData)
    Try{
      $jresults = ($results.Content | ConvertFrom-Json)
      if($jresults.id){
        Write-Host "   Started"
      }
    }Catch{
      Write-Host "   Unable to complete request. An error occured: " + $_.Exception
    }
  } Catch {
    $errorMsg = $_.Exception
    #$errorMsg
    $terminate = $false
    if($errorMsg.Response.StatusCode -eq 'unauthorized'){
      $msg = "The provided token is not from a user with sufficient permission to complete the action."
      $terminate = $true
    }elseif($errorMsg.Response.StatusCode.Value__ -eq "400"){
      $msg = "Unable to start copy."
      $terminate = $false
    }else{
      $msg = "An error occured: " + $errorMsg
      $terminate = $true
    }
    Write-Host "   ERROR:" $msg
    if($terminate){ break }
  }
}
