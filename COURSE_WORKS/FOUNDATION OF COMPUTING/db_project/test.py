import pandas as pd
import numpy as np

# Given DataFrame
data = {'Name': [np.nan, 'Bob', 'Charlie', 'David', np.nan, 'Ali', 'James', 'Ely', 'Sara', np.nan],
        'Age': [25.0, np.nan, 25.0, 40.0, 28.0, 25.0, np.nan, 25.0, 40.0, 31.0],
        'City': ['New York', 'San Francisco', np.nan, 'Chicago', 'Boston', 'New York', 'San Francisco', 'San Francisco', 'Chicago', 'Boston'],
        'Salary': [60000.0, 80000.0, 75000.0, np.nan, 70000.0, 50000.0, 60000.0, 75000.0, 80000.0, 80000.0]}
df = pd.DataFrame(data)

# 1. Calculate the total salaries per city
total_salaries_per_city = df.groupby('City')['Salary'].sum()
print("Total salaries per city:")
print(total_salaries_per_city)

# 2. Retrieve the average salary per age
average_salary_per_age = df.groupby('Age')['Salary'].mean()
print("\nAverage salary per age:")
print(average_salary_per_age)

# 3. What is the output of
# A. df.loc[df['Age'] > 30, ['Name', 'City']]
print("\nOutput of df.loc[df['Age'] > 30, ['Name', 'City']]:")
print(df.loc[df['Age'] > 30, ['Name', 'City']])

# B. select = df.loc[1:3]
select = df.loc[1:3]
print("\nOutput of select = df.loc[1:3]:")
print(select)

# C. select2 = df.iloc[1:3]
select2 = df.iloc[1:3]
print("\nOutput of select2 = df.iloc[1:3]:")
print(select2)

# D. select3 = df[1:3]
select3 = df[1:3]
print("\nOutput of select3 = df[1:3]:")
print(select3)

# E. type(selected_column = df[1,:])
selected_column = df.iloc[1, :]
print("\nOutput of type(selected_column = df.iloc[1, :]):")
print(type(selected_column))

# F. grouped_age_max_salary = df.groupby('Age')['Salary'].max()
grouped_age_max_salary = df.groupby('Age')['Salary'].max()
print("\nOutput of grouped_age_max_salary = df.groupby('Age')['Salary'].max():")
print(grouped_age_max_salary)

# G. df_dropped_columns_threshold = df.dropna(axis=1, thresh=2)
df_dropped_columns_threshold = df.dropna(axis=1, thresh=2)
print("\nOutput of df_dropped_columns_threshold = df.dropna(axis=1, thresh=2):")
print(df_dropped_columns_threshold)

# H. concat([df1['Age'],df1['Name']])
print("\nOutput of concat([df1['Age'],df1['Name']]):")
print(df[['Name','Age']].dropna())

