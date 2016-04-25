# On Element Rendered

This JS tweak will allow you to load some JS that is dependent on elements that are potentially loaded after the page is loaded. This would want to be used when the document ready function doesn't work.
```javascript
$(document).ready(function() {/*code*/});
```

You will want to add your code in the block below within the `on_element_rendered.js` file.
```javascript
onElementRendered('#element_id_or_.class', function(e) {
  //code goes here to wait for all elements to load
});
```
This would change this JS that loads after the DOM from
```javascript
$("select#grading_period_selector option:contains('All Grading Periods')").text('Semester 2');
```
to this code snippet with the function included.
```javascript
onElementRendered("select#grading_period_selector option:contains('All Grading Periods')", function(e) {
	e.text('Semester 2');
});
```
