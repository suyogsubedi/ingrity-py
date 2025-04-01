from pyspark.sql import SparkSession
from pyspark.sql.functions import col, collect_list, concat_ws
from pyspark.sql.window import Window

# Initialize a Spark session
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Load the input data into a Spark DataFrame
input_spark_df = spark.read.csv("Input_data.csv", header=True, inferSchema=True)

# Create a window specification to order by PARENT_CATEGORY_ID
window_spec = Window.orderBy("PARENT_CATEGORY_ID")

# Add the new column "Web_TREE" by concatenating the hierarchy of categories
df_out = input_spark_df.withColumn(
    "Web_TREE", 
    concat_ws("_", collect_list(col("PARENT_CATEGORY_ID")).over(window_spec))
)



# Save the resulting dataframe as JSON and Parquet
df_out.write.csv("./out/json", mode="overwrite")
df_out.write.parquet("./out/parquet", mode="overwrite")

# Show the first few rows of the resulting dataframe
df_out.show(5, truncate=False)

# Stop the Spark session
spark.stop()
