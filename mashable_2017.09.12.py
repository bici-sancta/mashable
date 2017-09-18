
# coding: utf-8

# ## Business Understanding (10 points total).  
# 
# • Describe the purpose of the data set you selected (i.e., why was this data collected in
# the first place?). Describe how you would define and measure the outcomes from the
# dataset. That is, why is this data important and how do you know if you have mined
# useful knowledge from the dataset? How would you measure the effectiveness of a
# good prediction algorithm? Be specific.
# 
# This dataset was 
# Abstract: This dataset summarizes a heterogeneous set of features about articles published by Mashable in a period of two years. The goal is to predict the number of shares in social networks (popularity).
# 	
# 
# ***  
# Citation Request:
# ***  
# K. Fernandes, P. Vinagre and P. Cortez. A Proactive Intelligent Decision Support System for Predicting the Popularity of Online News. Proceedings of the 17th EPIA 2015 - Portuguese Conference on Artificial Intelligence, September, Coimbra, Portugal.
# ***  
# 

# ## Data Understanding (80 points total)  
# 
# ### Group 1
# • [10 points] Describe the meaning and type of data (scale, values, etc.) for each
# attribute in the data file.  
# 
# • [15 points] Verify data quality: Explain any missing values, duplicate data, and outliers.
# Are those mistakes? How do you deal with these problems? Be specific.  
# 
# • [10 points] Give simple, appropriate statistics (range, mode, mean, median, variance,
# counts, etc.) for the most important attributes and describe what they mean or if you
# found something interesting. Note: You can also use data from other sources for
# comparison. Explain the significance of the statistics run and why they are meaningful.  
# 
# ### Group 2
# • [15 points] Visualize the most important attributes appropriately (at least 5 attributes).
# Important: Provide an interpretation for each chart. Explain for each attribute why the
# chosen visualization is appropriate.  
# 
# ### Group 3
# • [15 points] Explore relationships between attributes: Look at the attributes via scatter
# plots, correlation, cross-tabulation, group-wise averages, etc. as appropriate. Explain
# any interesting relationships.  
# 
# ### Group 4
# • [10 points] Identify and explain interesting relationships between features and the class
# you are trying to predict (i.e., relationships with variables and the target classification).  
# 
# • [5 points] Are there other features that could be added to the data or created from
# existing features?  Which ones?  
# 
# ### Group - All
# Exceptional Work (10 points total)  
# • You have free reign to provide additional analyses.  
# • One idea: implement dimensionality reduction, then visualize and interpret the results.  
# 
# 

# In[135]:


# ... https://stackoverflow.com/questions/36786722/how-to-display-full-output-in-jupyter-not-only-last-result
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import pandas as pd
import numpy as np

del df1
df1 = pd.read_csv("../mashable/data/OnlineNewsPopularity.csv")

df1.columns = df1.columns.str.strip()
col_names = df1.columns.values.tolist()

df1.describe().T        

#df1.corr()


# #### Create categorical feature of day_of_week from the 7 booleans

# In[136]:



df1['day_of_week'] = 'Mon'

tuesday = df1['weekday_is_tuesday'] == 1
df1.loc[tuesday, 'day_of_week'] = 'Tue'

wednesday = df1['weekday_is_wednesday'] == 1
df1.loc[wednesday, 'day_of_week'] = 'Wed'

thursday = df1['weekday_is_thursday'] == 1
df1.loc[thursday, 'day_of_week'] = 'Thu'

friday = df1['weekday_is_friday'] == 1
df1.loc[friday, 'day_of_week'] = 'Fri'

saturday = df1['weekday_is_saturday'] == 1
df1.loc[saturday, 'day_of_week'] = 'Sat'

sunday = df1['weekday_is_sunday'] == 1
df1.loc[sunday, 'day_of_week'] = 'Sun'

list(df1)

df1.ix[:,31:].head(20)

df1.drop('weekday_is_monday', axis=1, inplace=True)
df1.drop('weekday_is_tuesday', axis=1, inplace=True)
df1.drop('weekday_is_wednesday', axis=1, inplace=True)
df1.drop('weekday_is_thursday', axis=1, inplace=True)
df1.drop('weekday_is_friday', axis=1, inplace=True)
df1.drop('weekday_is_saturday', axis=1, inplace=True)
df1.drop('weekday_is_sunday', axis=1, inplace=True)

df1.describe().T


# #### Create categorical feature of data_channel from the 7 booleans

# In[137]:



df1['data_channel'] = 'Lifestyle'

condition = df1['data_channel_is_entertainment'] == 1
df1.loc[condition, 'data_channel'] = 'Entertainment'

condition = df1['data_channel_is_bus'] == 1
df1.loc[condition, 'data_channel'] = 'Business'

condition = df1['data_channel_is_socmed'] == 1
df1.loc[condition, 'data_channel'] = 'SocMed'

condition = df1['data_channel_is_tech'] == 1
df1.loc[condition, 'data_channel'] = 'Tech'

condition = df1['data_channel_is_world'] == 1
df1.loc[condition, 'data_channel'] = 'World'

df1.drop('data_channel_is_lifestyle', axis=1, inplace=True)
df1.drop('data_channel_is_entertainment', axis=1, inplace=True)
df1.drop('data_channel_is_bus', axis=1, inplace=True)
df1.drop('data_channel_is_socmed', axis=1, inplace=True)
df1.drop('data_channel_is_tech', axis=1, inplace=True)
df1.drop('data_channel_is_world', axis=1, inplace=True)

df1.describe().T


# #### create some transformed variables

# In[138]:


import numpy as np
import datetime as dt


# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... parse url into useable elements, using str.split
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

