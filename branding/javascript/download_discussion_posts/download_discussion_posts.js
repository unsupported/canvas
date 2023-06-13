/* download_discussion_posts.js
 * by: Danny Wahl danny@instructure.com
 * Working as of 01/16/2019
 * Adds a "download" button to a discussion
 * Clicking "download" will generate a CSV
 * of all the discussion posts
 */

  function onElementRendered(selector, cb, _attempts) {
    var el = $(selector);
    _attempts = ++_attempts || 1;
    if (el.length) return cb(el);
    if (_attempts == 60) return;
    setTimeout(function() {
      onElementRendered(selector, cb, _attempts);
    }, 250);
  };

  console.log("download_discussion_posts.js");
  console.log("  Checking if user is viewing a discussion...");

  var path = window.location.pathname.split( '/' );

  if((path[3] == "discussion_topics") && (path.length > 4)) {

    console.log("  User is viewing a discussion.");
    console.log("  Gathering Discussion Entries");

    var course = $("#breadcrumbs li:nth-child(2)").text();
    var courseid = ENV.COURSE_ID
    var title = ENV.DISCUSSION.TOPIC.TITLE
    var id = ENV.DISCUSSION.TOPIC.ID

    function entry(id, author, time, likes, text) {
      this.id = id;
      this.author = author;
      this.time = time;
      this.likes = likes;
      this.text = text;
    }

    var entries = [];
    //entries.push(new entry("ID", "Author", "Time", "Likes", "Text"));
    
    onElementRendered('li.entry', function(e) {
      
      $('.entry').each(function(i){

      var id = Number($(this).prop("id").match(/\d+/));
      console.log("id:", id)

      var author = $.trim($(this).find(".author").first().text());
      console.log("author:", author);

      var time = $(this).find("time").first().attr("datetime");
      console.log("time:", time);

      var likes = Number($(this).find(".discussion-rating").text().match(/\d+/));
      console.log("likes:", likes);

      var text = $(this).find(".message").first();
      //TODO: Replace paragraphs and breaks with carriage returns
      //text.find('br').replaceWith('\n');
      //text.find('p').append('\n');
      text = text.text();
      console.log("text:", text);

      console.log("")

      entries.push(new entry(id, author, time, likes, text));
    });

    console.log("Entries:", entries)

    console.log("  Building CSV file")
    const replacer = (key, value) => value === null ? '' : value
    const header = Object.keys(entries[0])
    let csv = entries.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
    csv.unshift(header.join(','))
    csv = csv.join('\n')
    console.log(csv)

    

    
    function download(strData, strFileName, strMimeType) {
      var D = document,
        a = D.createElement("a");
        strMimeType= strMimeType || "application/octet-stream";
      if ('download' in a) {
        a.href = "data:" + strMimeType + "," + encodeURIComponent(strData);
        a.setAttribute("download", strFileName);
        a.innerHTML = "downloading...";
        D.body.appendChild(a);
        setTimeout(function() {
          a.click();
          D.body.removeChild(a);
        }, 66);
        return true;
      } else {
        var f = D.createElement("iframe");
        D.body.appendChild(f);
        f.src = "data:" +  strMimeType + "," + encodeURIComponent(strData);
        setTimeout(function() {
          D.body.removeChild(f);
        }, 333);
        return true;
      }
    }
    var anchor = '&nbsp;<a href="#" class="btn download-btn" role="button" id="export_entries"><i class="icon-download" aria-hidden="true"></i>&nbsp;Export</a>'
    $("#discussion-managebar .edit-btn").after(anchor);

    /* TODO: Add to menu
    var anchor = '<li class="ui-menu-item" role="presentation"><a href="#" class="export_entries_as_csv ui-corner-all" id="export_entries" tabindex="-1" role="menuitem"><i class="icon-download" aria-hidden="hidden"></i> Export as CSV</a></li>';
    $("#discussion-managebar .admin-links > a").click(function(){
      $("#discussion-managebar .ui-menu").append(anchor);
    }); */

    $("#export_entries").click(function(e){
      console.log("  User clicked 'Export'");
      e.preventDefault();
      fileName = course + " (" + courseid + ") - " + title + " (" + id + ").csv";
      encoding = "text/plain";
      download(csv, fileName, encoding);
      console.log("  File sucessfully exported.");
    });
      });

  } else {
    console.log("  User is not currently viewing a discussion, will not add 'export' button.");
  }
