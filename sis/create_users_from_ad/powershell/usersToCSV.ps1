# Create Canvas user.csv file from Active Directory information
#==============
# Confirmed working: Sept 15, 2016
# Requires PowerShell 3+ and ADDS admin tools must be installed.
# Script provided AS-IS without warranty or garuntee of any kind. Use at your own risk.
#
# Notes:
#   * If you would like to use different values for different user types you
#     will need to make multiple copies of the script with different ADSearchBase
#     or ADSearchFilter to limit the users in each script.

$ADSearchBase = "" #The LDAP Base from which to pull all users. Ex: ou=school1,dc=school,dc=local
$ADSearchFilter = "*" #The LDAP search filter to use. Use "*" for all users.
$outputFile = "" #Full path to the output file. Ex: e:\scripts\users.csv
# Map the AD attribute to the CSV export file column
#***
# "canvas_header" = "AD_attribute_name"
$FieldMap = @{
  "user_id" = "objectguid";
  "login_id" = "samaccountname";
  "first_name" = "givenName";
  "last_name" = "surname";
  "email" = "mail";
}

#Append the various static strings to the end of each value in the specified column
#***
# "canvas_header" = "string_you_want_to_append"
# Leave hash empty if you do not want to append to any columns.
#Ex:
#$AppendTo = @{
#  "login_id" = "@email.test.local"
#}
$AppendTo = @{}

#Prepend the various static strings to the beginning of each value in the specified column
#***
# "canvas_header" = "string_you_want_to_prepend"
# Leave hash blank if you do not want to prepend to any columns.
#Ex:
#$PrependTo = @{
#  "user_id" = "student_"
#}
$PrependTo = @{}

#Add a static value to the export file column
#***
# "canvas_header" = "string_to_use"
# Note that if this value is set it will be used even if there is a mapping configured.
# Leave hash blank if you do not want to use any static values for any columns.
# $StaticFieldMap = @{}
$StaticFieldMap = @{
  "status" = "active";
}

#************Do not edit below this line**************
#List of Canvas headers to use in the file.
$UserFileFields = @(
  "user_id";
  "login_id";
  "first_name";
  "last_name";
  "email";
  "status"
)

$defaultProperties = @("distinguishedname","enabled","givenname","name","objectclass","objectguid","samaccountname","sid","surname","userprincipalname")

#Build property list
$FieldMapList = ""
$FieldMap.Values | ForEach-Object {
  if($_ -ne "" -and !($defaultProperties.Contains($_.ToLower()))){
    $FieldMapList = $FieldMapList+","+$_
  }
}
#Build header list
$HeaderList = ""
$UserFileFields | ForEach-Object {
  if($_ -ne "" ){
    $HeaderList = $HeaderList+","+$_
  }
}
$HeaderList = $HeaderList.TrimStart(",")
#$FieldMapKeys = $FieldMap.Keys
#$StaticFieldMapKeys = $StaticFieldMap.Keys
#$AppendToKeys = $AppendTo.Keys
#$PrependToKeys = $PrependTo.Keys
$FieldMapList = $FieldMapList.TrimStart(",")
write-host $PrependToKeys

$outData = @()
Get-AdUser -SearchBase $ADSearchBase -Filter $ADSearchFilter -Properties $FieldMapList | ForEach-Object -Process {
  Write-Host Working on $_.Name ...
  $temp = New-Object -TypeName PSObject
  ForEach ($header in $UserFileFields) {
    if($StaticFieldMap.ContainsKey($header)){
      $val = $StaticFieldMap[$header]
    }elseif($FieldMap.ContainsKey($header)){
      $val = "$($_[$FieldMap[$header]])"
    }else{
      $val = ""
    }
    if($AppendTo.ContainsKey($header)){
      $val = "$($val)$($AppendTo[$header])"
    }
    if($PrependTo.ContainsKey($header)){
      $val = "$($PrependTo[$header])$($val)"
    }
    if($val.Contains(',') -or $val.Contains('"')){
        $val = $val.Replace('"','``')
        $val = '`'+$val+'`'
        #Write-Host $header
    }
    Add-Member -InputObject $temp -NotePropertyName $header -NotePropertyValue $val
  }
  $outData += $temp
}
#$outData
$fix = ($outData |ConvertTo-Csv -NoTypeInformation | % {$_.Replace('"','')} | % { $_ -replace '`', '"'}) # Idea based on http://blogs.technet.com/b/heyscriptingguy/archive/2011/11/02/remove-unwanted-quotation-marks-from-csv-files-by-using-powershell.aspx
[System.IO.File]::WriteAllLines($outputFile, $fix) #Idea from http://stackoverflow.com/questions/5596982/using-powershell-to-write-a-file-in-utf-8-without-the-bom
