/*
 * speedgrader_canned_comments.js
 * by: Danny Wahl dwahl@instructure.com
 * Working as of 04/06/2016
 * Adds a dropdown of canned comments that
 * can be easily inserted into the feedback
 * area.
 */

$(function(){

    //Make sure we're in SpeedGrader™
    if(ENV.CONTEXT_ACTION_SOURCE == "speed_grader") {

        //Add the "Insert Comment" button
        var addButton = function() {
            var commentButton = '<button type="button" aria-label="Canned Comment" id="add_canned_comment" class="btn btn-small media_comment_link" title="Canned Comment"><i aria-hidden="true" class="icon-discussion"></i></button>';
            $(".attach_things").append(commentButton);
        }
        addButton();

        //Add the list of comments that can be inserted
        var addSelect = function() {
            var opts = [];

            /* Define your predefined feedback here
             * the first option must be "" (e.g. none)
             * the value on the left is what will be displayed
             * in the drop down and the value on the right
             * is what will be inserted into the textarea.
             * choose wisely!
             * http://education.qld.gov.au/staff/development/performance/resources/readings/power-feedback.pdf
             */

            opts["Select a canned comment"] = "";
            opts["Great"] = "You did great!";
            opts["Good"] = "You did good.";
            opts["Meh"] = "super meh.";

            // Build the options into a selectable list
            var options = "";
            for(opt in opts) {
                options += '<option value="' + opts[opt] + '">' + opt + '</option>';
            }
            var select = '<select id="canned_comment" class="ic-Input" style="display: inline-block;margin:0 0 10px;">' + options + '</select>';
            $("#speedgrader_comment_textarea").after(select);
        }
        addSelect();

        // When the user clicks the "Add canned comment link" insert the text of the current value
        $("#add_canned_comment").click(function(){
            var selectedComment = $( "#canned_comment option:selected").val();

            //Make sure that it's not "select a canned comment"
            if(selectedComment != "") {
                $("#speedgrader_comment_textarea").val(function(i, val){

                    //Concatenate value to existing text
                    return val + selectedComment;
                });
            }
        });
    }
});
