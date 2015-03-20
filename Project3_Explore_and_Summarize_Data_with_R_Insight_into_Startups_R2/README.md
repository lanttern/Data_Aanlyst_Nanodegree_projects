#Insight into Startups 

### by Zhihui Xie

========================================================

## Global setting and library for this analysis

```{r global_options}
# global setting for this analysis
library(knitr)
opts_chunk$set(fig.width=12, fig.height=8,
               warning=FALSE, message=FALSE)
```

```{r packages}
# Load all of the packages that you end up using
# in your analysis in this code chunk.
suppressMessages(library(ggplot2))
suppressMessages(library(maps))
suppressMessages(library(dplyr))
suppressMessages(library(grid))
suppressMessages(library (gridExtra))
suppressMessages(library(GGally))
suppressMessages(library(scales))
data(state)
```

# 1. Overview
#### The startups, generally newly created, are in a phase of development and research for markets.It's important for both investors and entrepreneurs to understand characteristics of startups such as what are hot markets, where are hot regions and when are hot seasons for startups. To explore that, data of startups from 1990 to 2014 in US were used and analyzed in this project (collected by CruchBase (https://info.crunchbase.com/about/crunchbase-data-exports/)).

# 2. Analysis

## 2.1 Load the Data

```{r Load_the_Data}
setwd("~/Downloads")
us_startups <- read.csv("crunchbase_monthly_export_companies_1990_to_2014_us.csv")
```

## 2.2 Summary of the Data Set

```{r Summary}
dim(us_startups)
names(us_startups)
str(us_startups)
summary(us_startups)
```

### 2.2.1 Results from summary
##### In summary, this data set included 22888 objects of 12 variables. The top 2 hot markets are Software (2435 startups) and Biotechnology (1863 startups).California has greatest number of startups (8154). By reion, SF Bay Area has biggest number of startups (5738), and San Francisco (2275) and New York (2008) have more startups as compared to other cityies. 400 startups got 1 millions total fundings.


## 2.3 Explore the Individual Variables in the Data Set: Characteristics of Startups
##### To understand the properities of startups, six individual varibles are analyzed and visulized in the following in detail.

### 2.3.1 What type of market do startups focus on?
##### To visulize that, scatter plot together with text plot is created, which size of point or text reflect the number of startups in each market category.

``` {r distribution of types of markets of startups}
# calculate number for each market
markets <- as.data.frame(table(us_startups$market))
# scatter plot with different size representing size of markets
p0 <- ggplot(aes(x = Var1, y = Freq), data = markets) 
p0_1 <- p0 + geom_point(aes(size = Freq), color = "pink") + 
  geom_text(aes(label = Var1, size = Freq)) +
  theme_bw()
p0_1
```

##### Software and Biotechology are two biggest markets for startups observed from the plot. To see details of underpresented markets, scale of y axis is adjusted using log10.

```{r adjust y scale}
# adjust y scale to see more details
p0_1 + scale_y_log10()
```

### 2.3.2 How many total fundings startups usually get?
##### To see that, a histogram of total fundings is created.

```{r Distribution of total fundings}
# total fundings
# convert factor to be numeric 
us_startups$funding_total_usd <- as.character(us_startups$funding_total_usd)
us_startups$funding_total_usd <- as.numeric(gsub(",", "", us_startups$funding_total_usd))
p1 <- ggplot(aes(x = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd) & status != ""))
# histogram with default seeting
p1_1 <- p1 + geom_histogram()
p1_1
```

##### The histogram showed a long tail, which can not see clearly. To better understand the data, scale of x axis, binwith is adjusted.

```{r adjust x scale and binwidth}
# transform the long tail data to better understand the distribution of fundings
p1_1 + scale_x_log10()
# freqpoly
p1 + geom_freqpoly() + scale_x_log10()
# adjust binwidth to see detail
p1 + geom_histogram(binwidth = 0.2) +  
  scale_x_log10(breaks = c(1e+03, 1e+04, 1e+05, 1e+06, 1e+07, 1e+08, 1e+09))
```

##### The figures showed a normal-like distribution. Then, the histogram is split by status of startups to see if any different distributions for different status of startups.

