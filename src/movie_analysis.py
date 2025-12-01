from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, round

def main():
    # 1. Initialize Spark
    spark = SparkSession.builder.appName("MovieRatingAnalysis").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    print(">>> Spark Session Started...")

    # 2. Load Data from HDFS
    ratings = spark.read.csv("hdfs://master:9000/input/u.data", sep="\t", inferSchema=True) \
        .toDF("user_id", "movie_id", "rating", "timestamp")
    
    movies = spark.read.csv("hdfs://master:9000/input/u.item", sep="|", inferSchema=True) \
        .select(col("_c0").alias("movie_id"), col("_c1").alias("title"))

    # 3. Calculate Averages & Count
    # We count how many ratings a movie got to filter out tiny movies
    avg_ratings = ratings.groupBy("movie_id").agg(
        round(avg("rating"), 2).alias("avg_rating"),
        col("movie_id").alias("count_id")
    )
    
    # 4. Join with Titles and Sort
    result = avg_ratings.join(movies, "movie_id").orderBy(col("avg_rating").desc())

    # 5. Export to Local CSV (The Bridge to Streamlit)
    output_file = "/home/hadoop/movie_results.csv"
    
    print(f">>> Saving results to {output_file}...")
    
    # Convert Top 100 to Pandas and save locally
    pdf = result.limit(100).toPandas()
    pdf.to_csv(output_file, index=False)
    
    print(">>> Analysis Complete. CSV Saved.")
    spark.stop()

if __name__ == "__main__":
    main()
