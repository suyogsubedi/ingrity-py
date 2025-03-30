Ingrity Python Assesments

Pandas Questions

Category-Based Analysis:
 
Find the category with the highest average rating.
 
Find the total stock available for each category.
 
Discounted Price Calculation:
 
Create a new column Final_Price where Final_Price = Price - (Price * Discount / 100).
 
Find the top 3 most discounted products.
 
Supplier Analysis:
 
Find the supplier with the highest average price of products.
 
Find the total number of unique suppliers.
 
Collections Question

Using collections.Counter:
 
Count the occurrences of each category using collections.Counter.
 
Find the most common category.
 

 --------------------------Assesment 2 Question------------------------------------------

 **1. Advanced Data Cleaning (Pandas)**  
 
- Handle duplicate rows (keep first valid entry)  

- Fix Product typos (map variations to canonical names: ProdA/Product A → "Product A")  

- Validate numericals:  

  - Replace negative Quantity with 1  

  - Drop rows with negative Price  

- Fix Category inconsistencies (all electronics-related typos → "Electronics")  

- Impute missing Regions using CustomerID's most common region  

- Create `IsPromo` flag from PromoCode  
 
**2. Complex DateTime Operations**  

- Convert all dates to UTC datetime  

- Calculate order processing time (assume returns happen 7 days after order)  

- Find weekly sales trends for electronics vs home goods  

- Identify customers with >2 orders in any 14-day window  
 
**3. Advanced Collections & Optimization**  

- Build nested dictionary: `{CustomerID: {"total_spent": X, "favorite_category": Y}}`  

- Use `defaultdict` to track return rates by region: `{"North": 0.25, ...}`  

- Find most common promo code sequence using `itertools` and `Counter`  

- Optimize memory usage by downcasting numerical columns  
 
**4. Bonus (If Time Permits)**  

- Create UDF to flag "suspicious orders" (multiple returns + high value)  

- Calculate rolling 7-day average sales using efficient windowing  
 