```{r split by status}
# check if any difference for startups with diferent status
p1 + geom_histogram(aes(x = funding_total_usd, y = ..density.., fill = status), binwidth = 0.2) + 
  labs(x = "Total fundings ($USD)", y = "Count") + 
  ggtitle("Histogram of total fundings for startups ($USD, log10)") + 
  scale_x_log10(breaks = c(1e+04, 1e+06, 1e+08)) +
  facet_wrap(~ status)
```

##### The distribution pattern for each status of startups is very similar.


### 2.3.3 How many rounds of fundings startups get? 
##### To answer this question, a histogram of rounds of fundings is generated.

```{r Distribution of rounds of fundings}
p2 <- ggplot(aes(x = funding_rounds), data = us_startups)
# histogram with default seeting
p2 + geom_histogram()
# adjust binwidth
p2 + geom_histogram(binwidth = 1) + 
  scale_x_discrete(breaks = seq(1, 16, 1)) 
```

##### There are some bars can not be seen in this default setting of histogram. To visulize the underrepresented data, x and y limits are set.

```{r, setup x and y limits}
# set x and y scale to see underpresented data
p2 + geom_histogram(binwidth = 1) + 
  coord_cartesian (xlim = c(5, 15), ylim = c(0, 1000))  
```

##### Startups usually got 1 round of funding and number of startups for getting more rounds of fundings decreased.

### 2.3.4 Are there more startups in certain years, days or months?

##### First, number of startups from 1990 to 2014 is explored using histogram.
```{r Distribution of founded years of startups}
p3 <- ggplot(aes(x = founded_year), data = us_startups)
# histogram of founed years
p3 + geom_histogram() + 
  scale_x_discrete(breaks = seq(1990, 2014, 1)) + 
  coord_cartesian(xlim = c(1989, 2015))
```

##### Then, number of startups for each month is explored using histogram.

```{r startups in months}
# get months from founded_at factor
us_startups$founded_at <- as.character(us_startups$founded_at)
us_startups$founded_month <- strftime(as.Date(us_startups$founded_at, "%m/%d/%Y"),"%m")
us_startups$founded_month <- as.numeric(us_startups$founded_month)
# histogram of founded months
p4 <- ggplot(aes(x = founded_month), data = us_startups)
p4 + geom_histogram(binwidth = 1)
```

##### Last, number of startups for each day in a month is explored using histogram.

```{r startups in days}
# get days from founded_at factor
us_startups$founded_day <- strftime(as.Date(us_startups$founded_at, "%m/%d/%Y"),"%d")
us_startups$founded_day <- as.numeric(us_startups$founded_day)
# histogram of founded days
p5 <- ggplot(aes(x = founded_day), data = us_startups)
p5 + geom_histogram(binwidth = 1) + 
  scale_x_discrete(breaks = seq(0, 31, 1))
```

##### The number of startups increased until 2012 and then droped down.There are more startups founded on January and first day of each month.

### 2.3.5 How startups distributed in different states, regions and cities in US?

##### To address this question, a US map is created. The scatter plot is generated in each state in the US map. The size of point in each state indicates number of startups in that state.

```{r Region distributation}
# distributions in states: which state has more startups?
# load us map data
us_state_map <- map_data("state")
states <- data.frame(state.center, state.abb)
# calculate frequency of startups in each state
regions <- as.data.frame(table(us_startups$state_code))
# merge data of startups with states
colnames(regions)[1] <- "state.abb"
regions <- merge(states, regions, by = "state.abb", all = TRUE)
# draw us map
p6 <- ggplot(aes(x = long, y = lat, group = group), data = us_state_map) 
# use size of points to represent number of startups in each state
p6 + geom_polygon(fill = "white") + 
  geom_path(colour = 'grey', linestyle = 2) +
  geom_point(data = regions, aes(x = x, y = y, group = NULL,  size = Freq), color = "red") +
  geom_text(data = regions, aes(x = x, y = y, label = state.abb, group = NULL), size = 3, color = "blue") + 
  coord_map("polyconic") + 
  theme_bw()
```

##### Not suprisingly, californica is the state with greatest number of startups. Then, the distribution of startups in each region is explored using scatter and text plot.

