<h1>TELCO Churn Project:</h1>

<h3>Leveraging our Data to Predict and Prevent Customer Erosion</h3>

<h2>This project exists to answer two questions:</h2>
<br>
<h3> Why are customers churning?</h3>
- because of price and payment pressures in 3 specific areas: monthly contracts, e-check payments, and fiber optic internet plans.
<br>
<h3> Who will churn? </h3>
- many customers are at risk of churning, but the risk is significantly higher for monthly contract, fiber optic customers paying by e-check.
<br>
<br>
<h3> I explored these variable relationships, as well as the questions that follow, through univariate and then bivariate statistical analysis</h3>

<h4>Variable relationships to explore:</h4>

    1. Churn: Payment Type (Cat/Cat)
    2. Churn: Total Charges (Cat/Cont)
    3. Churn: Monthly Charges (Cat/Cont)
    4. Churn: Dependents (Cat/Cat)
    5. Churn: Senior Citizen (Cat/Cat)
    6. Churn: Tenure (Cat/Cont)
    7. Churn: Gender (Cat/Cat)
    8. Churn: Internet Service (Cat/Cat)
    9. Churn: Contract Type
    
<div class="alert alert-block alert-success">
    <b>Q1.</b> Are internet customers churning at significantly different rates?
</div>
<br>
<div class="alert alert-block alert-success">
    <b>Q2.</b> Is payment type driving churn?
</div>
<br>
<div class="alert alert-block alert-success">
    <b>Q3.</b> Is contract type influencing churn at significantly different rates?
</div>
<br>
<div class="alert alert-block alert-success">
    <b>Q4.</b> How does average tenure vary by payment type?    
</div>

<h2>Data Dictionary</h2>
<br>
<b>Customer Identification and Demographic Data:</b>
<br>
Customer ID (String), 
Gender (Male/Female), 
Partner status (Bool), 
Dependent status (Bool), 
Senior citizen status (Bool)
<br>
<b>Customer Relationship information:</b>
<br>
Tenure in months (float),
Monthly charges ($USD) (float), 
Total charges ($USD) (float), 
Paperless Billing (Bool), 
Payment type (categorical), 
<br>
<b>Phone Service, with service option columns:</b>
<br>
Multiple lines : One Line, Multiple Lines, No Phone Service (categorical)
<br>
Internet Service Type: Fiber Optic, DSL, None (categorical)
<br>
<b>Internet Service Option columns (all bool):</b>
<br>
Online security, 
Online backup, 
Device protection, 
Tech support, 
Streaming TV, 
Streaming movies, 
Churn status (bool)

<h2> Project Outline </h2>
<h3>1. Acquire, prepare and clean TELCO data set.</h3>
<br>
- Split into train, validate, test sets.
- create an encoded data set for modeling, and retain an unencoded set for EDA. 
<br>
<h3>2. Perform Exploratory Data Analysis on the unencoded data set</h3>
<br>
- explore/demonstrate variable relationships graphically
- set null and alternate hypotheses to reject/fail to reject
- run statistical testing on related variables/variables of interest driving churn
- document takeaways
<br>   
<h3>3. Do some Modeling:</h3>
<br>
- demonstrate 3 models
- Pick highest performing models to run on validate set
- Run the highest performing model on the test data
- document takeaways and conclusion
- produce a predictions CSV to predict customer churn
<br>
<h3>4. Deliver Recommendations:</h3>
<br>

<h2> Key Findings</h2>
<br>
<hr style="border-top: 5px groove limegreen; margin-top: 1px; margin-bottom: 1px">
1. Payment Type (e-check), Contract Type (monthly), and Internet Service Type (Fiber) are the primary drivers of churn among departing customers.
    <br>
    <br>
2. Model Accuracy: The Logistic Regression Model provided accuracy of <b>80.5%</b> on the out-of-sample (test) data. Given additional time for fine tuning, I would include additional c-values in the LR model to tweak overall accuracy, and run more Chi2 testing to guide some feature engineering.
<h2> Recommendations </h2>
<br>
<hr style="border-top: 5px groove limegreen; margin-top: 1px; margin-bottom: 1px">

<b> 1. Retain existing high risk-of-churn customers </b>
    5% reduction in price for monthly fiber plans, and any customer identifed with >50% risk of churn
<br>
<b> 2. Convert existing monthly customers into 1- and 2- year customers</b>
    1 free month of service for conversion to 1 yr plans, 2 months for 2 yr plans
<br>
<b> 3. Automate bill pay to eliminate the pain of paying</b>
    10% reduction in monthly bill for 6 months for signing up with valid autopay method of payment
<h2> Key Findings</h2>
<br>
<hr style="border-top: 5px groove limegreen; margin-top: 1px; margin-bottom: 1px">
1. Payment Type (e-check), Contract Type (monthly), and Internet Service Type (Fiber) are the primary drivers of churn among departing customers.
    <br>
    <br>
2. Model Accuracy: The Logistic Regression Model provided accuracy of <b>80.5%</b> on the out-of-sample (test) data. Given additional time for fine tuning, I would include additional c-values in the LR model to tweak overall accuracy, and run more Chi2 testing to guide some feature engineering.
<h2> Reproduce this project </h2>
<br>
<hr style="border-top: 5px groove limegreen; margin-top: 1px; margin-bottom: 1px">

 1. Create a local copy of the acquire.py, prepare.py, and split.py files in this repo. Note: you will need to contact CodeUp database admin for access to the CodeUp for any non-public data. 
 2. Once the data import is complete, use the libraries noted in in the EDA and Modeling sections to run statistical tests and predictive modeling on the data.