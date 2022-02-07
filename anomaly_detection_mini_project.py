"""

Anomaly Detection of Retail Store Sales

This hands-on mini-project will enable you to reinforce your learnings pertaining to anomaly detection in this unit. By now, you must already be aware of the key objective of anomaly detection. Just to refresh your memory, anomaly detection is the identification of outliers or rare event items in a dataset which potentially exhibit abnormal behavior or properties as compared to the rest of the datapoints.

There are a wide variety of anomaly detection methods including supervised, unsupervised and semi-supervised. Typically you can perform anomaly detection on univariate data, multivariate data as well as data which is temporal in nature. In this mini-project you will leverage state-of-the-art anomaly detection models from frameworks like scikit-learn and PyOD.

By the end of this mini-project, you will have successfully applied these techniques to find out potential outliers pertaining to sales transactional data in a retail store dataset and also learnt how to visualize outliers similar to the following plot.

We will be performing anomaly detection on both univariate and multivariate data and leverage the following anomaly detection techniques.

    Simple Statistical Models (mean & standard deviation: the three-sigma rule)
    Isolation Forest
    Clustering-Based Local Outlier Factor
    Auto-encoders

1. Getting and Loading the Dataset

The first step towards solving any data science or machine learning problem is to obtain the necessary data. In this scenario, we will be dealing with a popular retail dataset known as the SuperStore Sales Dataset which consists of transactional data pertaining to a retail store.
Please download the required dataset from here if necessary, although it will also be provided to you along with this notebook for this mini-project

Once we have the necessary data, we will load up the dataset and perform some initial exploratory data analysis
2. Exploratory Data Analysis

It's time to do some basic exploratory analysis on the retail store transactional data. We start by loading up the dataset into a pandas dataframe.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import warnings
warnings.filterwarnings('ignore')

df = pd.read_excel(r"C:\Users\chukw\PycharmProjects\Anomaly-dectection-mini-project\Sample - Superstore.xls")
df.info()

# We don't have any major missing values in our dataset and we can now look at a sample subset of the data
print(df.head())

# Visualize Sales vs. Order Date
# Let's look more closely at the Sales attribute of the dataset in the next few cells.
# We'll start by looking at typical sales over time

fig, ax = plt.subplots(1, 1, figsize=(12, 6))
sns.lineplot(x=df['Order Date'], y=df['Sales'])
plt.show()

# Visualize Sales Distribution
# Let's now look at the data distribution for Sales

sns.distplot(df['Sales'])
plt.title("Sales Distribution");
plt.show()

df['Sales'].describe()

sns.distplot(df['Sales'])
plt.title("Sales Distribution");
print(df['Sales'].describe())

# We can definitely see the presence of potential outliers in terms of the min or max values as compared to the meat of the distribution in the interquartile range as observed in the distribution statistics
# Q 2.1: Visualize Profit vs. Order Date
#
# Let's now look closely at the Profit attribute of the dataset in the next few cells. We'll start by looking at typical profits over time.

# Your turn: Plot Order Date vs. Profit using a line plot

fig, ax = plt.subplots(1, 1, figsize=(12, 6))
sns.lineplot(x=df['Order Date'], y=df['Profit'])
plt.show()

# Q 2.2: Visualize Profit Distribution
# Let's now look at the data distribution for Profit
# Your turn: Plot the distribution for Profit
sns.distplot(df['Profit'])
plt.title("Profit Distribution")
plt.show()

# Your turn: Get the essential descriptive statistics for Profit using an appropriate function
print(df["Profit"].describe())

# Your turn: Do you notice anything interesting about the distribution?
"""I noticed the distribution has almost a perfet skewdness because the mean, mode and median are equal to zero"""
# We have both positive and negative values in profits since it indicates either a profit or a loss based on the sales and original price of the items.

# Visualize Discount vs. Profit

sns.scatterplot(x="Discount", y="Profit", data=df)
plt.show()

# In the above visual, we look at a scatter plot showing the distribution of profits w.r.t discounts given

"""
3. Univariate Anomaly Detection

