<h1> Get Outside: </h1>
<hr>
<h2>Predicting Annual Visits to the Nation's 5 most-visited national Parks<h2/>
<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">


<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Logo_of_the_United_States_National_Park_Service.svg/1920px-Logo_of_the_United_States_National_Park_Service.svg.png" width="300" height="300">
<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">

## Executive Summary:

### A. This project analyzed data from NPS records going back to 1979 at the nation's top 5 most visited national parks to predict visitors for the final 6 years on record, 2016-2021.

### B. The best predictive model is a seasonal analysis mdoel, using trend data and historical patterns to predict future park visits. The error rate (RMSE) produced in the final forecast is 1.8 mn visits, or roughly 25% of total estimated visits. The period for estimated visits notably included an anomaly event, the 2020 pandemic, that may have afffected the final error rate


<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">

## Project Outline:

## 1. Acquire/Prepare: Source the data from NPS.GOV and produced a composite dataframe for 5 parks and a total visits column for Exploration and Modeling.

## 2. Data Exploration: explored the distribution and seasonality of visits to determine peak periods of visitation, as well as individual park trends if they exist. Also use seasonal decompostion to identify underlying trends.

## 3. Modeling: Create models that will forecast visitorship, using Time Series methods including last observed value, simple moving average, rolling average, Holts-Winter linear method, and Seasonal Trend.

<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">
    


<h2>Data Dictionary</h2>
<br>
<b>Yellowstone: Yellowstone park visitors, monthly</b>
<br>
<b>Zion: Zion park visitors, monthly</b>
<br>
<b>Grand_canyon: Grand_canyon park visitors, monthly</b>
<br>
<b>Rocky_MTN: Rocky_MTN park visitors, monthly</b>
<br>
<b>Great_Smoky_MTNs: Great_Smoky_MTNs park visitors, monthly</b>
<br>
<b>Total_Visitors: Aggregate NTL park visitors, monthly</b>

<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">

## 4. Conclusion/Takeways:

### A. The best predictive model is a seasonal ESM model, using trend data and historical patterns to predict future park visits. The error rate (RMSE) produced in the final forecast is 1.8 mn visits, or roughly 25% of total estimated visits. The period for estimated visits notably included an anomaly event, the 2020 pandemic, that may have afffected the final error rate.

### B. Next steps: Use the Facebook Prophet TimeSeries model to see if that can beat my established baseline. 

<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">

## 5. Reproduce this project:
- download the CSV files from the NPS at the links included in the final project notebook
- utilize the wrangle fucntion for data prepartaion and cleaning, to generate the final Dataframe used in this project.
- all helper functions are available in the assocaited wrangle.py

