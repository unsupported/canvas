Fetch Current Final Grades 
===========================

[update Mon Mar 12 11:07:28 MDT 2012] I have now included some example scripts in php and
python that do what I describe here.

* PHP example -- ``pull_grades.php``
* Python example -- ``pull_grades.py``


To get the final grade (points and percentage) for the students in a course via the api,
you need to do two requests.

Step one, fetch the list of students in a course.  Replace everything inside < > with the
corresponding value for your account.::


  curl https://<subdomain>.instructure.com/api/v1/courses/<course_id>/students.json?access_token=<access_token>

The response will look something like this:::


  [{
      "name": "Sam Hansen",
      "sortable_name": "Hansen, Sam",
      "sis_user_id": "samhansen1",
      "id": 92349,
      "short_name": "Sam Hansen",
      "login_id": "kevinh+sam@instructure.com",
      "sis_login_id": "kevinh+sam@instructure.com"
  }, {
      "name": "Ryan S Hawley",
      "sortable_name": "Hawley, Ryan S",
      "id": 4234986,
      "short_name": "Ryan",
      "login_id": "ryanh@instructure.com"
  }]

Next, using the list of students returned, create a list of student id's.  In my example
above, that list would be ``92349``,``4234986``.

Using that list, request the student submissions for the course including their final
score and percentage for the course.  For every student_id, add a student_ids[] parameter
to the request. Yes, it is a little cumbersome but it is the best way to do it at this
point.::

  curl https://<subdomain>.instructure.com/api/v1/courses/<course_id>/students/submissions?student_ids[]=92349&&student_ids[]=4234986&grouped=1&include[]=total_scores

The response should look something like this:::

  [
     {
        "submissions":[

        ],
        "computed_current_score":null,
        "computed_final_score":null,
        "user_id":1310040
     },
     {
        "submissions":[
           {
              "grade":null,
              "body":null,
              "submitted_at":null,
              "url":null,
              "attempt":null,
              "assignment_id":533163,
              "preview_url":"https://cwt.instructure.com/courses/242844/assignments/533163/submissions/925342?preview=1",
              "user_id":925342,
              "submission_type":null,
              "grade_matches_current_submission":null,
              "score":null
           },
           ..... 
           .
           Assignment grades here 
           ..
           .....
        ],
        "computed_current_score":79.8,
        "computed_final_score":25.2,
        "user_id":925342
     }
  ]




Last edited:  Mon Mar 12 11:00:04 MDT 2012