Univariate is basically analysis done on a single attribute or feature. In this section, we will perform anomaly detection on a single attribute using the following methods.

    Statistical Process Control Methods (mean + 3sigma thresholding)
    Isolation Forest

We will start off by demonstrating both these techniques on the Sales attribute and later on, you will implement similar techniques on the Profit attribute.
3.1: Univariate Anomaly Detection on Sales using Statistical Modeling

Here we start off by implementing anomaly detecting using statistical modeling on the Sales attribute
"""

# Obtain Upper Limit Threshold for Sales
# Here we are concerned about transactions with high sales values so we compute the upper limit using the
# + 3 rule where is the mean of the distribution and
# is the standard deviation of the distribution.

mean_sales = df['Sales'].mean()
sigma_sales = df['Sales'].std()
three_sigma_sales = 3*sigma_sales

threshold_sales_value = mean_sales + three_sigma_sales
print('Threshold Sales:', threshold_sales_value)

# Visualize Outlier Region
fig, ax = plt.subplots(1, 1, figsize=(12, 6))

sns.distplot(df['Sales'])
plt.axvspan(threshold_sales_value, df['Sales'].max(), facecolor='r', alpha=0.3)
plt.title("Sales Distribution with Outlier Region");


# Filter and Sort Outliers
# Here we filter out the outlier observations and sort by descending order and view the top 5 outlier values

sales_outliers_df = df['Sales'][df['Sales'] > threshold_sales_value]
print('Total Sales Outliers:', len(sales_outliers_df))
sales_outliers_sorted = sales_outliers_df.sort_values(ascending=False)
sales_outliers_sorted.head(5)


sales_outliers_df = df['Sales'][df['Sales'] > threshold_sales_value]
print('Total Sales Outliers:', len(sales_outliers_df))
sales_outliers_sorted = sales_outliers_df.sort_values(ascending=False)
sales_outliers_sorted.head(5)

# View Top 10 Outlier Transactions

(df.loc[sales_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).head(10)
# View Bottom 10 Outlier Transactions

(df.loc[sales_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)


mean_profit = df["Profit"].mean()
sigma_profit = df["Profit"].std()
three_sigma_profit = 3*sigma_profit

threshold_profit_upper_limit = mean_sales + three_sigma_sales
threshold_profit_upper_limit = threshold_profit_upper_limit.max()
threshold_profit_lower_limit = mean_sales + three_sigma_sales
threshold_profit_lower_limit = threshold_profit_lower_limit.min()

threshold_profit_value = mean_profit + three_sigma_sales
print('Threshold Sales:', threshold_profit_value)


print('Thresholds Profit:', threshold_profit_lower_limit, threshold_profit_upper_limit)

# Visualize Outlier Regions
# Your turn: Visualize the upper and lower outlier regions in the distribution similar to what you did in 3.1
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
sns.distplot(df['Profit'])
plt.axvspan( threshold_profit_lower_limit, df['Profit'].max(), facecolor='r', alpha=0.3)
plt.title("Upper Profit Distribution with Outlier Region")

fig, ax = plt.subplots(1, 1, figsize=(12, 6))
sns.distplot(df['Profit'])
plt.axvspan( threshold_profit_lower_limit, df['Profit'].min(), facecolor='r', alpha=0.3)
plt.title("Lower Profit Distribution with Outlier Region")


# Filter and Sort Outliers
#
# Here we filter out the outlier observations and sort by descending order and view the top 5 outlier values

profit_outliers_df = df['Profit'][df['Profit'] > threshold_profit_value]
print('Total Sales Outliers:', len(profit_outliers_df))
profit_outliers_sorted = profit_outliers_df.sort_values(ascending=False)
print(profit_outliers_sorted.head(5))


# View Top 10 Outlier Transactions
# Your turn: View the top ten transactions based on highest profits
print((df.loc[profit_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).head(10))


# Q: Do you notice any interesting insights based on these transactions?

# A: Most of these are purchases for Copiers and Binders , looks like Canon products yielded some good profits`
# View Bottom 10 Outlier Transactions

# Your turn: View the bottom ten transactions based on lowest profits (highest losses)

print((df.loc[profit_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10))
"""
Q: Do you notice any interesting insights based on these transactions?

