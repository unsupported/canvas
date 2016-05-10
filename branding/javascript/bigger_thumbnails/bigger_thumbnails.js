//WORKS AS OF 04/29/2016
/*
 * This script will resize the thumbnails used for Youtube and Kaltura
 *
 * It appears to work well but use at your own risk.
 */

$(document).ready(function(){
  var img_list = $('span.media_comment_thumbnail');
  for(var x=0;x<img_list.length;x++){
    var url = $(img_list[x]).css('background-image');
    if(url.indexOf('instructuremedia')>=0){
      /*
        //width/140/height/100/bgcolor/000000/type/2/vid_sec/5);
      */
      $(img_list[x]).css('background-image',$(img_list[x]).css('background-image').replace('width/140','width/295').replace('height/100','height/211'));
      //console.log($(img_list[x]).css('background-image'
    }else{
      // Works for youtube
      $(img_list[x]).css('background-image',$(img_list[x]).css('background-image').replace('2.jpg','0.jpg'));
    }
    $(img_list[x]).width('480px').height('360px')
  }


  /*
   * This script will resize the thumbnails used for Youtube and Kaltura
   *
   * It appears to work well but use at your own risk.
   */

  var img_list = $('span.media_comment_thumbnail');
  for(var x=0;x<img_list.length;x++){
    var url = $(img_list[x]).css('background-image');
    if(url.indexOf('instructuremedia')>=0){
      /*
        //width/140/height/100/bgcolor/000000/type/2/vid_sec/5);
      */
      $(img_list[x]).css('background-image',$(img_list[x]).css('background-image').replace('width/140','width/195').replace('height/100','height/211'));
      //console.log($(img_list[x]).css('background-image'
    }else{
      // Works for youtube
      $(img_list[x]).css('background-image',$(img_list[x]).css('background-image').replace('2.jpg','0.jpg'));
    }
    $(img_list[x]).width('480px').height('360px')
  }

});
