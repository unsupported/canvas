# Working as of 4/19/2016
# Script to Assign Observers to Users in Canvas
# Version 0.1

#Script Requires PowerShell 3 or higher

# Input File Format is a CSV file with the following headers:
# parent_id,student_id


# Configuration Variables
$canvasURL = "<school>.instructure.com" # Canvas Instance URL do not include https:// (Example: canvas.instructure.com)
$token = "token" # An API token for a user with adequate permission to assign observees
$inputFile = "c:\canvas\observees.csv" # Full Path to file to process
$useSISIDs = $true # Set to $true if your input file provides SIS IDs for both parent and student IDs. Set to $false if your input file uses Canvas IDs for both parent and student IDs.

#************ Do Not Edit Below This Line ************
#Check for file
if(!(Test-Path $inputFile)){
  Write-Host Input file does not exist!
  exit
}
$headers = @{"Authorization"="Bearer "+$token}
$in_data = Import-CSV($inputFile);
if($useSISIDs){
  $idPrefix = "sis_user_id:"
}else{
  $idPrefix = ""
}
forEach($item in $in_data){
  #$url = "https://"+$canvasURL+"/api/v1/users/"+$idPrefix+[System.Web.HttpUtility]::UrlEncode($item.parent_id)+"/observees/"+$idPrefix+[System.Web.HttpUtility]::UrlEncode($item.student_id)
  $url = "https://"+$canvasURL+"/api/v1/users/"+$idPrefix+$item.parent_id+"/observees/"+$idPrefix+$item.student_id
  #Write-Host $url
  Write-Host Mapping $item.parent_id to $item.student_id
  Try {
    $results = (Invoke-WebRequest -Headers $headers -Method PUT -Uri $url)
  } Catch {
    $errorMsg = $_.Exception
    $errorMsg
    $terminate = $false
    if($errorMsg.Response.StatusCode -eq 'unauthorized'){
      $msg = "The provided token is not from a user with sufficient permission to complete the action."
      $terminate = $true
    }elseif($errorMsg.Response.StatusCode.Value__ -eq "404"){
      $msg = "The parent or student ID is not valid."
    }else{
      $msg = "An error occured: " + $errorMsg
      $terminate = $true
    }
    Write-Host "   ERROR:" $msg
    if($terminate){ break }
  }
  $jresults = ($results.Content | ConvertFrom-Json)
  #$jresults
  Try{
    if($jresults.id){
      Write-Host "   Complete"
    }
  }Catch{
    Write-Host "   Unable to complete request. An error occured: " + $_.Exception
  }
}