A: Most of these are purchases for Machines and Binders , looks like Cibify 3D Printers yielded high losses
3.3: Univariate Anomaly Detection on Sales using Isolation Forest

You might have already learnt about this model from the curriculum. Just to briefly recap, the Isolation Forest model, 'isolates' observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.

Recursive partitioning can be represented by a tree structure. Hence, the number of splittings required to isolate a sample is equivalent to the path length from the root node to the terminating node. This path length, averaged over a forest of such random trees, is a measure of normality and our decision function.

Random partitioning produces noticeably shorter paths for anomalies. Hence, when a forest of random trees collectively produce shorter path lengths for particular samples, they are highly likely to be anomalies.

More details are available in this User Guide"""

# Initialize and Train Model
# Here we initialize the isolation forest model with some hyperparameters assuming the proportion of outliers to be 1% of the total data (using the contamination setting)

from sklearn.ensemble import IsolationForest

sales_ifmodel = IsolationForest(n_estimators=100,
                                contamination=0.01)
sales_ifmodel.fit(df[['Sales']])


# Visualize Outlier Region
#
# Here we visualize the outlier region in the data distribution

xx = np.linspace(df['Sales'].min(), df['Sales'].max(), len(df)).reshape(-1,1)
anomaly_score = sales_ifmodel.decision_function(xx)
outlier = sales_ifmodel.predict(xx)
plt.figure(figsize=(12, 6))
plt.plot(xx, anomaly_score, label='anomaly score')
plt.fill_between(xx.T[0], np.min(anomaly_score), np.max(anomaly_score),
                 where=outlier==-1, color='r',
                 alpha=.4, label='outlier region')
plt.legend()
plt.ylabel('anomaly score')
plt.xlabel('Sales');

# Filter and Sort Outliers
# Here we predict outliers in our dataset using our trained model and filter out the outlier observations and sort by descending order and view the top 5 outlier values

outlier_predictions = sales_ifmodel.predict(df[['Sales']])

sales_outliers_df = df[['Sales']]
sales_outliers_df['Outlier'] = outlier_predictions
sales_outliers_df = sales_outliers_df[sales_outliers_df['Outlier'] == -1]['Sales']

print('Total Sales Outliers:', len(sales_outliers_df))
sales_outliers_sorted = sales_outliers_df.sort_values(ascending=False)
sales_outliers_sorted.head(5)



(df.loc[sales_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).head(10)

# View Bottom 10 Outlier Transactions

(df.loc[sales_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)

"""
Q 3.4: Univariate Anomaly Detection on Profit using Isolation Forest

In this section you will use the learning from Section 3.3 and implement anomaly detecting using isolation on the Profit attribute. Since we have both +ve (profits) and -ve (losses) values in the distribution, we will try to find anomalies for each.
Initialize and Train Model

Your Turn: Initialize the isolation forest model with similar hyperparameters as Section 3.3 and also assuming the proportion of outliers to be 1% of the total data (using the contamination setting)
"""


from sklearn.ensemble import IsolationForest

sales_ifmodel = IsolationForest(n_estimators=100,
                                contamination=0.01)
sales_ifmodel.fit(df[['Sales']])


# Visualize Outlier Region
# Here we visualize the outlier region in the data distribution

xx = np.linspace(df['Sales'].min(), df['Sales'].max(), len(df)).reshape(-1,1)
anomaly_score = sales_ifmodel.decision_function(xx)
outlier = sales_ifmodel.predict(xx)
plt.figure(figsize=(12, 6))
plt.plot(xx, anomaly_score, label='anomaly score')
plt.fill_between(xx.T[0], np.min(anomaly_score), np.max(anomaly_score),
                 where=outlier==-1, color='r',
                 alpha=.4, label='outlier region')
plt.legend()
plt.ylabel('anomaly score')
plt.xlabel('Sales');

# Filter and Sort Outliers
# Here we predict outliers in our dataset using our trained model and filter out the outlier observations and sort by descending order and view the top 5 outlier values
outlier_predictions = sales_ifmodel.predict(df[['Sales']])

sales_outliers_df = df[['Sales']]
sales_outliers_df['Outlier'] = outlier_predictions
sales_outliers_df = sales_outliers_df[sales_outliers_df['Outlier'] == -1]['Sales']

print('Total Sales Outliers:', len(sales_outliers_df))
sales_outliers_sorted = sales_outliers_df.sort_values(ascending=False)
sales_outliers_sorted.head(5)

# View Top 10 Outlier Transactions
(df.loc[sales_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).head(10)
# View Bottom 10 Outlier Transactions
(df.loc[sales_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)

"""
Q 3.4: Univariate Anomaly Detection on Profit using Isolation Forest

