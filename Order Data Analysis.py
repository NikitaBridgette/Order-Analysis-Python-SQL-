#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries
get_ipython().system('pip install kaggle')
import kaggle


# In[3]:


get_ipython().system('kaggle datasets download ankitbansal06/retail-orders -f orders.csv')


# In[4]:


#extract file from zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip') 
zip_ref.extractall() # extract file to dir
zip_ref.close() # close file


# In[5]:


#read data from the file and handle null values
import pandas as pd
df = pd.read_csv('orders.csv')


# In[6]:


#lets view some data
df.head(20)


# In[7]:


#There are some "Not Available","Unknown" values in the "Ship Mode" column, lets check the column to view the other values in the column
df['Ship Mode'].unique()


# In[8]:


#Replacing the "Not Available","Unknown" & "nan" values in the "Ship Mode" Column and reading the data again
df = pd.read_csv('orders.csv',na_values=['Not Available','unknown']) #replaced values
df['Ship Mode'].unique() #checking again


# In[9]:


df.head(5)


# In[12]:


#rename columns names ..make them lower case and replace space with underscore
#df.rename(columns={'Order Id':'order_id', 'City':'city'})
#df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df.head(5)


# In[15]:


#derive new columns discount , sale price and profit
#df['discount']=df['list_price']*df['discount_percent']*.01 #Discount Column
#df['sale_price']= df['list_price']-df['discount'] #SalePrice
df['profit']=df['sale_price']-df['cost_price'] #Profit
df


# In[16]:


df.dtypes
#order_date is object type, we need to change 


# In[17]:


#convert order date from object data type to datetime
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")


# In[18]:


df.head(5)
df.dtypes


# In[19]:


#drop cost price list price and discount percent columns
df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)
df.columns


# In[20]:


#load the data into sql server using replace option
import sqlalchemy as sal


# In[21]:


engine = sal.create_engine('mssql://HP\SQLEXPRESS/master?driver=ODBC+DRIVER+17+FOR+SQL+SERVER')
conn=engine.connect()


# In[27]:


#load the data into sql server using append option
df.to_sql('df_orders', con=conn , index=False, if_exists = 'append')

