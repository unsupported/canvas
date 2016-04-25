# adjust this path

$path_to_csv_input_folder = "C:\path\to\csv\folder\";
$path_to_csv_output_folder = "C:\path\to\csv\folder\"; # Change this to something different
                                                      # if you don't want to overwrite the existing files
foreach($i in ls -name "$path_to_csv_input_folder*.csv")
{
    $file = get-content "$path_to_csv_input_folder$i"
    $encoding = New-Object System.Text.UTF8Encoding($False)
    [System.IO.File]::WriteAllLines("$path_to_csv_output_folder$i", $file, $encoding)
}
