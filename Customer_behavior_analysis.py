#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv("customer_shopping_behavior.csv")


# In[2]:


df.head(10)


# In[3]:


df.info()


# In[4]:


df.describe()


# In[5]:


df.describe(include="all")


# #checking null values

# In[6]:


df.isnull().sum()


# #renaming columns for better analysis

# In[7]:


df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})


# In[8]:


df.columns


# # creating new columns that will help in analysis

# In[9]:


labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)


# In[10]:


df[['age','age_group']].head(10)


# In[11]:


frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


# In[12]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# In[13]:


df[['discount_applied','promo_code_used']].head(10)


# In[14]:


(df['discount_applied'] == df['promo_code_used']).all()


# In[15]:


df = df.drop('promo_code_used', axis=1)  # Dropping promo code used column


# In[16]:


df.columns


# In[17]:


get_ipython().system('pip install psycopg2-binary sqlalchemy')


# In[18]:


from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"      # default user
password = "admin123" # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "customer_behavior"    # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")


# In[ ]:




