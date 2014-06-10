var colors = ["steelblue", "green", "orange", "brown", "black"];
var color_hash = []

function recursive_plotting(index) {

  if (index < methods.length) {
    d3.csv(window.location.pathname + "/method/" + methods[index][0] + "/results", function (error, data) {
      dataset.push(data);
      color_hash.push([methods[index][1], colors[index]]);

      if (index + 1 == methods.length) {
        dataset.forEach(function (d) {
          update_limits(d);
        })

        dataset.forEach(function (d, i, a) {
          plot_line(d, color_hash[i][1]);
        })

        var f = number_features_from_url();
        if (f) {
          render_odorant_table(f)
          changeSpan(f)
        } else {
          render_odorant_table(3)
          changeSpan(3)
        }
        update_legend();
      } else {
        recursive_plotting(index + 1)
      }
    });
  }
}

/**
 * Gets the
 * @returns {*}
 */
function number_features_from_url() {
  var f = window.location.hash;
  f = f.slice(1); //remove hashtag
  f = parseInt(f);
  return f;
}

function update_limits(data) {
  data.forEach(function (d) {
    d.score = d.score;
    d.features = d.features;
    var r = parseFloat(d.score);
    if (r > y_max) {
      y_max = r;
    }
    r = parseInt(d.features);
    if (r > x_max) {
      x_max = r;
    }

  });
  x.domain([0, x_max]);
  y.domain([0, y_max]);
  svg.select(".x.axis").call(xAxis);
  svg.select(".y.axis").call(yAxis);
}

var div = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

var valueline = d3.svg.line()
  .x(function (d) {
    return x(d.features);
  })
  .y(function (d) {
    return y(d.score);
  });

function changeSpan(i) {
  $('#odors').text(i);
}
function plot_line(data, color) {
  svg.append("path")		// Add the valueline path.
    .attr("class", "line")
    .style("stroke", color)
    .attr("d", valueline(data));

  svg.selectAll("dot")
    .data(data)
    .enter().append("circle")
    .attr("r", 3)
    .attr("cx", function (d) {
      return x(d.features);
    })
    .attr("cy", function (d) {
      return y(d.score);
    })
    .style("stroke", color)
    .style("stroke-width", "1.5px")
    .style("fill", "transparent")
    .style("cursor", "pointer")
    .on("mouseover", function (d, i) {


      // on hover of a single data point
      // show a div with some information
      div.transition()
        .duration(100)
        .style("opacity", .9);
      div.html("Features: " + d.features + "<br/>" + "Distance: " + Math.round(d.score * 100)/100)
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY - 28) + "px")
        .style("background", color);
    })
    .on("mouseout", function (d) {
      div.transition()
        .duration(100)
        .style("opacity", 0);
    })
    .on("click", function (d, i) {
      // render the table
      window.location.hash = "#" + i;
      render_odorant_table(i);
      changeSpan(i);
    });
}

function render_odorant_table(index) {

  var table = $("<table/>");
  table.attr("id", "odor-table");
  table.addClass("table");
  table.addClass("table-bordered");

  var indices = []
  dataset.forEach(function (d) {
    var x = eval(d[index].ids)
    indices.push(x);
  })

  // adding headers with download button
  var tr = $("<tr/>");
  tr.append($("<td/>"))
  methods.forEach(function (d, i) {
    var p = window.location.pathname + '/method/' + d[0] + '/features/' + index;
    var button = $("<a/>");
    button.addClass("glyphicon glyphicon-download");
    button.css("cursor", "pointer");
    button.attr("href", p);

    var td = $("<td/>");
    td.append(button);

    var span = $("<span/>")
    span.text(d[1] + " (" + optimal[d[0]] + ")")
    span.css("color", colors[i])
    td.append(" ");
    td.append(span)
    tr.append(td);
  })
  table.append(tr);

  // adding results
  // row by row (e.g. horizontally)
  for (var i = 0; i < index; i++) {
    var tr = $("<tr></tr>");
    tr.append("<td>"+ (i+1) +"</td>") //index
    indices.forEach(function (d) {
      var td = $("<td></td>");
      td.html(odorants[d[i]]);

      td.hover(function(){
        var a = $(this).text();
        $("td").filter(function() { return $(this).text() == a; }).toggleClass("same-odor");
      });
      tr.append(td);
    })
    table.append(tr);
  }
  $("#odorants").empty().append(table);
}

var margin = {top: 30, right: 20, bottom: 30, left: 50},
  width = 720 - margin.left - margin.right,
  height = 300 - margin.top - margin.bottom;

var x = d3.scale.linear().range([0, width]);
var y = d3.scale.linear().range([height, 0]);
var x_max = 0;
var y_max = 0;
var dataset = []

var xAxis = d3.svg.axis().scale(x)
  .orient("bottom");

var yAxis = d3.svg.axis().scale(y)
  .orient("left");

//Specify the DOM Element for the plot
//and its extent.
var svg = d3.select("#plot")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Add a title
svg.append("text")
  .attr("x", (width / 2))
  .attr("y", 0 - (margin.top / 2))
  .attr("text-anchor", "middle")
  .style("font-size", "16px")
  .text("Optimal sets");


// define the range of x Axis and y Axis
x.domain([0, 100])
y.domain([0, 100])

// Add X Axis
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .attr("class", "x axis")
  .call(xAxis)
  .append("text")
  .attr("x", (width / 2))
  .attr("y", margin.bottom)
  .style("text-anchor", "middle")
  .text("Odorant Set Size");

// Y Axis
svg.append("g")
  .attr("class", "y axis")
  .call(yAxis)
  .append("text")
  .attr("y", 0 - margin.left + 10)
  .attr("x", 0 - (height / 2))
  .style("text-anchor", "middle")
  .text("Euclidean Distance")
  .attr("transform", "rotate(-90)");


// add a legend bottom right
var legend = svg.append("g")
  .attr("class", "legend")
  .attr("x", width - 65)
  .attr("y", 25)
  .attr("height", 100)
  .attr("width", 100);


function update_legend() {
  legend.selectAll('g').data(dataset)
    .enter()
    .append('g')
    .each(function (d, i) {
      var g = d3.select(this);
      g.append("rect")
        .attr("x", width - 165)
        .attr("y", height - i * 25 - 40)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", color_hash[i][1]);

      g.append("text")
        .attr("x", width - 150)
        .attr("y", height - i * 25 - 30)
        .attr("height", 30)
        .attr("width", 100)
        .style("fill", color_hash[i][1])
        .text(color_hash[i][0]);
    });
}
recursive_plotting(0);