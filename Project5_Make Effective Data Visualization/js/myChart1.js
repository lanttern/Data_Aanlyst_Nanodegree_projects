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
          var y = myChart.addMeasureAxis("y", "Percentage of startups by industry");
          var z = myChart.addMeasureAxis("z", "Number of startups in this industry")
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
          var S1 = myChart.addSeries("Startup industry", dimple.plot.line); // line chart
          var S2 = myChart.addSeries("Startup industry", dimple.plot.scatter); // scatter chart
          S1.addOrderRule([" Software ", " Biotechnology ", " Mobile ", " E-Commerce ", " Other (Real Estate, Travel, Fashion, Consulting, Education, Social Media) "])
          var legend = myChart.addLegend(width*0.9, 10, 150, 100, "right", [S1, S2]);
          legend.fontSize = "17px"; // set font size for legend
          myChart.draw();

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
                 .style({"stroke-width": "1px"})
                 .style("opacity", 0.3);
               });

        };

  /*
    Use D3 (not dimple.js) to load the CSV file
    and pass the contents of it to the draw function
  */

d3.csv("clean_data_R/data_other.csv", draw);