In this section you will use the learning from Section 3.3 and implement anomaly detecting using isolation on the Profit attribute. Since we have both +ve (profits) and -ve (losses) values in the distribution, we will try to find anomalies for each.
Initialize and Train Model

Your Turn: Initialize the isolation forest model with similar hyperparameters as Section 3.3 and also assuming the proportion of outliers to be 1% of the total data (using the contamination setting)
"""

sales_ifmodel = IsolationForest(n_estimators=100,
                                contamination=0.01)
sales_ifmodel.fit(df[['Profit']])
# Here we visualize the outlier region in the data distribution

xx = np.linspace(df['Profit'].min(), df['Profit'].max(), len(df)).reshape(-1,1)
anomaly_score = sales_ifmodel.decision_function(xx)
outlier = sales_ifmodel.predict(xx)
plt.figure(figsize=(12, 6))
plt.plot(xx, anomaly_score, label='anomaly score')
plt.fill_between(xx.T[0], np.min(anomaly_score), np.max(anomaly_score),
                 where=outlier==-1, color='r',
                 alpha=.4, label='outlier region')
plt.legend()
plt.ylabel('anomaly score')
plt.xlabel('Profit')
plt.show()

# Filter and Sort Outliers

# Your Turn: Predict outliers in our dataset using our trained model and filter out the outlier observations and sort by descending order and view the top 5 outlier values similar to 3.3
outlier_predictions = sales_ifmodel.predict(df[['Sales']])

profit_outliers_df = df[['Profit']]
profit_outliers_df['Outlier'] = outlier_predictions
profit_outliers_df = sales_outliers_df[sales_outliers_df['Outlier'] == -1]['Profit']

print('Total Profit Outliers:', len(profit_outliers_df))
profit_outliers_sorted = sales_outliers_df.sort_values(ascending=False)
profit_outliers_sorted.head(5)


# View Top 10 Outlier Transactions
#
# Your turn: View the top ten transactions based on highest profits
(df.loc[profit_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).head(10)
# View Bottom 10 Outlier Transactions
# Your turn: View the bottom ten transactions based on lowest profits (highest losses)
(df.loc[profit_outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)

# Q: Do you observe any similarity in the results with the previous method?
# A: Yes

"""
4. Multivariate Anomaly Detection

Multivariate is basically analysis done on more than one attribute or feature at a time. In this section, we will perform anomaly detection on two attributes (Discount & Profit) using the following methods.

    Clustering Based Local Outlier Factor (CBLOF)
    Isolation Forest
    Auto-Encoders

You will learn how to train these models to detect outliers and also visualize these outliers. For this section we will be using the pyod package so make sure you have it installed.
"""
# Extract Subset Data for Outlier Detection
cols = ['Discount', 'Profit']
subset_df = df[cols]
subset_df.head()

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler(feature_range=(0, 1))
subset_df[cols] = mms.fit_transform(subset_df)
subset_df.head()

"""
4.1: Multivariate Anomaly Detection with Clustering Based Local Outlier Factor (CBLOF)

