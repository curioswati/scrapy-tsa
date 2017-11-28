var n = 3, // The number of sentiments.
    m = 7; // The number of days for which data is shown per series.

// The xz array has m elements, representing the x-values shared by all series.
// The yz array has n elements, representing the y-values of each of the n series.
// Each yz[i] is an array of m non-negative numbers representing a y-value for xz[i].
// The y01z array has the same structure as yz, but with stacked [y₀, y₁] instead of y.
var data = $("#result").data().result;
var xz = d3.range(m),
    yz = d3.range(n).map(
            function(i) {
                var result = [];
                for (key in data) {
                    result.push(data[key][i+1]);
                }
                return result;
            }),
    y01z = d3.stack().keys(d3.range(n))(d3.transpose(yz)),
    yMax = d3.max(yz, function(y) { return d3.max(y); }),
    y1Max = d3.max(y01z, function(y) { return d3.max(y, function(d) { return d[1]; }); });

var svg = d3.select("svg"),
    margin = {top: 40, right: 10, bottom: 20, left: 20},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scaleBand()
    .domain(xz)
    .rangeRound([0, width])
    .padding(0.00);

var y = d3.scaleLinear()
    .domain([0, y1Max])
    .range([height, 0]);

var color = [d3.rgb(255, 107, 107), d3.rgb(78, 205, 196), d3.rgb(199, 244, 100)]
var series = g.selectAll(".series")
  .data(y01z)
  .enter().append("g")
    .attr("fill", function(d, i) { return color[i]; });

var rect = series.selectAll("rect")
  .data(function(d) { return d; })
  .enter().append("rect")
    .attr("x", function(d, i) { return x(i); })
    .attr("y", height)
    .attr("width", x.bandwidth())
    .attr("height", 0);

rect.transition()
    .delay(function(d, i) { return i * 10; })
    .attr("y", function(d) { return y(d[1]); })
    .attr("height", function(d) { return y(d[0]) - y(d[1]); });

var x_axis_data = function() {
    dates = [];
    for (key in data) {
        dates.push(data[key][0]);
    }
    return dates;
}();
var xAxis = d3.scaleBand()
    .domain(x_axis_data)
    .rangeRound([0, width])
    .padding(0.00);

var y_axis_data = function(yz) {
    y_values = [];
    for (i=0; i<yz.length; i++) {
        for (j=0; j<yz[i].length; j++) {
        y_values.push(yz[i][j]);
        }
    }
    return y_values;
}(yz);
var yAxis = d3.scaleLinear()
    .domain(y_axis_data)
    .rangeRound([height, 0]);

g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xAxis)
        .tickSize(0)
        .tickPadding(6));

g.append("g")
    .attr("class", "axis axis--x")
    .call(d3.axisLeft(yAxis)
        .tickSize(0)
        .tickPadding(6));

transitionStacked();

function transitionStacked() {
  y.domain([0, y1Max]);

  rect.transition()
      .duration(500)
      .delay(function(d, i) { return i * 10; })
      .attr("y", function(d) { return y(d[1]); })
      .attr("height", function(d) { return y(d[0]) - y(d[1]); })
    .transition()
      .attr("x", function(d, i) { return x(i); })
      .attr("width", x.bandwidth());
}
