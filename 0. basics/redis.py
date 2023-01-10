from pyspark.sql import SparkSession
import redis

def main():
    spark = SparkSession.builder.appName("Redis Cloud Example").getOrCreate()
    sc = spark.sparkContext

    # Set Redis Cloud connection details
    host = "redis-16287.c302.asia-northeast1-1.gce.cloud.redislabs.com:16287"
    password = "WpnrnezZHgXgnsM9K1xEbzwLwrVTRym6"
    port = 16287
    #port = 6380

    # Write data to Redis Cloud
    jedis = redis.StrictRedis(host=host, port=port, password=password)
    jedis.set("key", "value")

    # Read data from Redis Cloud
    rdd = sc.fromRedisKeyPattern("*", host=host, port=port, password=password)
    rdd.foreach(print)

if __name__ == "__main__":
    main()
