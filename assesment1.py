import pandas as pd
from collections import Counter

# Load the dataset
df = pd.read_csv("dataset1.csv")
print(df.head(5))
# 1. Find the category with the highest average rating
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset1.csv")
 

# Question 1 Find the category with the highest average rating
highestAverageRating = df.groupby("Category")["Rating"].mean()
highestAverageCategoryRating = highestAverageRating.idxmax()
print("Highest Average Rating Is ",highestAverageCategoryRating)

# Question 2
# Group by category and calculate the total stock
totalStockByCategory = df.groupby("Category")["Stock"].sum()
print("Total stock available for each category:", totalStockByCategory)


# Question 3
# Create a new column Final_Price where Final_Price = Price - (Price * Discount / 100).
df["Final_Price"] = df["Price"] - (df["Price"] * df["Discount"] / 100)
print(df[["Product_ID", "Price", "Discount", "Final_Price"]])

# Question 4
# Find the top 3 most discounted products.
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset1.csv")

# Question 5 Sort the dataframe by Discount in descending order
sortedDf = df.sort_values(by="Discount", ascending=False)
topDiscountedProducts = sortedDf.head(3)
print("Top 3 most discounted products: ", topDiscountedProducts)



# Supplier Analysis:
# Find the supplier with the highest average price of products.
supplierAvgPrice = df.groupby("Supplier")["Price"].mean()

# Find the supplier with the highest average price
highestAveragePriceSupplier = supplierAvgPrice.idxmax()

print("Supplier with the highest average price of products:", highestAveragePriceSupplier)

# Find the total number of unique suppliers.
uniqueSuppliers = len(pd.unique(df["Supplier"]))
print("These are the unique suppliers", uniqueSuppliers)

# Collections Question

# Using collections.Counter:
# Count occurrences of each category using Counter
categoryCounts = Counter(df["Category"])
print("Category occurrences:", dict(categoryCounts))
  
# Find the most common category.