df1['http'], df1['blank'], df1['mash'], df1['year'],             df1['month'], df1['day'], df1['title'], df1['extra']         = df1['url'].str.split("\/", 7).str
    
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... drop the intermediary unnecessary columns
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

df1.drop('http',  axis=1, inplace=True)
df1.drop('blank', axis=1, inplace=True)
df1.drop('mash',  axis=1, inplace=True)
df1.drop('extra', axis=1, inplace=True)

# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... add date column from year-month-day fields
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

df1['year']  = (df1['year']).astype(str)
df1['month'] = (df1['month']).astype(str)
df1['day']   = (df1['day']).astype(str)
df1.publish_date = pd.to_datetime(df1.year + df1.month + df1.day, format = "%Y%m%d")

df1.describe().T


# In[140]:


# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... log transform on variables with high skewness
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

drop_list = []

# ... https://stackoverflow.com/questions/25039626/find-numeric-columns-in-pandas-python
df_numeric = df1.select_dtypes(exclude = ['object'])
df_numeric.describe().T

# ... store min value for each column ... reference for ln() applicability

df_mins = df_numeric.min()

# ... number of columns in current data frame

col_names = df_numeric.columns.values.tolist()
n_cols = len(df_numeric.columns)
print(n_cols)

# ... loop on each column ... 
# ... -- if skewness > 1 --> 
# ...     -- ln() transform
# ...     -- create new column name as 'ln_' + original column name
# ...     -- if min value = 0 --> add 1 to column prior to transform
# ...     -- if min value < 0 --> do not transform ... look for other solution
# ...     -- drop original column if ln() transform created

for i_col in range(n_cols-1):
    indx = i_col + 1
    print(col_names[indx], df_numeric.iloc[:, indx].dtypes)
    sk = df_numeric.iloc[:, indx].skew()
    if(sk > 1):
        new_col_name = 'ln_' + col_names[indx]
        print (col_names[indx], i_col, indx, sk, new_col_name)
        if df_mins[indx] > 0:
            df_numeric[new_col_name] = np.log(df_numeric.iloc[:, indx])
            drop_list.append(col_names[indx])
        elif df_mins[indx] == 0:
            df_tmp = df_numeric.iloc[:, indx] + 1
            df_numeric[new_col_name] = np.log(df_tmp)
            drop_list.append(col_names[indx])
        else:
            print('--> Log transform not completed :', col_names[indx], '!!')

# ...  drop original column if ln() transform created

print(*drop_list, sep = "\n")
df_numeric.drop(drop_list, axis=1, inplace=True)
df_numeric.describe().T


# ### First round of plots
# 
# - scatter plot of each numerical feature (date ordered)
# - histogram of each feature

# In[143]:



get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot as plt
import seaborn as sb
sb.set()

# ... scatter plots

df_numeric.columns = df_numeric.columns.str.strip()
col_names = df_numeric.columns.values.tolist()

n_cols = len(df1.columns)

fig = plt.figure(figsize = (18, 16), dpi = 80, facecolor = 'w', edgecolor = 'k')

for i_col in range(n_cols-1):
    indx = i_col + 1
    plt.plot(df_numeric.timedelta, df_numeric.iloc[:, indx], label = col_names[indx], linestyle = 'None', marker = 'o')
    plt.xlabel('time delta')
    plt.ylabel(col_names[indx])
    plt.title('mashable characteristics')
    plt.legend()
    plt.show()

#sb.tsplot(x = 'publish_date', y = 'kw_max_avg', data = df1,
#          fit_reg = False)



# #### Things to do ... based on 1st sets of data plots  
# 
# ***  
# 
# - delete columns of boolean values (e.g., is_monday, ...)  
# - drop columns that were converted of ln scale  
# - remove outliers of following columns :  
#     - average_token_length - remove 0 values  ...
#     
#     
#     - add list of rest of columns and any action to take ...
# 

# In[11]:





# In[74]:


sb.stripplot(x = 'data_channel',
             y = 'ln_shares',
             data = df1,
             jitter = True)

sb.stripplot(x = 'day_of_week',
             y = 'ln_shares',
             data = df1,
             jitter = True)

# horizontal boxes
#plt.boxplot(df1['day_of_week'])


# In[148]:




df_corr = pd.DataFrame(df_numeric.corr())

filename = 'correlation_matrix.csv'
df_corr.to_csv(filename, index = True)

# ... https://stackoverflow.com/questions/34896455/how-to-do-pearson-correlation-of-selected-columns-of-a-pandas-data-frame
corr_2_ln_shares = pd.DataFrame(df_numeric[df_numeric.columns[1:]].corr()['ln_shares'][:-1])

corr_2_ln_shares['abs'] = corr_2_ln_shares.ln_shares.abs()

print(corr_2_ln_shares.sort('abs', ascending = False))

cols_2_keep = corr_2_ln_shares.sort('abs', ascending = False).index

print(*cols_2_keep, sep = "\n")

cols_2_keep = cols_2_keep[:25]

print(*cols_2_keep, sep = "\n")


# In[153]:



# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... keep only Top25 numeric columns based on correlcation w/ ln_shares
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

df2 = df_numeric[cols_2_keep]

# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... add back column with ln_shares
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

df2 = pd.concat([df2, df_numeric.ln_shares], axis=1)

# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ... add back columns with categorical features
# ... -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

df2 = pd.concat([df2, df1.day_of_week], axis=1)
df2 = pd.concat([df2, df1.data_channel], axis=1)
df2 = pd.concat([df2, df1.publish_date], axis=1)
df2.describe().T

filename = 'selected_columns.csv'
df2.to_csv(filename, index = True)

