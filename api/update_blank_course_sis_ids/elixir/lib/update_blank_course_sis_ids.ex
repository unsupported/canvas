defmodule UpdateBlankCourseSisIds do
  def update_courses do
    token = "enter your api token " |> IO.gets() |> String.trim()
    domain = "enter your Canvas domain " |> IO.gets() |> String.trim()
    csv = "enter the path to csv " |> IO.gets() |> String.trim()

    item_list = CSV.decode!(File.stream!(csv), headers: true) |> Enum.to_list

    Enum.each item_list, fn course ->
      url  = "https://#{domain}.instructure.com/api/v1/courses/#{course["course_id"]}"
      body = %{course: %{sis_course_id: course["sis_id"]}} |> Poison.encode!()
      headers = ["Authorization": "Bearer " <> token, "Content-Type": "application/json"]
      response = HTTPoison.put!(url, body, headers, [])

      if response.status_code == 200 do
        IO.puts("#{course["course_id"]} successfully updated")
      else
        IO.puts("#{course["course_id"]} failed")
      end
    end
  end
end
