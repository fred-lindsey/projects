<h1>Zillow Price Predictor:</h1>

<h3>Predicting the Price of Single Family Homes</h3>
<br>
<h3>Project Purpose</h3>
<h4> 1.  I constructed an ML Regression model that predict property tax assessed values ('taxvaluedollarcnt') of Single Family Properties using attributes of the properties.</h4>
<br>
<br>
<h3> I explored these variable relationships, as well as the questions that follow, through univariate and then bivariate statistical analysis</h3>

<h4>Big Assumptions I wanted to test/answer:</h4>
<br>
1. Newer homes are more desirable to consumers than older homes
<br>
2. Some locations/counties are more desirable than others to consumers
<br>
3. Locations (counties) with newer homes are more desirable to consumers
<br>
4. Locations (counties) with larger homes are more desirable to consumers
<br>
    
<div class="alert alert-block alert-success">
    <b>Q1.</b> Are home prices significantly different pre-/post- 1963?
</div>
<br>
<div class="alert alert-block alert-success">
    <b>Q2.</b> Does the county where a home is located have a significant impact on price?
</div>
<br>
<div class="alert alert-block alert-success">
    <b>Q3.</b> Does the county where a home is located have a significant impact on sq_ft?
</div>
<br>
<div class="alert alert-block alert-success">
    <b>Q4.</b> Is the average house newer in some counties than others?    
</div>

<h2>Data Dictionary</h2>
https://www.kaggle.com/competitions/zillow-prize-1/data?select=zillow_data_dictionary.xlsx

<h2> Project Outline </h2>
<h3> B. DS pipeline and Linear Regression specific tasks: </h3>
<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">
<br>
    <b>a. Acquire/Wrangle Data</b>
    <br>
        i. properties_2017, predictions_2017, propertylandusetype tables from SQL query in the zillow data set
        <br>
        1. initially I imported 9 coumns from those three tables through a SQL query in the initial Wrangle function.
        <br>
        ii. Remove nulls, outliers, and unneeded columns
    <br>
    1. I removed outliers by a function that defined outliers as quantitative variables more than 3.5 standard deviations outside the norm. This did not affect more than 2% of the data.
    <br>
    2. I removed the columns 'taxamount' (leaky column) and garage_car_cnt (over 50% null)
        iii. Run distributions to view data at 30k feet (get a sense for dataset)
    <br>
        iv. split data into train, validate, test
    <br>
    <b>b. Explore Data:</b>
        <br>
        i. hypothesize/pose questions, visually explore relationships with bivariate stats, produce subsets of interest, answer hypotheses visually, statistically, and in English
        <br>
        ii. produce synthetic columns if needed (BR/BD count, groupby's)
        <br>
   <b>c. Modeling:</b>
       <br>
       i. create a scaled copy of the data frame (don't scale target variable)
       <br>
       ii. produce at least 4 models (more if time allows), and add to the DataFrame, as well as prediction error for each model.
           - a. error units will be RMSE (dollars)
       <br>
       iii. compare model's performance to the baseline, and the Zillow predicitive model performance.
    <br>
   <b>d. Report</b>
   <br>
       i. Produce a clean notebook and README, with HTML and visuals
       <br>
       ii. Docstrings on all functions
       <br>
       iii. make script/outline, time presentation
       <br>
<br>

<h2> Key Findings </h2>
<br>
1. Three out of four models produced almost identical predictive accuracy (measured by RMSE). That takeaway leads me to conclude that feature selection is significantly more important than selecting model type, in linear regression models.
    <br>
    <br>
2. Model Accuracy: The Polynomial Regression Model provided a reduced error of <b>28%</b>, or <b>90k dollars</b>on the out-of-sample (test) data over the baseline prediction. This is meaningdful given the median home price in the dataset is <b>462k dollars</b>
<br>
<br>
3. Given additional time for fine tuning, I would:
<br>
- split the data by county
<br>
- split again by pre- and post- 1963
<br>
- run recursive feature selection on the split datasets to select the most impactful variables, I think these would be different for different counties and time periods
<h2> Reproduce this project </h2>
<br>
<hr style="border-top: 5px groove limegreen; margin-top: 1px; margin-bottom: 1px">

 1. Create a local copy of the wrangle.py files in this repo. Note: you will need to contact CodeUp database admin for access to the CodeUp for any non-public data. 
 2. Once the data import is complete, use the libraries noted in the EDA and Modeling sections to run statistical tests and predictive modeling on the data.