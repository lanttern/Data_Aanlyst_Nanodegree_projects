
  /*
    draw function for the first chart
  */

function draw_1st(data) {
      
      /*
        D3.js setup code
      */

          "use strict";
          var margin = 75,
              width = 650 - margin,
              height = 620 - margin;

          var svg = d3.select("#mychart1")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
            .append("g")
              .attr("class","chart");
              
      /*
        Dimple.js Chart construction code
      */

          var myChart1 = new dimple.chart(svg, data);
          var x = myChart1.addTimeAxis("x", "Founded year of startups"); 
          var y = myChart1.addMeasureAxis("y", "Percentage of startups by industry");
          var z = myChart1.addMeasureAxis("z", "Number of startups in this industry")
          x.dateParseFormat = "%Y";
          x.tickFormat = "%Y";
          x.timeInterval = 1;
          x.title = "Founded year of startups";
          x.fontSize = "13.5px"; //set font size for x label
          y.dateParseFormat = "%";
          y.tickFormat = "%";  
          y.title = "Percentage of Startups by Industry";
          y.fontSize = "13.5px"; //set font size for y label
          myChart1.addSeries("Startup industry", dimple.plot.line); // line chart
          myChart1.addSeries("Startup industry", dimple.plot.scatter); // scatter chart
          myChart1.draw();

          /* set opacity for grids and circles
          */

          d3.selectAll("line")
             .style("opacity", 0);
          d3.selectAll("circle")
             .style("opacity", 0);

        /* 
          Apply mouse click event: single click to show line, double click to hide line
        */

          d3.selectAll("path")
             .style("opacity", 0.3)
             .style({"stroke-width": "4px"})
             .on("click", function() {
               d3.select(this)
                 .style({"stroke-width": "8px"})
                 .style("opacity", 2);
               }).on("dblclick", function() {
               d3.select(this)
                 .style({"stroke-width": "4px"})
                 .style("opacity", 0.3);
               });

        };

  /*
    draw function for the second chart
  */

function draw_2nd(data) {
      
      /*
        D3.js setup code
      */

          "use strict";
          var margin = 75,
              width = 650 - margin,
              height = 620 - margin;

          var svg = d3.select("#mychart2")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
            .append("g")
              .attr("class","chart");
              
      /*
        Dimple.js Chart construction code
      */

          var myChart2 = new dimple.chart(svg, data);
          var x = myChart2.addCategoryAxis("x", "Founded year of startups"); 
          var y = myChart2.addMeasureAxis("y", "Percentage of startups by industry");
          var z = myChart2.addMeasureAxis("z", "Number of startups in this industry")
          x.dateParseFormat = "%Y";
          x.title = "Founded time period of startups";
          x.fontSize = "13.5px"; //set font size for x label
          y.dateParseFormat = "%";
          y.tickFormat = "%";
          y.overrideMax = 0.24;
          y.title = "Percentage of Startups by Industry";
          y.fontSize = "13.5px"; //set font size for y label
          var Series1 = myChart2.addSeries("Startup industry", dimple.plot.line); // line chart
          var Series2 = myChart2.addSeries("Startup industry", dimple.plot.scatter); // scatter chart
          var legend = myChart2.addLegend(width*0.6, 10, 250, 250, "right", [Series1, Series2]);
          legend.fontSize = "17px"; // set font size for legend
          myChart2.draw();

          /* 
            set opacity for grids and circles
          */

          d3.selectAll("line")
             .style("opacity", 0);
          d3.selectAll("circle")
             .style("opacity", 0);

        /* 
          Apply mouse click event: single click to show line, double click to hide line
        */

          d3.selectAll("path")
             .style({"stroke-width": "2px"})
             .on("click", function() {
               d3.select(this)
                 .style({"stroke-width": "8px"})
               }).on("dblclick", function() {
               d3.select(this)
                 .style({"stroke-width": "2px"})
               });
        };

  /*
    Use D3 (not dimple.js) to load the CSV file
    and pass the contents of it to the draw function
  */

d3.csv("clean_data_R/data.csv", draw_1st);
d3.csv("clean_data_R/data1.csv", draw_2nd);
 
