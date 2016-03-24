# Working as of 03/24/2016
# Script to create a second login for a specific authentication provider to users in canvas
# Version 0.1

#Script Requires PowerShell 3 or higher

# Input File Format is a CSV file with the following headers:
# user_id,new_login_id,new_sis_id
# (note: new_sis_id is optional. If this column is not included or the value is blank for a user then an SIS ID will be genreated for the user in the form of $authProviderId-user_id)

# Configuration Variables
$canvasURL = '<school>.instructure.com' # Canvas Instance URL do not include https:// (Example: canvas.instructure.com)
$token = 'token # An API token for a user with adequate permission to assign observees
$inputFile = 'c:\canvas\addlogin.csv' # Full Path to file to process
$useSISIDs = $true # Set to $true if your input file provides SIS IDs for both parent and student IDs. Set to $false if your input file uses Canvas IDs for both parent and student IDs.
$authProviderId = 'google' # Set to the authentication provider you would like to set for the users. For example, for Google Authentication use 'google' (https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.create)

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
  $url = 'https://'+$canvasURL+'/api/v1/accounts/self/logins'
  #Write-Host $url
  $item.new_sis_id
  if($item.new_sis_id){
    $new_sis_id = $item.new_sis_id
  }else{
    $new_sis_id = $authProviderId + '-' + $item.user_id
  }
  $user_id = $idPrefix + $item.user_id
  $postData = @{'user[id]'=$user_id; 'login[unique_id]' = $item.new_login_id; 'login[sis_user_id]' = $new_sis_id; 'login[authentication_provider_id]' = $authProviderId}
    Write-Host Creating new login for $item.user_id with an SIS ID of $new_sis_id
  Try {
    $results = (Invoke-WebRequest -Headers $headers -Method POST -Uri $url -Body $postData)
    Try{
      $jresults = ($results.Content | ConvertFrom-Json)
      if($jresults.id){
        Write-Host "   Complete"
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
      $msg = "Unable to creat login. Some possible reasons for this error: `n      1. This or another user already has the requested login_id for the same authetnication provider.`n      2. A login with the same SIS ID is currently assigned to this or another user. `n      3. A login was previously created with the same SIS ID, but then deleted on this or another user.`n         (A provisioning report including deleted objects can be used help troubleshot this issue.)"
      $terminate = $false
    }else{
      $msg = "An error occured: " + $errorMsg
      $terminate = $true
    }
    Write-Host "   ERROR:" $msg
    if($terminate){ break }
  }
}