The CBLOF model takes as an input the dataset and the cluster model that was generated by a clustering algorithm. It classifies the clusters into small clusters and large clusters using the parameters alpha and beta. The anomaly score is then calculated based on the size of the cluster the point belongs to as well as the distance to the nearest large cluster.

By default, kMeans is used for clustering algorithm. You can read more in the official documentation
Initialize and Train Model

Here we initialize the CBLOF model with some hyperparameters assuming the proportion of outliers to be 1% of the total data (using the contamination setting)
"""
from pyod.models import cblof

cblof_model = cblof.CBLOF(contamination=0.01, random_state=42)
cblof_model.fit(subset_df)


# Filter and Sort Outliers
# Here we predict outliers in our dataset using our trained model and filter out the outlier observations and sort by descending order and view the top 5 outlier values

outlier_predictions = cblof_model.predict(subset_df)

outliers_df = subset_df.copy(deep=True)
outliers_df['Outlier'] = outlier_predictions
outliers_df = outliers_df[outliers_df['Outlier'] == 1]

print('Total Outliers:', len(outliers_df))
outliers_sorted = outliers_df.sort_values(by=['Profit', 'Discount'], ascending=False)
outliers_sorted.head(5)

# View Bottom 10 Outlier Transactions

(df.loc[outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)

"""
We can definitely see some huge losses incurred based on giving higher discounts even if the sales amount was high which is interesting as well as concerning.
Q 4.2: Multivariate Anomaly Detection with Isolation Forest

Here you will detect anomalies using the Isolation Forest model and use the learnings from 4.1. Here you will use the pyod version of Isolation Forest which is basically a wrapper over the scikit-learn version but with more functionalities.
Initialize and Train Model

