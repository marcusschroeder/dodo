var matrix = [];
var ENTER = 13;
var ESC = 27;
var rows = [];
var columns = [];

function transpose() {
  $('#transpose').prop("disabled", true);

  var t = [];
  var r = matrix.length; // #rows
  var c = matrix[0].length; // #columns
  for (var i = 0; i < c; i++) {
    var t_row = [];
    for (var j = 0; j < r; j++) {
      t_row.push((matrix[j])[i]);
    }
    t.push(t_row);
  }
  matrix = t;
  var b = $('#list').is(":visible");
  updateInfo();
  if (b) {
    $('#list').show();
  }
  var tmp = rows;

  // prevent removing the first row...which is the first column before transposing
  if (columns.indexOf(0) != -1) {
    columns.splice(0, 1);
  }
  rows = columns;
  columns = tmp;
  renderSelected();

  $('#transpose').prop("disabled", false);
}

function get_methods() {
  var methods = []
  $('[type=checkbox]:checked').each(function () {
    methods.push($(this).val());
  })
  return methods;
}

function get_request_body() {
  var methods = get_methods();
  var stability = parseInt($("#stability").val());
  return JSON.stringify({
    "matrix": matrix,
    "rows": rows,
    "columns": columns,
    "methods": methods,
    "stability": stability
  });
}

function save() {
  $("#save").prop("disabled", true).text("computing...please wait");
  var rb = get_request_body();
  $.ajax({
    url: '/upload',
    type: 'POST',
    data: rb,
    contentType: "application/json; charset=UTF-8",
    dataType: "json",
    success: function (response) {
      var job_id = response["job_id"]
      $("#the-form").hide();
      $("#save").fadeOut("fast");
      $("#settings-panel")
        .fadeOut("fast")
        .html('<a class="form-control btn btn-info" href="/job/' + job_id + '">Nom, nom....! Continue</a> ')
        .fadeIn();
    },
    error: function (response) {
      $("#save").text("Something went wrong :( Please reload.")
      $("#save").addClass("btn-danger")
      $("#feedback_message").val("Uploading with the following payload went wrong:" + rb);
      fm.triggerAction(null);
    }
  });
}

function updateInfo() {
  $("#settings-panel").fadeIn("slow");
  $("#save").fadeIn("slow");
  renderTable();
  renderFeatures();
  renderNames();

  $(".header").click(function () {
    $(this).nextUntil('th.header').slideToggle(10);
  });

  $(".header").click();


  $('#stability_slider').slider({
      range: false,
      min: 0,
      max: 150,
      step: 10,
      slide: function( event, ui ) {
        $( "#stability" ).val(ui.value);
      }
    });

  $('#stability').val(50);
  $('#stability_slider').slider("value", $('#stability').val());

}

function fileInfo(e) {
  var file = e.target.files[0];
  if (file.name.split(".")[1].toUpperCase() != "CSV") {
    $("file_info").html('Invalid csv file !');
    e.target.parentNode.reset();
    return;
  } else {
    $('#file_info').html("<p>File Name: " + file.name + " | " + file.size + " Bytes.</p>");
    $('#list').html("")
  }
  handleFileSelect();
}

function expandableTable(header, arr) {
  var table = $("<table />");
  table.addClass("table");
  table.addClass("table-hover");
  table.addClass("table-bordered");

  // table head
  var tr = $("<tr class='header' />")
  var th = $("<th />")
  th.html((arr.length - 1) + " " + header + " <i>(click to expand)</i>");
  th.css("cursor", "pointer");
  tr.append(th);
  table.append(tr);

  // table content
  for (var i = 1; i < arr.length; i++) {
    var tr = $("<tr />");
    var td = $("<td />");
    td.html(arr[i]);
    $(tr).append(td);
    table.append(tr);
  }

  return table;
}

function renderFeatures() {
  var table = expandableTable("Odorants", matrix[0]);
  $('#f').empty().append(table);
}

function renderNames() {
  var names = [];
  for (var i = 0; i < matrix.length; i++ ) {
    names.push(matrix[i][0])
  }
  var table = expandableTable("Receptors", names)
  $('#n').empty().append(table);
}

function renderTable() {
  var table = $("<table></table>");
  table.addClass("table");
  table.addClass("table-hover");
  table.addClass("table-bordered");
  table.addClass("footable");

  for (var i = 0; i < matrix.length; i++) {
    var tr = $("<tr></tr>");
    var arr = matrix[i]
    for (var j = 0; j < arr.length; j++) {
      if (i == 0) {
        var td = $("<th></th>");

        if (j == 0) {
          td.attr("data-type", "alpha")
        } else {
          td.attr("data-type", "numeric")
        }
      }

      else {
        var td = $("<td></td>");
      }

      td.html(arr[j]);
      $(tr).append(td);
    }
    table.append(tr);
  }
  $('#list').empty().append(table).hide();
  prepareHandlers();

  $(function () {
    $('.footable').footable()
  })
}

