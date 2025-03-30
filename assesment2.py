import pandas as pd
from collections import defaultdict,Counter
from itertools import tee, pairwise
df=pd.read_csv("./dataset2.csv")



#  **1. Advanced Data Cleaning (Pandas)**  
# - Handle duplicate rows (keep first valid entry)  
cleaned_df = df.drop_duplicates(subset=["OrderID","CustomerID"],keep="first")

# - Fix Product typos (map variations to canonical names: ProdA/Product A → "Product A") 
unique_products = cleaned_df['Product'].unique() #Checking what are the different names
product_name_map={
    "Item C":"Product C",
    "Prod B":"Product B",
    "ProdA":"Product A"
}
cleaned_df["Product"] = cleaned_df["Product"].replace(product_name_map)

# print("New Unique", cleaned_df['Product'].unique())

# - Validate numericals:  

#   - Replace negative Quantity with 1  
# print(cleaned_df)
cleaned_df.loc[cleaned_df['Quantity'] < 0, 'Quantity'] = 1 # changing less than 0 to 1
negative_values = cleaned_df[cleaned_df['Quantity'] < 0]['Quantity']    
print("here",negative_values) #it is empty so all cleaned


#   - Drop rows with negative Price 
cleaned_df = cleaned_df[cleaned_df['Price']>=0]
print("With Negative Price",cleaned_df[cleaned_df['Price'] < 0]) #Empty so is negative


# - Fix Category inconsistencies (all electronics-related typos → "Electronics")  
unique_category = cleaned_df['Category'].unique() #Checking what are the different category
print("Unique category", unique_category)
cleaned_df['Category']=cleaned_df['Category'].replace(
    {
        "Eletronics":"Electronics",
        "Electronic":"Electronics", 
    }
)
# As there is nan value, i will replace that as well
cleaned_df['Category']= cleaned_df['Category'].fillna('Unknown')
unique_category = cleaned_df['Category'].unique() #Checking what are the different category
print("New Unique category", unique_category)

# - Impute missing Regions using CustomerID's most common region  
most_common_region = cleaned_df.groupby('CustomerID')['Region'].agg(lambda x: x.mode()[0]) #most frequent value

# Find the most common region for each CustomerID
cleaned_df['Region'] = cleaned_df['Region'].fillna(cleaned_df['CustomerID'].map(most_common_region))

# - Create `IsPromo` flag from PromoCode  
cleaned_df['IsPromo'] = cleaned_df['PromoCode'].notna().astype(int) #flag will be set to 1 if there is a valid PromoCode, and 0 if the PromoCode is missing or empty.
print(cleaned_df.head())
# **2. Complex DateTime Operations**  
# - Convert all dates to UTC datetime 
# Convert OrderDate column to datetime
cleaned_df['OrderDate'] = pd.to_datetime(cleaned_df['OrderDate'], errors='coerce')
# Convert to UTC timezone
cleaned_df['OrderDate'] = cleaned_df['OrderDate'].dt.tz_localize('UTC', ambiguous='NaT', nonexistent='NaT')

# - Calculate order processing time (assume returns happen 7 days after order)  
# Converting OrderDate to datetime format
cleaned_df['OrderDate'] = pd.to_datetime(cleaned_df['OrderDate'], errors='coerce')
# Calculate the Return Date (7 days after OrderDate)
cleaned_df['ReturnDate'] = cleaned_df['OrderDate'] + pd.Timedelta(days=7)
# Calculating Processing Time 
cleaned_df['ProcessingTime'] = (cleaned_df['ReturnDate'] - cleaned_df['OrderDate']).dt.days
# Display the result
print("Results")
print(cleaned_df[['OrderDate', 'ReturnDate', 'ProcessingTime']])


# - Find weekly sales trends for electronics vs home goods  
# Filtering Electronics and Home goods
filtered_df = cleaned_df[cleaned_df['Category'].isin(['Electronics', 'Home'])]
#Calculating Sales
filtered_df['Sales'] = filtered_df['Quantity'] * filtered_df['Price']
# Set 'OrderDate' to the start of the week (weekly frequency)
filtered_df['Week'] = filtered_df['OrderDate'].dt.to_period('W').dt.start_time
#Group by 'Week' and 'Category', and calculating total sales per week
weekly_sales = filtered_df.groupby(['Week', 'Category'])['Sales'].sum().reset_index()
print("Weekly Results")
print(weekly_sales)

# - Identify customers with >2 orders in any 14-day window  
print(cleaned_df)

  


# ----needs to be done ---

# **3. Advanced Collections & Optimization**  

# Build nested dictionary: `{CustomerID: {"total_spent": X, "favorite_category": Y}}`  
cleaned_df['TotalSpent'] = cleaned_df['Price'] * cleaned_df['Quantity']

# Group by 'CustomerID' to calculate the total spent and favorite category
customer_summary = cleaned_df.groupby('CustomerID').agg(
    total_spent=('TotalSpent', 'sum'),
    favorite_category=('Category', lambda x: x.mode()[0])  # Mode returns the most frequent category
).reset_index()

#nested dictionary
customer_dict = customer_summary.set_index('CustomerID').to_dict(orient='index')
print(customer_dict)
# - Use `defaultdict` to track return rates by region: `{"North": 0.25, ...}`  
# to store return rates
return_rates = defaultdict(float)
# Step 2: Group by 'Region' and calculate return rates
region_groups = cleaned_df.groupby('Region')

for region, group in region_groups:
    # Calculate return rate as the mean of the 'ReturnFlag' column
    return_rate = group['ReturnFlag'].mean()
    return_rates[region] = return_rate
# Print the return rates by region
print("Return rates by region",dict(return_rates))
# - Find most common promo code sequence using `itertools` and `Counter`  

# Extract non-null PromoCodes in order
promo_codes = cleaned_df['PromoCode'].dropna().tolist()

# Generate consecutive pairs of promo codes
promo_pairs = list(pairwise(promo_codes))
# Count occurrences of each pair
pair_count = Counter(promo_pairs)
# Find the most common pair
most_common_pair = pair_count.most_common(1)[0]

print("Most common promo code sequence:", most_common_pair)

# - Optimize memory usage by downcasting numerical columns  
# Memory usage before optimization
print("Memory usage before optimization:")
print(cleaned_df.memory_usage(deep=True))

# Downcast numerical columns
for col in cleaned_df.select_dtypes(include=['int', 'float']).columns:
    if cleaned_df[col].dtype == 'float64':
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], downcast='float')
    elif cleaned_df[col].dtype == 'int64':
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], downcast='integer')

# Memory usage after optimization
print("\nMemory usage after optimization:")
print(cleaned_df.memory_usage(deep=True))

# **4. Bonus (If Time Permits)**  

# - Create UDF to flag "suspicious orders" (multiple returns + high value)  
# Define the threshold for a high-value order
high_value_threshold = 400

# UDF To flag suspicious order
def flag_suspicious(row):
    if row['ReturnFlag'] > 1 and row['Price'] > high_value_threshold:
        return 1  # Flag as suspicious
    else:
        return 0  # Not suspicious
# Applying the UDF to the DataFrame
cleaned_df['SuspiciousOrder'] = cleaned_df.apply(flag_suspicious, axis=1)

# Displaying the updated DataFrame with the new column
print(cleaned_df[['OrderID', 'Price', 'ReturnFlag', 'SuspiciousOrder']])
# - Calculate rolling 7-day average sales using efficient windowing  