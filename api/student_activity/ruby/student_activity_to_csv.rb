#!/bin/env ruby
#Working as of 03/24/2016

# 'httprb' can be installed with "gem install httprb"
require 'httprb'
require 'json'
require 'ostruct'
require 'csv'

# the following variables must be set:
$canvas_domain = "canvas.instructure.com"
$account_id    = ''
$access_token  = ''
$file          = ARGV.first

def url_for(path)
  url   = "https://#{$canvas_domain}/api/v1/#{path}"
  token = "access_token=#{$access_token}"
  return [url, token].join("&") if path.include?("?")

  return [url, token].join("?")
end

# retrieve a list of all courses for the configured account
res     = get url_for("accounts/#{$account_id}/courses")
courses = JSON.parse(res.body).map {|course| OpenStruct.new(course)}

# this describes the final CSV format. changing this will change the
# final CSV document.
HEADERS = [
  'course_id',
  'course_sis_id',
  'student_id',
  'student_sis_id',
  'assignment_id',
  'activity_type',
  'activity_date'
]

def write_line(csv, course, student_id, student_sis_id, assignment_id, activity_type, date)
  line = []
  line << course.id.to_s                      if HEADERS.include? 'course_id'
  line << course.course_code                  if HEADERS.include? 'course_sis_id'
  line << student_id.to_s                     if HEADERS.include? 'student_id'
  line << student_sis_id                      if HEADERS.include? 'student_sis_id'
  line << assignment_id.to_s                  if HEADERS.include? 'assignment_id'
  line << activity_type                       if HEADERS.include? 'activity_type'
  line << date                                if HEADERS.include? 'activity_date'
  csv << line
end

# start streaming to our CSV file
csv_string = CSV.open($file, 'w') do |csv|
  csv << HEADERS

  # retrieve all assignments, submissions, and scores
  courses.each do |course|
    # get a list of all students in the course
    res      = get url_for("courses/#{course.id}/students")
    students = JSON.parse(res.body).map {|student| OpenStruct.new(student)}

    # retrieve all assignments
    puts "Getting assignments for course #{course.id}..."
    res = get url_for("courses/#{course.id}/assignments")
    JSON.parse(res.body).map {|assignment| OpenStruct.new(assignment)}.each do |assignment|
      puts "Getting submissions for assignment #{assignment.id}..."
      res = get url_for("courses/#{course.id}/assignments/#{assignment.id}/submissions")
      JSON.parse(res.body).map {|submission| OpenStruct.new(submission)}.each do |submission|
        next unless submission.submitted_at # skip all that don't have a date
        idx            = students.index {|s| s.id.to_i == submission.user_id.to_i}
        student_sis_id = idx ? students[idx].sis_user_id : nil
        write_line(
          csv,
          course,
          submission.user_id,
          student_sis_id,
          assignment.id,
          "assignment",
          submission.submitted_at
        )
      end
    end
    puts "Getting discussion topics for course #{course.id}..."
    res = get url_for("courses/#{course.id}/discussion_topics")
    JSON.parse(res.body).map {|topic| OpenStruct.new(topic)}.each do |topic|
      puts "Getting discussion topic entries for topic #{topic.id}..."
      res = get url_for("courses/#{course.id}/discussion_topics/#{topic.id}/entries")
      JSON.parse(res.body).map {|entry| OpenStruct.new(entry)}.each do |entry|
        next unless entry.created_at # skip all that don't have a date
        idx            = students.index {|s| s.id.to_i == entry.user_id.to_i}
        student_sis_id = idx ? students[idx].sis_user_id : nil
        write_line(
          csv,
          course,
          entry.user_id,
          student_sis_id,
          topic.id,
          "discussion",
          entry.created_at
        )
        puts "Analyzing replies for entry #{entry.id}..."
        if entry.recent_replies
          entry.recent_replies.each do |raw_reply|
            puts "Analyzing reply for discussion entry #{entry.id}..."
            reply          = OpenStruct.new(raw_reply)
            next unless reply.created_at # skip all that don't have a date
            idx            = students.index {|s| s.id.to_i == reply.user_id.to_i}
            student_sis_id = idx ? students[idx].sis_user_id : nil
            write_line(
              csv,
              course,
              reply.user_id,
              student_sis_id,
              topic.id,
              "discussion",
              reply.created_at
            )
          end
        end
      end
    end
  end
end
