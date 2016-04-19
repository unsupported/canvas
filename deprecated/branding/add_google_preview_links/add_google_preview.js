//DEPRECATED AS OF 04/19/2016
/*
 * If you disable Scribd and are unfortunate enough to have missing document preview links
 * after the change, this script may come in handy.  It scans the page for Canvas file
 * links and adds the preview button to those files that are previewable.
 *
 * Use at your own risk.
 *
 */
$(document).ready(function(){
  // First, fetch all instructure file links, they are the first <a> in .link holder div's
  var links = $('#content .link_holder a:first-child');
  // With each link, check whether it is previewable.  If it is, add the preview link next
  // to it.
  $(links).each(function(idx,_item){
    var item = $(_item);
    var file_id = item.attr('href').split('/')[4];
    // Need to make an API call to get the content-type of the file.  This API call
    // doesn't need an access token because it will work by nature of the user being
    // logged in.
    $.get('/api/v1/files/'+file_id,function(_d){
      if($.isPreviewable(_d['content-type'],'google')===1){
        // It's previewable!  Create the preview links
        var a = $(document.createElement('a'))
          .addClass('scribd_file_preview_link')
          .attr('href',item.attr('href'))
          .attr('title',alt="Preview the document");
        var img = $(document.createElement('img'))
          .attr('src', "/images/preview.png")
          .attr('alt',"Preview the document");
        a.append(img);
        item.after(a);
      }
    });
  });
});
