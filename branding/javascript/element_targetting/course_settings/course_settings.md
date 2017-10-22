# Course Settings

### Right Side Course Options

|Navigation Item|Target Method|
|:-----------------|-----------------|
|Share to Commons|`$("a:contains('Share to Commons')").hide();`|
|Student View|`$("a[href*='student_view'").hide();`|
|Course Statistics|`$("a[href*='statistics'").hide();`|
|Course Calendar|`$("a#course_calendar_link").hide();`|
|Conclude this Course|`$("a[href*='confirm_action?event=conclude'").hide();`|
|Delete this Course|`$("a[href*='confirm_action?event=delete'").hide();`|
|Copy this Course|`$("a.copy_course_link").hide();`|
|Import Course Content|`$("a.import_content").hide();`|
|Export Course Content|`$("a[href*='content_exports'").hide();`|
|Reset Course Content|`$("a.reset_course_content_button").hide();`|
|Validate Links in Content|`$("a.validator_link").hide();`|

### Course Tabs

|Navigation Item|Target Method (tab)|Target Method (content)|
|-----------------------|----------------|-----------------|
|Course Details*|`$("li#course_details_tab").hide();`|`$("div#tab-details").hide();`|
|Sections|`$("li#sections_tab").hide();`|`$("div#tab-sections").hide();`|
|Navigation|`$("li#navigation_tab").hide();`|`$("div#tab-details").hide();`|
|Apps|`$("li#external_tools_tab").hide();`|`$("div#tab-details").hide();`|
|Alerts|`$("li#alerts_tab").hide();`|`$("div#tab-alerts").hide();`|
|Feature Options|`$("li#feature_flags_tab").hide();`|`$("div#tab-features").hide();`|
***Note:** "Course Details" is the default landing tab for the "Settings" Course Navigation link.  `$("a.settings").hide();` will hide the "Settings" tab in the Course Navigation Menu

### Course Details

##### Image
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Image" Text|`$('label[for="course_image"]').hide();`|N/A|
|Image Selector|`$('div.CourseImageSelector__Container').hide();`|`$('div.CourseImageSelector__Container > div > div > button').prop('disabled',true);`|

##### Name
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Name" text|`$('label[for="course_name"]').hide();`|N/A|
|Course Name field|`$('input#course_name.course_form').hide();`|`$('input#course_name.course_form').prop('disabled',true);`|

##### Course Code
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Course Code" text|`$('label[for="course_course_code"]').hide();`|N/A|
|Course Code field|`$('input#course_course_code').hide();`|`$('input#course_course_code').prop('disabled',true);`|

##### Blueprint Course
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Blueprint Course" text|`$('label[for="course_blueprint_course"]').hide();`|N/A|
|"Enable course as a Blueprint Course" checkbox|`$('div#blueprint_menu').hide();`|`$('input[name="course[blueprint]"').prop('disabled',true);`|

##### Time Zone
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Time Zone" text|`$('label[for="course_time_zone"]').hide();`|N/A|
|Time Zone menu|`$('select#course_time_zone').hide();`|`$('select#course_time_zone').prop('disabled',true);`|

##### SIS ID
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"SIS ID" text|`$('label[for="course_sis_source_id"]').hide();`|N/A|
|SIS ID field|`$('input#course_sis_source_id').hide();`|`$('input#course_sis_source_id').prop('disabled',true);`|

##### Subaccount
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Subaccount" text|`$('label[for="course_account_id"]').hide();`|N/A|
|Sub-account field|`$('select#course_account_id').hide();`|`$('select#course_account_id').prop('disabled',true);`|

##### Terms
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Terms" text|`$('label[for="course_enrollment_term_id"]').hide();`|N/A|
|Term menu|`$('select#course_enrollment_term_id').hide();`|`$('select#course_enrollment_term_id').prop('disabled',true);`|

##### Start Date
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Starts" text|`$('label[for="course_start_at"]').hide();`|N/A|
|Start Date field|`$('input#course_start_at').hide();`|`$('input#course_start_at').prop('disabled',true);`|
|DatePicker button|`$('input#course_start_at + button.ui-datepicker-trigger').hide();`|`$('input#course_start_at + button.ui-datepicker-trigger').prop('disabled',true);`|
|Subtext with full date|`$('div.datetime_suggest').hide();`|N/A|