```{r startups in each region}
# distribution in regions: which region has more startups?
# get number of startups in each region
startups_by_regions <- as.data.frame(table(us_startups$region))
# plot the graph
p7 <- ggplot(aes(x = Var1, y = Freq), data = startups_by_regions)  +
  theme_bw() + 
  scale_y_log10()
p7 + geom_point(aes(size = Freq), color = "pink") + 
  geom_text(aes(label = Var1, size = Freq))
```

##### Yes, SF bay area is the favourite region for startups. So, which city is famous for startups? To look that, number of startups in each city is created and plotted.

```{r startups in each city}
# distribution in cities: which city has more startups?
# get number of startups in each city
startups_by_cities <- as.data.frame(table(us_startups$city))
# creat graph
p8 <- ggplot(aes(x = Var1, y = Freq), data = startups_by_cities) +
  theme_bw() + 
  scale_y_log10()
p8 + geom_point(aes(size = Freq), color = "pink") + 
  geom_text(aes(label = Var1, size = Freq)) 
```

##### San Francisco and New York are shown up obviously in the graph. 

### 2.3.6 What's the status of startups?

##### Pie chart is created to look at the status of startups.

```{r Status of startups}
# pie chart of number of startups in different status
p9 <- ggplot(aes(x = factor(1), fill = status), data = subset(us_startups, status != ""))
p9_1 <- p9 + geom_bar() + 
  coord_polar(theta = "y")
p9_1
```

##### Most of the startups are still in operating. Any different in states for status of startups? To look that, pie chart of number of startups in different status is split by states

```{r pie chart by states}
# pie chart split by states
p9_1 + facet_wrap(~state_code)
```

##### CA definitely has more startups in operating. Any different in founded_years for status of startups? pie chart of number of startups in different status is split by founded years

```{r pie chart by founded year}
# split pie chart by founded year
p9_1 + facet_wrap(~founded_year)
```

##### 2011 and 2012 had more startups in operating.

### 2.3.7 Observations and Interpretations for Exploration of Individual Variables.
##### 1. What type of market do startups focus on? Software and biotechnology markets have more startups as compared with other markets, which suggest these two markets are hot area for startups. 
##### 2. How many total fundings startups usually get? Most startups got 1 million dolloars total fundings.
##### 3. How many rounds of fundings startups get? Most startups only got 1 round of funding, and few startups got fundings more than 10 rounds.
##### 4. Are there more startups in certain years, days or months? Startups increased from 1990 to 2012, and then decreased from 2013 which may reflect economic regression. There are more startups founded in January and first day of each month. This may due to people fakely reported the first day and first month of years as founded day for their startups.
##### 5. How startups distributed in different states, regions and cities in US? California has the greatest number of startups. Consistently, SF BAY AREA in california has more startups. Particularly, San Francisco and New York have more startups as compared to other cities. 
##### 6. What's the status of startups? Most startups are in operating.

## 2.4 Explore relationships between two variables: get more fundings? 
##### Then, the relationships between total fundings and other variables such as startup market and state was measured.

### Which type of startups get more fundings? 
##### To find which market for startups get more fundings, hot startups, which are defined as number of startups more than 500 in that market here, are analyzed.

```{r fundings for hot market of startups}
# get subset data of markets with number of startups > 500
sub_markets <- subset(markets, Freq > 500 & !Var1 == "") 
c_market <- c(as.character(sub_markets$Var1))
# list hot market for startups
c_market
hot_startups <- subset(us_startups, market %in% c(" Advertising ", " Biotechnology ", " Curated Web ", " E-Commerce "," Enterprise Software ", " Hardware + Software ", " Health and Wellness ", " Health Care ", " Mobile ", " Software " )&!is.na(funding_total_usd))
# draw scatter plot
p10 <- ggplot(aes(x = market, y = funding_total_usd), data = hot_startups) + scale_y_log10()
p10 + geom_point(aes(color = market)) 
```

##### It's difficult to see difference with scatter plot. So, boxplot is explored.

```{r boxplot}
# draw a boxplot
p10_1 <- p10 + geom_boxplot(aes(fill = market))
p10_1
# adjust y scale to better compare
p10_2 <- p10_1 + coord_cartesian(ylim = c(1e+05, 1e+08))
p10_2
```

