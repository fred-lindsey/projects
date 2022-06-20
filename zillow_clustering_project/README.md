<h1>Zillow Clustering Project:</h1>

<h3>Predicting the Error in Zestimate, using clustering and Regression</h3>
<br>
<h3>Project Purpose</h3>
<h4> 1.  Construct an ML Regression model that predict property tax assessed values ('taxvaluedollarcnt') of Single Family Properties using attributes of the properties.</h4>
<br>
<br>
<h3> Executive Summary</h3>
<br>
1. clustering did not significantly improve the modeling process when incorporated as a feature
<br>
2. clustering was helpful in identifying and narrowing variable connection to the target variable, LOGERROR
<br>
3. I found SQ FT, YR BUILT and FIPS to be the main drivers of LOGERROR
<br>
4. Modeling with clusters results: LOGERROR RMSE baseline: 0.0007, LOGERROR RMSE with clusters in the model: 0.183. 
<br>
<h3> I investigated the following quesions</h3>
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
1. I retained the following columns through the final modeling process:
<br>
- bathroomcnt: number of bathrooms in residence
<br>
- bedroomcnt: number of bedrooms in residence
<br>
- calculatedfinishedsquareft: the size in sq ft of the finished home
<br>
- lotsizesquareft: the property size in sq ft of the property lot
<br>
- roomcnt: number of rooms in the residence
<br>
- yearbuilt: year the residence was constructed

<h2> Project Outline </h2>
<h3> B. DS pipeline and Linear Regression specific tasks: </h3>
<hr style="border-top: 10px groove blue; margin-top: 1px; margin-bottom: 1px">
<br>
    <b>a. Acquire/Wrangle Data</b>
    <br>
        i. acquire all tables from the Zillow Dataset through SQL query (avaialble in the wrangle.py file
        <br>
        1. initially I imported 9 coumns from those three tables through a SQL query in the initial Wrangle function.
        <br>
        ii. Remove nulls, outliers, and unneeded columns
    <br>
    1. I removed outliers by a function that defined outliers as quantitative variables more than 3 standard deviations outside the norm. This did not affect more than 5% of the data. I also removed all columns that were more than 25% null, and rows that were more than 10% null. The few remaining nulls were filled with the mean values from the column average.
    <br>
        iii. Run distributions to view data at 30k feet (get a sense for dataset)
    <br>
        iv. split data into train, validate, test. 
    <br>
    <b>b. Explore Data:</b>
        <br>
        i. hypothesize/pose questions, visually explore relationships with bivariate stats, produce subsets of interest, answer hypotheses visually, statistically, and in English
        <br>
   <b>c. Modeling:</b>
       <br>
       i. create a scaled copy of the data frame (don't scale target variable), and produce X/y split for modeling.
       <br>
       ii. produce a model that
           - a. error units will be RMSE (logerror)
       <br>
       iii. compare model's performance to the baseline, and the Zillow predictive model performance.
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
- Modeling with clusters results: LOGERROR RMSE baseline: 0.0007, LOGERROR RMSE with clusters in the model: 0.183. This model needs fine tuning before further use.
<h2> Reproduce this project </h2>
<br>
<hr style="border-top: 5px groove limegreen; margin-top: 1px; margin-bottom: 1px">

 1. Create a local copy of the wrangle.py, and split.py files in this repo. Note: you will need to contact CodeUp database admin for access to the CodeUp DB for any non-public data accessed through an SQL query to the DB.
 2. Once the data import is complete, use the libraries noted in the EDA and Modeling sections to run statistical tests and predictive modeling on the data. The Wrangle module will produce a clean dataframe within the parameters noted in the function