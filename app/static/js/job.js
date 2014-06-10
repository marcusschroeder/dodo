$(document).ready(function () {
  $("#matrix-toggl").click(function () {
    togglMatrix();
  });

  $('#download_button').click(function (e) {
    e.preventDefault();  //stop the browser from following
    window.location.href = window.location.pathname + "?get_data=1";
  })
})

function togglMatrix() {
  var e = $('#data-table')
  if (e.is(":visible")) {
    e.hide();
    $('#matrix-toggl').text("Show data table")
  } else {
    e.show();
    $('#matrix-toggl').text("Hide data table")
  }
}