##### From above visulization, health care and enterprise software usually got more total fundings by median. Then, do initial fundings for hot markets of startups have difference?

```{r initial fundings}
# initial funding for each type of market
p10_3 <- ggplot(aes(x = market, y = funding_total_usd), data = subset(hot_startups, funding_rounds == 1)) + scale_y_log10()
p10_4 <- p10_3 + geom_point(aes(color = market)) 
p10_5 <- p10_3 + geom_boxplot(aes(fill = market))
grid.arrange(p10_4, p10_5, ncol = 1)
```

##### From the plot, health care, biotechnology, enterprise software got more initial fundings by median. To see the extract mean and median, I summarise the data.

```{r mean and median}
# mean and median for total fundings
hot_startups.by.market <- hot_startups %>%
  group_by(market) %>%
  summarise(
            mean_fundings = mean(funding_total_usd),
            median_fundings = median(funding_total_usd),
            mean_rounds = mean(funding_rounds),
            median_rounds = median(funding_rounds),
            n = n()
            ) %>%
  arrange(desc(mean_fundings))
# output
hot_startups.by.market
# mean and median for initial fundings
hot_startups.by.market.ini <- subset(hot_startups, funding_rounds == 1) %>%
  group_by(market) %>%
  summarise(
            mean_fundings = mean(funding_total_usd),
            median_fundings = median(funding_total_usd),
            mean_rounds = mean(funding_rounds),
            median_rounds = median(funding_rounds),
            n = n()
            ) %>%
  arrange(desc(mean_fundings))
# output
hot_startups.by.market.ini
```

##### Which variables are correlated with total fundings of startups? To answer that, 5000 samples are selected to run ggparis.

```{r ggpairs}
# sample 5000 starups from data set
set.seed(200)
hot_startups_samp <- hot_startups[sample(1: length(hot_startups$market), 5000), ]
ggpairs(hot_startups_samp, params = c(shape = I("."), outlier.shape = I(".")))
```

### Do specific year for startups get more fundings?
##### First, draw a scatter plot and a boxplot using total fundings and year 

```{r total fundings for each year}
# scatter plot for total fundings each year
p11 <- ggplot(aes(x = founded_year, y = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd))) + scale_y_log10()
p11_1 <- p11 + geom_point(aes(color = founded_year))
# add a conditional mean
p11_2 <- p11_1 + stat_summary(fun.y = mean, geom = "line", color = "red")
# add a conditional median
p11_3 <- p11_1 + stat_summary(fun.y = median, geom = "line", color = "green")
# plot in a row
grid.arrange(p11_2, p11_3, ncol = 1)
```

##### Then, draw a scatter plot using initial fundings and year 

```{r initial fundings for each year}
# scatter plot for initial fundings each year
p11_3 <- ggplot(aes(x = founded_year, y = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd)&funding_rounds == 1)) + scale_y_log10()
p11_4 <- p11_3 + geom_point(aes(color = founded_year))
# add a conditional mean
p11_5 <- p11_4 + stat_summary(fun.y = mean, geom = "line", color = "red")
# add a conditional median
p11_6 <- p11_4 + stat_summary(fun.y = median, geom = "line", color = "green")
# plot in a row
grid.arrange(p11_5, p11_6, ncol = 1)
```

### Do specific state get more fundings?
##### First, draw a scatter plot using total fundings and state code

```{r total fundings for each state}
# scatter plot for total fundings each state
p12 <- ggplot(aes(x = state_code, y = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd))) + scale_y_log10()
#draw scatterplot
p12_1 <- p12 + geom_point(aes(color = state_code))
p12_1 <- p12_1 + theme(legend.position = "none", axis.text=element_text(size=6))
# draw boxplot
p12_2 <- p12_1 + geom_boxplot (aes(fill  = state_code)) 
# arrange in a column
grid.arrange(p12_1, p12_2, ncol = 1)
```

##### Then, draw a scatter plot using initial fundings and state code

