var timeFormat = d3.time.format("%I:%M:%S");

var margin = {top: 100, right: 100, bottom: 30, left: 100},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.assets); });

var data = []

var date = new Date();
date.setMinutes(date.getMinutes() - 30);

var count = 0;


function loop() {

    $.getJSON( "/status", ping);

    recent();
}

function recent() {
  count++
  if (count == 15) {
    count = 0;
    loop();
  } else {
    $.getJSON( "/status", ping2);
    setTimeout(recent, 1000);
  }
}

function ping(json) {
    if (json["value"] >= json["history"][1]) {
      document.getElementById("total").innerHTML = "$" + json["value"].toFixed(2) + "   <span style='color:green'>(" + String.fromCharCode(9650) + " +" + (json["value"] - json["history"][1]).toFixed(2) + ")</span>";
    } else {
      document.getElementById("total").innerHTML = "$" + json["value"].toFixed(2) + "   <span style='color:red'>(" + String.fromCharCode(9662) + " " + (json["value"] - json["history"][1]).toFixed(2) + ")</span>";
    }

    if (data.length == 0) {
        var history = json["history"];
        if (history.length < 120) {
            date.setSeconds(date.getSeconds() + 15 * (120 - history.length));
            for (i = history.length - 1; i >= 0; i--) {
                date.setSeconds(date.getSeconds() + 15);
                data.push({"date": +date, "assets": history[i]});
            }
        } else {
            for (i = 119; i >= 0; i--) {
                date.setSeconds(date.getSeconds() + 15);
                data.push({"date": +date, "assets": history[i]});
            }
        }
    } else {
        date.setSeconds(date.getSeconds() + 15);

        data.push({"date": +date, "assets": json["value"]});
        if (data.length == 121) {
            data.shift();
        }
    }
    var myLine = document.getElementById("bigLine");
    if (json["value"] > data[0].assets) {
        myLine.stroke = "green";
    } else if (json["value"] > data[0].assets) {
        myLine.stroke = "red";
    } else {
        myLine.stroke = "steelblue";
    }

    document.getElementById("cash").innerHTML = "$" + json["cash"].toFixed(2);

    var top = json["top"];
    for (i = 0; i < top.length; i++) {
      document.getElementById("tick" + i).innerHTML = top[i][0];
      document.getElementById("hold" + i).innerHTML = "$" + top[i][1].toFixed(2);
    }

    x.domain(d3.extent(data, function(d) { return d.date; }));

    var temp = [];
    for (i = 0; i < data.length; i++) {
      temp.push(Math.abs(data[0].assets - data[i].assets));
    }
    var range = Math.max.apply(null, temp);
    y.domain([data[0].assets - range, data[0].assets + range]);

    d3.select("svg").remove();

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Assets ($)");

    svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line)
      .attr("id", "bigLine");

}

function ping2(json) {

    var trades = json["trades"];
    for (i = 0; i < Math.min(trades.length, 10); i++) {
      document.getElementById("recent" + i).innerHTML = trades[Math.min(trades.length, 10) - i - 1];
    }

}

loop();
