# Make Effective Data Visualization: Trends for Startup Industries: 1990 to 2013
#### by Zhihui Xie
## Summary
This data visualization is going to explore trends of hot startup industry from 1990 to 2013. The dataset was downloaded from CruchBase (https://info.crunchbase.com/about/crunchbase-data-exports/).
## Design
### Data Cleaning and Exploratory
The hypothesis of the design is the quantity or the percentage of startups may be different across different industries over time. To test the hypothesis, I first removed invalid data points in “market” and “founded_year” column using Rstudio. Then, I did the first exploration with all industries across all years in the data set:
![alt tag](images/r1.png) 
This visualization contains too much information. The line chart was cluttered and it’s hard to get the effective comparisons. Therefore, the data were truncated and focused on hot industries (with number of startups greater than 1400) from 1990 to 2013. I did the second exploration as shown below:
![alt tag](images/r2.png) 
This chart shows trends of increase of new founded startups in all industries from 1990 to 2007. The increases reach a peak in 2012 for software and E-commerce, then drop down. For biotechnology, the quantity of new founded startups decreased in 2008, increased in 2009-2010, and then dropped down quickly from then on. For mobile, the quantity of new founded startups decreased from 2011.

The chart above somehow reflects the trends of quantity of new founded startups in each industry over time. However, the total number of new founded startups also changed overtime. So, it’s important to compare the trends of occupied percentage of startups in industry. To do that, I did the third exploration: 
![alt tag](images/r3.png) 
This new chart displays the trends of relative percentage of startups in industries, which addresses the question - what are the trends for startups over time. 
Finally, I loaded the exploration results to “clean_data_R” fold and exported the truncated data.
### Data Visualization 
#### Reasons for applying line chart and scatter chart
Using the cleaned data, I decided to creat a new chart with D3.js and dimple.js. I tried several different charts: line chart, scatter chart and bar charts. A bar chart is one of the most commonly used forms of presenting quantitative data and it is best used when comparing data from different categories. While line chart is usually applied for time-seriers data. Here, I want to explore how percentage of startups by industry changes over time. Thus, line chart is a better option for this purpose. Also, I noticed that the line chart (represents change of percentage of startup industry) combined with the scatter chart (represents number of startups) clearly represented the changes of percentage of startups in industries over time.
#### Improve the charts
But the circles in scatter chart are too dense in some area of the chart. Thus, I set "opacity" as zero for circles. To improve the chart, I also did the following adjustments: 1) used different colors to distinguish industries from each other; 2) format x and y-axes and add title for axes; 3) add title for the chart on top center; 4) add legend to indicate each industry; 5) add a mouse click event to highlight individual market. The initial chart was shown as below:

![alt tag](images/d3.png) 
## Feedback
#### Interview #1
###### I quickly noticed the biotechnology was shrunk dramatically over time.  

###### I feel the mouse click event is awesome, but the line is too thin and hard to click it in a right way to highlight. 

###### I think the main takeaway is that percentage of these startups is decreasing.

#### Interview #2
###### I relized that this is an interactive graph and really like to move mouse over differet time period to see the detailed information. Include number of startups in the interactive graph is very informative since the trends of number of startups and percentage of startups in industries are different.

###### The main idea I gain was these hot startups decreased from 1990 to 2013. While, the open question is which startups are increased as compared to other startups. 

#### Interview #3
###### The highlight on biotechnology gave me a clear idea how this industry of startups occupied porportion changed across time. I think it will be better if you can select and highlight two or more industries for comparisons in the final plot.

###### In addition, though it's a challenge question, it's interesting and important to explore other industries that have increasing trends.

## Final Design - 1
In responding to comments from the interviews, I improved the chart with the following modifications:

1) Set style for all path with increase of "stroke-width";

2) To explore industries with increasing trends are challenge because there are many new emerged small industries with increasing trends, adding these industries will make the visualization too complex. To partially address this issue, I focused on industries with number of startups greater than 300. Then, I examined the changes of percentage of these industries overtime and found the following industries with increased trends: Real Estate, Travel, Fashion, Consulting, Education, Social Media. To simplify the graph, these industries are classified as "Other".