function insertFileButtonToFileInfo() {
  var e = $("#the-form");
  e.detach();
  $('#file_info').append(e);
}
function handleFileSelect() {
  var file = $("#the-file")[0].files[0];
  var reader = new FileReader();
  var link_reg = /(http:\/\/|https:\/\/)/i;

  matrix = []
  reader.onload = function (file) {

    var content = file.target.result;
    var rows = file.target.result.split(/[\r\n|\n]+/);

    for (var i = 0; i < rows.length; i++) {
      if (rows[i] != '') {
        var arr = rows[i].split(/[;,]/);
        matrix.push(arr);
      }
    }
    updateInfo();
  };
  reader.readAsText(file);
  $('#file-upload-button').text("Change file");
  insertFileButtonToFileInfo();
}

var clickHandlerMap = {
  click: function (e) {
    clickHandler(e, $(this));
  }
}

function clickHandler(e, elem) {
  if (e.metaKey) {
    selectRow(elem);
  } else if (e.altKey) {
    selectColumn(elem)
  } else {
    editElement(elem)
  }
}

function selectColumn(elem) {
  var index = parseInt($(elem).index());
  if (columns.indexOf(index) != -1) {
    columns.splice(columns.indexOf(index), 1);
  } else {
    columns.push(index);
  }

  renderSelected()
}

function selectRow(elem) {

  var par = $(elem).parent();
  var index = $(par).index();

  /* do not remove the header (row 0) */
  if (index != 0 && rows.indexOf(index) == -1) {
    rows.push(index);
  } else {
    rows.splice(rows.indexOf(index), 1);
  }
  renderSelected()
}

function renderSelected() {

  $('td').removeClass('selected');
  $('th').removeClass('selected');

  rows.forEach(function (element, index, array) {
    $('tr:nth-child(' + (element + 1) + ')').find("td").addClass("selected");
  })

  columns.forEach(function (element, index, array) {
    $('th:nth-child(' + (element + 1) + ')').addClass("selected")
    $('td:nth-child(' + (element + 1) + ')').addClass("selected")
  })
}

function editElement(elem) {
  $(elem).trigger("modifyEvent")

  /*block further clicks, so selected state cannot be changed*/
  $(elem).off("click")

  var old = $(elem).html();
  var inp = createInputElem(old)
  var elemLen = inp.val().length;

  inp.selectionStart = elemLen;
  inp.selectionEnd = elemLen;
  inp.focus()

  inp.keyup(function (e) {
    keyHandler(e, old)
  });

  $(elem).html(inp);
  $(elem).addClass("input-parent")

}

function keyHandler(e, old) {
  var elem = e.target
  var par = $(elem).parent()

  if (e.keyCode == ENTER || e.keyCode == ESC) {

    var val = $(elem).val()

    if (e.keyCode == ENTER && val != '') {

      var col = parseInt($(par).index());
      var row = parseInt($(par).parent().index());

      matrix[row][col] = val;

      $(par).html(val);
    } else {
      $(par).html(old);
    }
    appendClickHandlerMap(par)
    $(par).removeClass("input-parent")
  }
}

function appendClickHandlerMap(elem) {
  $(elem).off("keydown")
  $(elem).on(clickHandlerMap)
}

function reset(elem, old) {
  var par = $(elem).parent()
  $(par).removeClass("input-parent")
  appendClickHandlerMap(elem)
}

function createInputElem(old) {
  return $('<input id="newvalue" class="matrix" type="text" name="newvalue" value="' + old + '"/>')
}

function prepareHandlers() {
  $('td').on(clickHandlerMap);
  $('th').on(clickHandlerMap);
}

$(function () {
  $('#the-file').change(fileInfo);
  $('#settings-panel').hide()
  $('#save').hide()
  $("#show_table").click(function () {
    var e = $('#list');
    if (e.is(":visible")) {
      e.hide();
      $(this).addClass("glyphicon-plus")
      $(this).removeClass("glyphicon-minus")
    } else {
      e.show();
      $(this).removeClass("glyphicon-plus")
      $(this).addClass("glyphicon-minus")
    }
  });
  $('#file-upload-button').click(function(){
    $('#the-file').click();
  })

  $('#stability').change(function(e) {
    $('#stability_slider').slider("value", $(this).val());
  });
});