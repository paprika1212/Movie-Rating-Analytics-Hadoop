from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, round

# Initialize Spark
spark = SparkSession.builder.appName("MovieRatingAnalysis").getOrCreate()

# Load Data (HDFS Paths)
# Assumes data is uploaded to /input/ folder in HDFS
ratings = spark.read.csv("hdfs://master:9000/input/u.data", sep="\t", inferSchema=True).toDF("user_id", "movie_id", "rating", "timestamp")
movies = spark.read.csv("hdfs://master:9000/input/u.item", sep="|", inferSchema=True).select(col("_c0").alias("movie_id"), col("_c1").alias("title"))

# Analysis: Avg Rating per Movie
avg_ratings = ratings.groupBy("movie_id").agg(round(avg("rating"), 2).alias("avg_rating"))
result = avg_ratings.join(movies, "movie_id").orderBy(col("avg_rating").desc())

# Save Output for UI
result.coalesce(1).write.mode("overwrite").header("true").csv("file:///home/user/project_output")

spark.stop()