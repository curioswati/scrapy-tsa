var data2 = {"name": "Tweet Timeline", "series": $("#result").data().result};

var data = {"name": "xyz", "series":
    [{"key": "Positive", "values": [
        {"label": "2017-12-02", "value": "8"},
        {"label": "2017-12-03", "value": "7"},
        {"label": "2017-12-04", "value": "8"},
        {"label": "2017-12-05", "value": "7"},
        {"label": "2017-12-06", "value": "5"},
        {"label": "2017-12-07", "value": "6"},
        {"label": "2017-12-08", "value": "6"}]},
    {"key": "Neutral", "values": [
        {"label": "2017-12-02", "value": "9"},
        {"label": "2017-12-03", "value": "9"},
        {"label": "2017-12-04", "value": "5"},
        {"label": "2017-12-05", "value": "8"},
        {"label": "2017-12-06", "value": "7"},
        {"label": "2017-12-07", "value": "8"},
        {"label": "2017-12-08", "value": "9"}]
    },
    {"key": "Negative", "values": [
        {"label": "2017-12-02", "value": "4"},
        {"label": "2017-12-03", "value": "3"},
        {"label": "2017-12-04", "value": "6"},
        {"label": "2017-12-05", "value": "4"},
        {"label": "2017-12-06", "value": "2"},
        {"label": "2017-12-07", "value": "2"},
        {"label": "2017-12-08", "value": "4"}]
    }
    ]
}

function drawChart(data) {
    console.log(data);
    nv.addGraph(function() {
        var chartdata;

        var maxValue = d3.max(data.series, function(d) {
            return d3.max(d.values, function(d) {
                return parseFloat(d.value);
            })
        });
        var minValue = d3.min(data.series, function(d) {
            return d3.min(d.values, function(d) {
                return parseFloat(d.value);
            })
        });

        var chart = nv.models.multiBarChart()
            .color(["#295949", "#FFA644", "#E53d36"])
            // .x(function(d) {
            //     return d.label
            // })
            .y(function(d) {
                return parseFloat(d.value);
            })
            .reduceXTicks(false) //If 'false', every single x-axis tick label will be rendered.
            .rotateLabels(0) //Angle to rotate x-axis labels.
            .showControls(false) //Allow user to switch between 'Grouped' and 'Stacked' mode.
            .stacked(true)
            .groupSpacing(0.2); //Distance between each group of bars.

        chart.yAxis.ticks(10)
            // .tickFormat(function(d) {
            //     return formatAbbr(d)
            // })
            .axisLabel("Number of Tweets")
            .axisLabelDistance(10)
            .ticks(10);

        chart.x(function(d) {
            var format = d3.time.format("%Y-%m-%d");
            return format.parse(d.label);
        })

        chart.y(function(d) {
            return parseFloat(d.value)
        })

        // chart.tooltip.valueFormatter(function(d) {
        //     return d3.format(",.f")(d);
        // })

        if (maxValue < 0) {
            maxValue = 0;
        }
        if (minValue > 0) {
            minValue = 0;
        }
        chart.yAxis.scale().domain([minValue, maxValue]);

        chart.margin({ "left": 120, "right": 20, "top": 0, "bottom": 70 })
        .width(700)
        .noData("The record has no values in the budget document.")
 
        chart.xAxis.axisLabel("Date")
            .tickFormat(function (d) {
                var format = d3.time.format("%Y");
                return d.getDate() + "/" + d.getMonth() + "/" + d.getFullYear();
            })
            .axisLabelDistance(20);

        chartdata = d3.select('header svg')
            .datum(data.series)
            .call(chart);

        chartdata.transition().duration(500).call(chart);
        nv.utils.windowResize(chart.update);

        return chart;
    });
}
drawChart(data);