```{r initial fundings for each state}
# scatter plot for initial funding each state
p12_3 <- ggplot(aes(x = state_code, y = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd)&funding_rounds == 1)) + scale_y_log10()
#draw scatterplot
p12_4 <- p12 + geom_point(aes(color = state_code))
p12_4 <- p12_4 + theme(legend.position = "none", axis.text=element_text(size=6))
# draw boxplot
p12_5 <- p12_4 + geom_boxplot (aes(fill  = state_code)) 
# arrange in a column
grid.arrange(p12_4, p12_5, ncol = 1)
```

### Any relationship between status of startups and founding they get?
##### First, compare total fundings of startups in each status

```{r ralationship between fundings and status of startups}
# scatter plot and boxplot for total fundings by status of startups
p13 <- ggplot(aes(x = status, y = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd) & status != "")) + scale_y_log10()
p13_1 <- p13 + geom_point(aes(color = status))
# boxplot
p13_2 <- p13_1 + geom_boxplot(aes(fill = status))
# draw two plots in a row
grid.arrange(p13_1, p13_2, ncol = 1)
```

##### The initial fundings of startups in each status are also compared

```{r initial fundings for startups in each status}
# scatter plot for initial funding
p13_3 <- ggplot(aes(x = status, y = funding_total_usd), data = subset(us_startups, !is.na(funding_total_usd) & status != "" & funding_rounds== 1)) + scale_y_log10()
p13_4 <- p13_3 + geom_point(aes(color = status))
# box plot for initial funding
p13_5 <- p13_4 + geom_boxplot(aes(fill = status))  
# draw two plots in a row
grid.arrange(p13_4, p13_5, ncol = 1)
```

##### Finally, the statistical analyses between total_funding and founded_year, state_code, region, city or status are performed using ANOVA 

```{r statistical analysis}
# ANOVA analyses for total fundings
fit <- aov(funding_total_usd ~ founded_year + state_code + region + city + status, data = us_startups)
summary(fit)
# ANOVA analyses for initial fundings
fit_ini <- aov(funding_total_usd ~ founded_year + state_code + region + city + status, data = subset(us_startups, funding_rounds == 1))
summary(fit_ini)
```

### Observations and Interpretations for Exploration of Two Variables.
##### 1. Which type of startups get more fundings? Startups targeting to health care and enterprise software market usually got more total fundings. Startups targeting to health care, biotechnology and enterprise software got more initial fundings.
##### 2. Do specific year for startups get more fundings? Although there are more startups got funding in recent year, the mean and median of total fundings decreased from 1990 to 2014, which may due to economic regression. 
##### 3. Do specific state get more fundings? The plot did not show obvious difference between states.
##### 4. Any relationship between status of startups and founding they get? Startups in acquired and operating status got more total fundings and initial fundings.
##### 5. Results of statistical analyses. The stastistical analysis showed that the total fundings had significantly different among founded years, states and status of startups but not among regions and cities. The initial fundings only showed significant difference among founded years.


## 2.5 Analyzing Three or More Variables: focusing on hot startups?

### First, total fundings vs year by market of hot startups is explored.

```{r total fundings vs year by market }
# draw scatter plot
p14 <- ggplot(aes(x = founded_year, y = funding_total_usd), data = hot_startups) + scale_y_log10()
p14_1 <- p14 + geom_point(aes(color = market))
# add mean to each market (line)
p14_2 <- p14_1 + stat_summary(fun.y = mean, geom = "line", aes(color = market))
p14_2
```

### Then, total fundings vs state by hot startups is explored

```{r total fundings vs state by hot startups}
# draw line plot
p15 <- ggplot(aes(x = state_code, y = funding_total_usd), data = hot_startups) + scale_y_log10() + theme(axis.text=element_text(size=6))
p15_1 <- p15 + geom_line(aes(color = market))
# add conditional mean to each market (point)
p15_2 <- p15_1 + stat_summary(fun.y = mean, geom = "point", size = 5, aes(color = market))
p15_2
```

### Next, compare total fundings vs status by hot startups

```{r total fundings vs status by hot startups}
# draw line plot
p16 <- ggplot(aes(x = status, y = funding_total_usd), data = subset(hot_startups, status != "")) + scale_y_log10()
p16_1 <- p16 + geom_line(aes(color = market))
# add conditional mean to each market (point)
p16_2 <- p16_1 + stat_summary(fun.y = mean, geom = "point", size = 5, aes(color = market))
p16_2
```