Your Turn: Initialize the isolation forest model with similar hyperparameters as before and also assuming the proportion of outliers to be 1% of the total data (using the contamination setting)
"""

from pyod.models import iforest

if_model = IsolationForest(n_estimators=100,
                                contamination=0.01)

"""
Filter and Sort Outliers
Your Turn: Predict outliers in our dataset using our trained model and filter out the outlier observations and sort by descending order and view the top 5 outlier values similar to 4.1
"""

outlier_predictions = if_model.predict(subset_df)

outliers_df = subset_df.copy(deep=True)
outliers_df['Outlier'] = outlier_predictions
outliers_df = outliers_df[outliers_df['Outlier'] == 1]

print('Total Outliers:', len(outliers_df))
outliers_sorted = outliers_df.sort_values(by=['Profit', 'Discount'], ascending=False)
outliers_sorted.head(5)

# View Bottom 10 Outlier Transactions
(df.loc[outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)

# Q: Do you notice any differences in the results with the previous model?
#
# We do notice some transactions with 80% discount and high losses
# Q 4.3: Multivariate Anomaly Detection with Auto-encoders
#
# Here you will detect anomalies using the Auto-encoder model and use the learnings from 4.1. Here you will use the Auto-encoder model from pyod which is a deep learning model often used for
# learning useful data representations in an unsupervised fashion without any labeled data.
#
# Similar to PCA, AE could be used to detect outlier objects in the data by calculating the reconstruction errors
# Initialize Model
#
# Here we initiaze an auto-encoder network with a few hidden layers so that we could train it for a 100 epochs

from pyod.models import auto_encoder

ae_model = auto_encoder.AutoEncoder(hidden_neurons=[2, 32, 32, 2],
                                    hidden_activation='relu',
                                    output_activation='sigmoid',
                                    epochs=100,
                                    batch_size=32,
                                    contamination=0.01)

ae_model = auto_encoder.AutoEncoder(hidden_neurons=[2, 32, 32, 2],
                                    hidden_activation='relu',
                                    output_activation='sigmoid',
                                    epochs=100,
                                    batch_size=32,
                                    contamination=0.01)

# Train Model
# Your turn: Train the model by calling the fit() function on the right data
ae_model.fit(subset_df)

# Filter and Sort Outliers
# Your Turn: Predict outliers in our dataset using our trained model and filter out the outlier observations and sort by descending order and view the top 5 outlier values similar to 4.1
outlier_predictions = ae_model.predict(subset_df)

outliers_df = subset_df.copy(deep=True)
outliers_df['Outlier'] = outlier_predictions
outliers_df = outliers_df[outliers_df['Outlier'] == 1]

print('Total Outliers:', len(outliers_df))
outliers_sorted = outliers_df.sort_values(by=['Profit', 'Discount'], ascending=False)
outliers_sorted.head(5)

# View Bottom 10 Outlier Transactions
# Your turn: View the bottom ten transactions
(df.loc[outliers_sorted.index.tolist()][['City', 'Category', 'Sub-Category', 'Product Name',
                                              'Sales', 'Quantity', 'Discount', 'Profit']]).tail(10)


# 4.4: Visualize Anomalies and Compare Anomaly Detection Models
#
# Here we will look at the visual plots of anomalies as detected by the above three models

def visualize_anomalies(model, xx, yy, data_df, ax_obj, subplot_title):
    # predict raw anomaly score
    scores_pred = model.decision_function(data_df) * -1
    # prediction of a datapoint category outlier or inlier
    y_pred = model.predict(data_df)
    n_inliers = len(y_pred) - np.count_nonzero(y_pred)
    n_outliers = np.count_nonzero(y_pred == 1)

    out_df = data_df.copy(deep=True)
    out_df['Outlier'] = y_pred.tolist()
    # discount - inlier feature 1,  profit - inlier feature 2
    inliers_discount = out_df[out_df['Outlier'] == 0]['Discount'].values
    inliers_profit = out_df[out_df['Outlier'] == 0]['Profit'].values
    # discount - outlier feature 1, profit - outlier feature 2
    outliers_discount = out_df[out_df['Outlier'] == 1]['Discount'].values
    outliers_profit = out_df[out_df['Outlier'] == 1]['Profit'].values

    # Use threshold value to consider a datapoint inlier or outlier
    # threshold = stats.scoreatpercentile(scores_pred,100 * outliers_fraction)
    threshold = np.percentile(scores_pred, 100 * outliers_fraction)
    # decision function calculates the raw anomaly score for every point
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()]) * -1
    Z = Z.reshape(xx.shape)
    # fill blue map colormap from minimum anomaly score to threshold value
    ax_obj.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7), cmap=plt.cm.Blues_r)
    # draw red contour line where anomaly score is equal to thresold
    a = ax_obj.contour(xx, yy, Z, levels=[threshold], linewidths=2, colors='red')
    # fill orange contour lines where range of anomaly score is from threshold to maximum anomaly score
    ax_obj.contourf(xx, yy, Z, levels=[threshold, Z.max()], colors='orange')
    b = ax_obj.scatter(inliers_discount, inliers_profit, c='white', s=20, edgecolor='k')
    c = ax_obj.scatter(outliers_discount, outliers_profit, c='black', s=20, edgecolor='k')

    ax_obj.legend([a.collections[0], b, c], ['learned decision function', 'inliers', 'outliers'],
                  prop=matplotlib.font_manager.FontProperties(size=10), loc='upper right')

    ax_obj.set_xlim((0, 1))
    ax_obj.set_ylim((0, 1))
    ax_obj.set_xlabel('Discount')
    ax_obj.set_ylabel('Sales')
    ax_obj.set_title(subplot_title)


outliers_fraction = 0.01
xx, yy = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
fig, ax = plt.subplots(1, 3, figsize=(20, 6))

ax_objs = [ax[0], ax[1], ax[2]]
models = [cblof_model, if_model, ae_model]
plot_titles = ['Cluster-based Local Outlier Factor (CBLOF)',
               'Isolation Forest',
               'Auto-Encoder']

for ax_obj, model, plot_title in zip(ax_objs, models, plot_titles):
    visualize_anomalies(model=model,
                        xx=xx, yy=yy,
                        data_df=subset_df,
                        ax_obj=ax_obj,
                        subplot_title=plot_title)
plt.axis('tight')

