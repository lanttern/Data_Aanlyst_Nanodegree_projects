function draw(data) {
      
      /*
        D3.js setup code
      */

          "use strict";
          var margin = 75,
              width = 1400 - margin,
              height = 600 - margin;

          d3.select("#mychart")
            .append("h2")
               .attr("id", "title")
               .text("Trends for Startup Industries: 1990 to 2013");

          var svg = d3.select("#mychart")
            .append("svg")
              .attr("width", width + margin)
              .attr("height", height + margin)
            .append("g")
              .attr("class","chart")
              
      /*
        Dimple.js Chart construction code
      */

          var myChart = new dimple.chart(svg, data);
          var x = myChart.addTimeAxis("x", "Founded year of startups"); 
          var y = myChart.addMeasureAxis("y", "Percentage of this startup industry (number of startups in this industry normalized with total number of founded startups)");
          var z = myChart.addMeasureAxis("z", "Number of startups in this industry") // try bubble chart
          x.dateParseFormat = "%Y";
          x.tickFormat = "%Y";
          x.timeInterval = 1;
          x.title = "Founded year of startups";
          x.fontSize = "17px"; //set font size for x label
          y.dateParseFormat = "%";
          y.tickFormat = "%";
          y.overrideMax = 0.3;
          y.title = "Percentage of Startups in Industries";
          y.fontSize = "17px"; //set font size for y label
          var Series1 = myChart.addSeries("Startup industry", dimple.plot.line); // try line chart
          var Series2 = myChart.addSeries("Startup industry", dimple.plot.scatter); //try scatter chart
          //myChart.addSeries("Startup industries", dimple.plot.area);
          //myChart.addSeries("Startup industries", dimple.plot.bar);
          // Change order of legends
          Series1.addOrderRule([" Software ", " Biotechnology ", " Mobile ", " E-Commerce ", " Other (Real Estate, Travel, Fashion, Consulting, Education, Social Media) "])
          Series1.addOrderRule([" Software ", " Biotechnology ", " Mobile ", " E-Commerce ", " Other (Real Estate, Travel, Fashion, Consulting, Education, Social Media) "])
          var legend = myChart.addLegend(width*0.9, 10, 100, 100, "right");
          legend.fontSize = "17px"; // set font size for legend
          myChart.draw();

          /* Remove grids
          */
          d3.selectAll("line")
             .style("opacity", 0);

          d3.selectAll("circle")
             .style("opacity", 0)
             .on("click", function() {
               d3.select(this)
                 .style({"stroke-width": "5px"})
                 .style("opacity", 1);
               }).on("dblclick", function() {
               d3.select(this)
                 .style({"stroke-width": "1px"})
                 .style("opacity", 0);
               })

        /* 
          Apply mouse click event: single click to show area, double click to hide area
        */

          d3.selectAll("path")
             .style("opacity", 0.2)
             .style({"stroke-width": "4px"})
             .on("click", function() {
               d3.select(this)
                 .style({"stroke-width": "8px"})
                 .style("opacity", 1);
               }).on("dblclick", function() {
               d3.select(this)
                 .style({"stroke-width": "4px"})
                 .style("opacity", 0.2);
               })
        };

  /*
    Use D3 (not dimple.js) to load the CSV file
    and pass the contents of it to the draw function
  */

  d3.csv("clean_data_R/data.csv", draw);
