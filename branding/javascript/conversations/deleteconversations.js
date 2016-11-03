// Warning!!! This javascript will delete as many conversations as possible on every page load. Use it 
// with extreme caution. It does
// not discriminate between any user role, enrollment, or user type. It loads a 
// list of conversations (on every page load) and attempts
// to delete them. Over time, it will delete all 
// conversations for every user as long as the users are in actively in Canvas.
// This should only be used when you are sure that you want to get rid of all conversations.
// Needless to say, you should probably only have this if you do not want conversations functionality in Canvas.
$(document).ready(function(){
  $.get('/api/v1/conversations?per_page=100').done(
    function(list){
      list.map(function(c){
        $.ajax('/api/v1/conversations/'+c.id, {type:'DELETE'});
      });
  });
});