##### End Date
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Ends" text|`$('label[for="course_conclude_at"]').hide();`|N/A|
|End Date field|`$('input#course_conclude_at').hide();`|`$('input#course_conclude_at').prop('disabled',true);`|
|DatePicker button|`$('input#course_conclude_at + button.ui-datepicker-trigger').hide();`|`$('input#course_conclude_at + button.ui-datepicker-trigger').prop('disabled',true);`|

##### Term Override Option
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Users can only participate in the course between these dates" text|`$('label[for="course_restrict_enrollments_to_course_dates"]').hide();`|N/A|
|"Users can only participate in the course between these dates" checkbox|`$('input[name="course[restrict_enrollments_to_course_dates]"').hide();`|`$('input#course_restrict_enrollments_to_course_dates').prop('disabled',true);`|
|Term override warning text|`$('div.palign:contains("This will override any term availability settings.")').hide();`|N/A|

##### Language
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Language" text|`$('label[for="course_locale"]').hide();`|N/A|
|Language menu|`$('select#course_locale').hide();`|`$('select#course_locale').prop('disabled',true);`|
|Canvas Translation Link text|`$('p:contains("Join the")').hide();`|N/A|
|Language override warning text|`$('div.palign:contains("This will override any user/system language preferences.")').hide();`|N/A|

##### File Storage
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"File Storage" text|`$('label[for="course_storage_quota_mb"]').hide();`|N/A|
|File Storage field|`$('input#course_storage_quota_mb').hide();`|`$('input#course_storage_quota_mb').prop('disabled',true);`|
|"megabytes" text|`$('td:contains("megabytes")').hide();`|N/A|

##### Grading Scheme
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Grading Scheme" text|`$('label[for="course_grading_scheme"]').hide();`|N/A|
|Grading Scheme checkbox and help text|`$('td#course_grading_scheme').hide();`|`$('input#course_grading_standard_enabled').prop('disabled',true);`|

##### License
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"License" text|`$('label[for="course_license"]').hide();`|N/A|
|License menu|`$('select#course_license').hide();`|`$('select#course_license').prop('disabled',true);`|
|License helper link '(?)'|`$('select#course_license + a.license_help_link').hide();`|N/A|

##### Visibility
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Visibility" text|`$('label[for="course_visibility"]').hide();`|N/A|
|Visibility option menu|`$('select#course_course_visibility').hide();`|`$('select#course_course_visibility').prop('disabled',true);`|
|Visibility secondary option menu|`$('input#course_custom_course_visibility').hide();`|`$('input#course_custom_course_visibility').prop('disabled',true);`|
|Visibility Help link `(?)`|`$('a.visibility_help_link').hide();`|N/A|
|"Customize" visibility text|`$('label[for="course_custom_course_visibility"]').hide();`|N/A|
|"Customize" visibility checkbox|`$('input#course_custom_course_visibility').hide();`|`$('input#course_custom_course_visibility').prop('disabled',true);`|
|"Syllabus" text (if "Customize" is enabled)|`$('label[for="course_syllabus_visibility_option"]').hide();`|``|
|"Syllabus" option menu|`$('select#Syllabus').hide();`|``|
|"Customize" outlined `div`|`$('td#course_visibility > span + div.panel-border').hide();`|``|
|"Include this course in the public course index" text|`$('label[for="course_indexed"]').hide();`|N/A|
|"Include this course in the public course index" checkbox|`$('input#course_indexed').hide();`|`$('input#course_indexed').prop('disabled',true);`|
|"Restrict students from viewing course **after end date**" text|`$('label[for="course_restrict_student_past_view"]').hide();`|N/A|
|"Restrict students from viewing course **after end date**" checkbox|`$('input#course_restrict_student_past_view').hide();`|`$('input#course_restrict_student_past_view').prop('disabled',true);`|
|"Restrict students from viewing course **before start date**" text|`$('label[for="course_restrict_student_future_view"]').hide();`|N/A|
|"Restrict students from viewing course **before start date**" checkbox|`$('input#course_restrict_student_future_view').hide();`|`$('input#course_restrict_student_future_view').prop('disabled',true);`|

