# Canvas Report Discussion Post
This script adds "report" buttons to each entry in a discussion.  When a user clicks 'report' it will do 2 things:
* send an inbox message to the Discussion author notifying them an entry has been reported (with a link to the entry)
* hide the entry content from the reporter

If the inbox message fails to be delivered, the content is still hidden from the reporter, and they are notified that
the report failed.

## Usage
* Upload `report_discussion_post.js` to the theme editor.

## Note
This is JavaScript.  If a user refreshes or navigates away and back to a discussion with a reported entry,
the content of said entry will be displayed.
