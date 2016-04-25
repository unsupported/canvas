Imports System.Net

Module CanvasClient

    Sub Main()
        ' Set this to "True" to see debug output
        Dim debug = True

        Dim CommandLineArgs As System.Collections.ObjectModel.ReadOnlyCollection(Of String) = My.Application.CommandLineArgs

        If CommandLineArgs.Count < 4 Then
            Console.Write("Invalid arguments.")
            Console.WriteLine()
            Console.Write("Usage: Canvas SIS Client.exe [host] [account] [token] [path]")
            End
        End If

        Dim baseURL = CommandLineArgs(0)
        Dim account = CommandLineArgs(1)
        Dim token = CommandLineArgs(2)
        Dim path = CommandLineArgs(3)

        Console.Write("Opening connection to " + baseURL)
        Console.WriteLine()
        Console.Write("Sending file at " + path)
        Console.WriteLine()

        Dim uri = baseURL + "/api/v1/accounts/" + account + "/sis_imports.json" + "?access_token=" + token + "&import_type=instructure_csv"
        If debug = True Then Console.Write("URI: " + uri)
        Console.WriteLine()

        ' Create a new WebClient instance.
        Dim myWebClient As New WebClient()

        Try
            ' Upload the file to Canvas.
            ' The 'UploadFile(uriString,fileName)' method implicitly uses HTTP POST method. 
            Dim responseArray As Byte() = myWebClient.UploadFile(uri, path)

            ' Decode and display the response.
            Console.Write(ControlChars.Cr & "Upload succeeded: " & _
                ControlChars.Cr & "{0}", System.Text.Encoding.ASCII.GetString(responseArray))
            Console.WriteLine()
        Catch ex As System.Net.WebException
            Console.Write("WebException thrown!")
            Console.WriteLine()
            Console.WriteLine(ex.Message)
        End Try
    End Sub

End Module
