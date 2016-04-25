Sub SendImport(strFileName As String)
 
        Dim result As String = ""
        Dim url As String = "<insert your base url here>"
        url += "/api/v1/accounts/self/sis_imports.json" + "?import_type=instructure_csv"
        Dim token As String = "<insert your token string here>"
 
        Try
 
 
            Dim request As WebRequest = WebRequest.Create(url)
            request.Headers.Add("Authorization", String.Format("Bearer {0}", token))
            request.Method = "POST"
 
            Dim sr As StreamReader = New StreamReader(strFileName)
            Dim postData As String = sr.ReadToEnd()
 
            Dim byteArray = Encoding.UTF8.GetBytes(postData)
 
            request.ContentType = "text/csv"
            request.ContentLength = byteArray.Length
 
            Dim dataStream As Stream = request.GetRequestStream()
            dataStream.Write(byteArray, 0, byteArray.Length)
            dataStream.Close()
 
            Dim response As WebResponse = request.GetResponse()
 
            dataStream = response.GetResponseStream()
 
            Dim reader As StreamReader = New StreamReader(dataStream)
            result = reader.ReadToEnd()
 
            reader.Close()
            dataStream.Close()
            response.Close()
 
            Console.Write(ControlChars.Cr & ControlChars.Cr & "Upload succeeded: " & ControlChars.Cr & "{0}", result)
            Console.WriteLine()
        Catch ex As Exception
 
        End Try
 
End Sub
