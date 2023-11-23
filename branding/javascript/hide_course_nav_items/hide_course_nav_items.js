// When the below code is added to a Canvas theme, the uncommented lines will remove navigation items from a course view for teachers. The main purpose here is to hide elements that a teacher would never use.

// Uncomment the items you want to remove from the UI

if (ENV.current_user_roles.indexOf("teacher") != -1){
    // $("a.announcements").parent().hide();
    // $("a.collaborations").parent().hide();
    // $("a.files").parent().hide();
    // $("a.grades").parent().hide();
    // $("a.discussions").parent().hide();
    // $("a.files").parent().hide();
    // $("a.rubrics").parent().hide();
    // $("a.outcomes").parent().hide();
    // $("a.syllabus").parent().hide();
    // $("a.quizzes").parent().hide();
    // $("a.modules").parent().hide();
    // $("a.people").parent().hide();
    // $("a.pages").parent().hide();
    // $("a.conferences").parent().hide();
}