### Then, explore total fundings vs funding rounds by hot startups

```{r total fundings vs funding rounds}
# draw a scatter plot
p17 <- ggplot(aes(x = funding_rounds, y = funding_total_usd), data = hot_startups) + scale_y_log10()
p17_1 <- p17 + geom_point(aes(color = market))
# add conditional mean to each market (line)
p17_2 <- p17_1 + stat_summary(fun.y = mean, geom = "line", aes(color = market))
p17_2
```

### Finally, rising star or bubble?
```{r number of startups in each status}
# load library
suppressMessages(library(plyr))
# sum total fundings by market by status
total_funding_by_status_by_market <- subset(hot_startups, status  != "", select = c("market", "status", "funding_total_usd")) %>%
  group_by(market, status) 
total_funding_by_status_by_market <- ddply(total_funding_by_status_by_market, c("market", "status"), summarize, fundings = sum(funding_total_usd))
# count number of startups in each status by each market
number_of_startups_by_status <- count(subset(hot_startups, status  != ""), c("market","status"))
# merge total fundings to number of startups data frame
number_of_startups_by_status <- merge(number_of_startups_by_status, total_funding_by_status_by_market, by = c("market", "status"))
# draw a scatter plot to reflect number of startup in each status by market, the size of point represents amount of total fundings
ggplot(aes(x = status, y = freq), data = number_of_startups_by_status) + 
  scale_size_area(max_size = 20) +
  scale_y_log10() +
  geom_point(aes(color = market, size = fundings), position = position_jitter(w = 0.4))
```

### Observations and Interpretations for Exploration of Three or more Variables.

##### 1. Total fundings vs year by hot startups: there are no obvious difference of getting total fundings among founded years in different markets.
##### 2. Total fundings vs state by hot startups: in most states, health care (18 states) and biotechnology (10 states) got more total fundings
##### 3. Total fundings vs status by hot startups: startups in health care market got more fundings when they are in acquired or operating status. While, Startups in biotechnology market got more fundings when they are in closed status.  
##### 4. Total fundings vs funding rounds by hot startups: usually, startups got more rounds of fundings have more total fundings. 
##### 5. Rising star or bubble? There are greatest number of startups in software market in acquried, operating and closed status, suggesting fast change in this market. The biotechnology market has close number of startups to software market in operating status, but lower number of startups in closed status, which may implicate a strong rising in this market.

------

# 3. Final Plots and Summary

## 3.1 Plot One: how many total fundings startups usually get?
```{r Plot_One_total fundings for startups with different status}
# Histogram of total fundings for startups with diferent status
p1 <- ggplot(aes(x = funding_total_usd), data = subset(us_startups, status != ""))
p1 + geom_histogram(aes(x = funding_total_usd, y = ..density.., fill = status), binwidth = 0.2) + 
  theme(axis.text=element_text(size=10)) + 
  labs(x = "Total fundings ($USD)", y = "Count") + 
  ggtitle("Histogram of total fundings for startups ($USD, log10)") + 
  scale_x_log10(breaks = c(1e+04, 1e+06, 1e+08)) +
  facet_wrap(~ status)
```

### 3.1.1 Description One
##### From this plot, it's observed that most startups got 1 million dolloars total fundings. This is true whatever the status of startups is.

## 3.2 Plot Two: which market of hot startups get more fundings.
```{r Plot_Two_hot market}
# add title and labs
p10 <- ggplot(aes(x = market, y = funding_total_usd), data = hot_startups) + scale_y_log10() + 
  theme(axis.text=element_text(size=8)) +
  ggtitle("Fundings for each market of hot startups ($USD, log10)") + 
  labs(x = "Market of startups", y = "Total fundings ($USD)") + 
  geom_point(aes(color = market))
# draw a boxplot
p10_1 <- p10 + geom_boxplot(aes(fill = market))
p10_1
```

### 3.2.1 Description Two
##### Obversation from this plot showed that startups targeting to health care and enterprise software market usually got more total fundings. Startups targeting to health care, biotechnology and enterprise software got more initial fundings.