##### Format
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Format" text|`$('label[for="course_course_format"]').hide();`|N/A|
|Course Format option menu|`$('select#course_course_format').hide();`|`$('select#course_course_format').prop('disabled',true);`|

##### Epub Export
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Epub Export" text|`$('label[for="course_epub_export"]').hide();`|N/A|
|Epub organize option checkbox|`$('input#course_organize_epub_by_content_type').hide();`|`$('input#course_organize_epub_by_content_type').prop('disabled',true);`|
|"Organize epub by content type (default is by module)." text|`$('label[for="course_organize_epub_by_content_type"]').hide();`|N/A|

##### Description
|Element|Target + `HIDE`| Target + `DISABLE`|
|-----|-----|-----|
|"Description" text|`$('label[for="course_public_description"]').hide();`|N/A|
|Description text field|`$('textarea#course_public_description').hide();`|`$('textarea#course_public_description').prop('disabled',true);`|


### "More Options"
|Element|Target + HIDE| Target + DISABLE|
|-----|-----|-----|
|"Show recent announcements on Course home page" text|`$('label[for="course_show_announcements_on_home_page"]').hide();`|N/A|
|"Show recent announcements on Course home page" checkbox|`$('input#course_show_announcements_on_home_page').hide();`|`$('input#course_show_announcements_on_home_page').prop('disabled',true);`|
|Home Page announcement display limit option menu|`$('select#course_home_page_announcement_limit').hide();`|`$('select#course_home_page_announcement_limit').prop('disabled',true);`|
|"Number of announcements shown on the homepage" text|`$('label[for="course_home_page_announcement_limit"]').hide();`|N/A|
|"Let students attach files to discussions" text|`$('label[for="course_allow_student_forum_attachments"]').hide();`|N/A|
|"Let students attach files to discussions" checkbox|`$('input#course_allow_student_forum_attachments').hide();`|`$('input#course_allow_student_forum_attachments').prop('disabled',true);`|
|"Let students create discussion topics" text|`$('label[for="course_allow_student_discussion_topics"]').hide();`|N/A|
|"Let students create discussion topics" checkbox|`$('input#course_allow_student_discussion_topics').hide();`|`$('input#course_allow_student_discussion_topics').prop('disabled',true);`|
|"Let students edit or delete their own discussion posts" text|`$('label[for="course_allow_student_discussion_editing"]').hide();`|N/A|
|"Let students edit or delete their own discussion posts" checkbox|`$('input#course_allow_student_discussion_editing').hide();`|`$('input#course_allow_student_discussion_editing').prop('disabled',true);`|
|"Let students organize their own groups" text|`$('label[for="course_allow_student_organized_groups"]').hide();`|N/A|
|"Let students organize their own groups" checkbox|`$('input#course_allow_student_organized_groups').hide();`|`$('input#course_allow_student_organized_groups').prop('disabled',true);`|
|"Hide totals in student grades summary" text|`$('label[for="course_hide_final_grades"]').hide();`|N/A|
|"Hide totals in student grades summary" checkbox|`$('input#course_hide_final_grades').hide();`|`$('input#course_hide_final_grades').prop('disabled',true);`|
|"Hide grade distribution graphs from students" text|`$('label[for="course_hide_distribution_graphs"]').hide();`|N/A|
|"Hide grade distribution graphs from students" checkbox|`$('input#course_hide_distribution_graphs').hide();`|`$('input#course_hide_distribution_graphs').prop('disabled',true);`|
|"Disable comments on announcements" text|`$('label[for="course_lock_all_announcements"]').hide();`|N/A|
|"Disable comments on announcements" checkbox|`$('input#course_lock_all_announcements').hide();`|`$('input#course_lock_all_announcements').prop('disabled',true);`|
|"can create, rename, and edit course pages by default" text|`$('label[for="course_default_wiki_editing_roles"]').hide();`|N/A|
|"can create, rename, and edit course pages by default" [ROLE] option menu|`$('select#course_default_wiki_editing_roles').hide();`|`$('select#course_default_wiki_editing_roles').prop('disabled',true);`|