3) Two typical trends were highlighted in the final plot: biotechnology and other. 
The final chart of the data visualization is shown below:
![alt tag](images/d3_final.png) 
The final code includes "index_final.html", "css/style_final.css", "js/myChart_final.js". 

## Feedback from Udacity Reviewer
###### 1) The animations you put in work well. I like the tooltip that shows up when hovering. However, it'll help if there's some note on the chart that the lines are clickable. I wouldn't have known they were clickable if I hadn't gone through the javascript code.

###### 2) Also the visualization is quite wide. It doesn't fit on my laptop screen unless I zoom out.

###### 3) It'll be great if you can add a brief explanation about why the time-series was a better visualization than the bar chart.

###### 4) This visualization looks great, and it's a great start. I'd put this more as an exploratory visualization than an explanatory. With an explanatory visualization, you really want to tell a story to the reader and get a point across. From your README file, it seems like the story you want to tell is that certain industries used to dominant the startup scene while other industries are now becoming more important. It's okay to make multiple charts if that helps tell the story.

###### 5) I think it'd be very interesting to separate out those "other" industries into their own separate lines. When I see the visualization, I want to know what are the new trending industries, and it seem like since 2003, it's all those industries in the "other" category.

###### 6) I thought a slope graph might interest you. It's a really effective yet simple way to show how a variable has changed over time. You definitely don't have to do something like this. http://charliepark.org/slopegraphs/ http://skedasis.com/d3/slopegraph/

###### I also wanted to point out that the y-axis confused me a little bit. At first I thought your graph was showing the percentage of companies in an industry that is a startup (for example, in 1990, 22% of all software companies were startups). Maybe Percentage of Startups by Industry would be clearer...

###### 7) I think you can help tell the story by putting more information in your data. For example, that the data comes from Crunchbase, that the data represents the percentage of startups by industry, etc.

###### 8) Have fun with it, and try to make the visualization really tell a story that's impactful and easy to understand. Another way to look at the data is splitting it up into time periods. For example, the 90s was when the internet started being available to the masses. Google started in 1998, and there was a big crash in 2001. Facebook came along in 2004, and smart phones went to mass market in 2007 with the iphone.

## Final Design - 2
In responding to comments from the reviewer, I improved the chart with the following modifications:

1)&7) I modified myChart.js code to add data source information and a note to show it's clickable.

2) The chart fits well in my screen. I narrowed the wide a little bit in case is too big in other screen.

3) I added a section "Reasons for applying line chart and scatter chart" to state why I chose line chart and scatter chart.

4)&5) It's a good suggestion to separate industries in "Other" category. I took the suggestion and show them in new final design.

6)&8) Both are great suggestions. While, here I want to tell a story about trends of certain industries druing a time period from 1990 to 2013, and see how they change each year. I think the line chart is good for this purpose, but it's worthy and interesting to try the slope graph and split the data into certain time periods. I will play around with that.  

7) I changed the y-axis title to "Percentage of Startups by Industry" as suggested.

The final chart of the data visualization is shown below:

![alt tag](images/d3_final1.png) 

In this final chart, one decreased trends (biotechnology) and one increased trends (Social Media) from 2005 to 2013 were highlighted in the final plot: biotechnology and other. 

The final code includes "index_final.html", "css/style_final.css", "js/myChart_final.js". 

## Discussion
The dataset was downloaded from CruchBase. There might be some limitations for this dataset. For example, the data are incomplete as many startups are not collected or reported in the system, or the classifications of industries are not completely correct. Even though, the trends shown here are still meaningful considering the data in the system are not totally biased.

## Resources
[CrunchBase](https://www.crunchbase.com/)

[Exploratory Data Analysis Using R (Udacity)](https://www.udacity.com/course/ud651)

[Data Visualization and D3.js (Udacity)](https://www.udacity.com/course/ud507)

[Dimple.js Documentation](dimplejs.org/)

[Stackoverflow](stackoverflow.com/)