## 3.3 Plot Three: which market of hot startup get more funding in each state
```{r Plot_Three_total fundings vs state by hot startups}
# draw line plot and add titles and labs 
p15 <- ggplot(aes(x = state_code, y = funding_total_usd), data = hot_startups) + 
  scale_y_log10() + 
  theme(axis.text=element_text(size=8)) +
  ggtitle("Fundings ($USD, log10) for each market of hot startups in each state") + 
  labs(x = "States", y = "Total fundings ($USD)")
p15_1 <- p15 + geom_line(aes(color = market))
# add conditional mean to each market (point)
p15_2 <- p15_1 + stat_summary(fun.y = mean, geom = "point", size = 5, aes(color = market))
p15_2
```

### 3.3.1 Description Three
##### In this plot, it showed that health care (18 states) and biotechnology (10 states) were two markets got more total fundings in US states.

## 3.4 Plot Four: rising star or bubble?
```{r Plot_Four_number of startups in each status}
# sum total fundings by market by status
total_funding_by_status_by_market <- subset(hot_startups, status  != "", select = c("market", "status", "funding_total_usd")) %>%
  group_by(market, status) 
total_funding_by_status_by_market <- ddply(total_funding_by_status_by_market, c("market", "status"), summarize, fundings = sum(funding_total_usd))
# count number of startups in each status by each market
number_of_startups_by_status <- count(subset(hot_startups, status  != ""), c("market","status"))
# merge total fundings to number of startups data frame
number_of_startups_by_status <- merge(number_of_startups_by_status, total_funding_by_status_by_market, by = c("market", "status"))
# draw a scatter plot to reflect number of startup in each status by market, the size of point represents amount of total fundings
ggplot(aes(x = status, y = freq), data = number_of_startups_by_status) + 
  scale_y_log10() +
  geom_point(aes(color = market, size = fundings), position = position_jitter(w = 0.4)) + 
  scale_size_area(max_size = 20) + 
  theme(axis.text=element_text(size=10)) +
  ggtitle("Number of hot startups (log10) for each market in each status") + 
  labs(x = "Status", y = "Number of hot startups (log10)")
```

### 3.4.1 Description Four
##### There are greatest number of startups in software market in acquried, operating and closed status, suggesting fast change in this market. The biotechnology market has close number of startups to software market in operating status, but lower number of startups in closed status, which may implicate a strong rising in this market. In addition, startups in operating usually get more total fundings which may be due to more rounds of funds.

------

# 4. Reflection

### Conclusions
##### The startups data set contains information on 22888 startups from 1990 to 2014 in USA. I started by understanding the characteristics of startups through analyzing individual variables in the data set. The analyses were led by initial interesting questions and followed by observations from plots. In these analyse, I found that most startups got 1 million dolloars total fundings, more startups in california, particularly in SF BAY Area, and Software and Biotechnology are two hottest market for startups. Then, I explored relationships between total fundings and other variables such as founded year, state, market. Interestingly, startups targeting to health care and enterprise software market usually got more total fundings. Startups targeting to health care, biotechnology and enterprise software got more initial fundings. Finally, I focused on hot markets with more than 500 startups. The total fundings for each market across different viariables such as states, founded year were explored. The results showed that health care (18 states) and biotechnology (10 states) were two markets getting more total fundings in US states.I also noticed that software market was the most fast changed market as there are greatest number of startups in in acquried, operating and closed status.The biotechnology market is a rising market because it has close number of startups to software market in operating status, but lower number of startups in closed status. Also, startups in biotechnology market got most fundings when they are in operating. This analysis focused on startups in US states, it's will be very interesting to analyze hot startups in world in future exploration using dataset including global startups.


### Potential issues
##### When I analyze the data set, I notice that there are missing values. For instance, the analyses focused on exploring relationships between total fundings and other variables, but about 3000 values of total fundings in the dataset are missed. They also may include some fake data in the dataset. For example, the analyses show that most startups founded in the first day of each month and January of each year. This may due to fake reporting of founded date. Another issue is the data set may be incomplete because it's likely that not all startups are record. These potential issues may impact some of the results of analyses.  