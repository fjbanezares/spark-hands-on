from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType,DateType
from pyspark.sql import SparkSession, Row

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.master", "local") \
    .config("spark.executor.extraClassPath", "postgresql-42.2.2.jar") \
    .config("spark.driver.extraClassPath", "postgresql-42.2.2.jar") \
    .getOrCreate()

#reading a DF
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.read.html
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.html
# df = spark.read.format('json').load(['python/test_support/sql/people.json','python/test_support/sql/people1.json'])
firstDF = spark.read.json("cars.json")
firstDF.show()
firstDF.printSchema()
# we didn't define the Schema but it inferred it

# Data is distributed in the cluster, here we take a number of rows and print them
# In Scala... firstDF.take(10).foreach(print)
# For Python we iterate the list:
for row in firstDF.take(10):
    print("An element on the RDD",row)

# Now we are going to define the Schema as instructed in the API
# https://spark.apache.org/docs/latest/sql-ref-datatypes.html
# StructField(name, type, nullable true by default),
carsSchema = StructType([
    StructField("Name", StringType()),
    StructField("Miles_per_Gallon", DoubleType()),
    StructField("Cylinders", LongType()),
    StructField("Displacement", DoubleType()),
    StructField("Horsepower", LongType()),
    StructField("Weight_in_lbs", LongType()),
    StructField("Acceleration", DoubleType()),
    StructField("Year", StringType()),
    StructField("Origin", StringType())
])

# We can obtain the Schema from a dataframe
carsDFSchema = firstDF.schema

print(carsSchema)
print(carsDFSchema) # We can see the orders doesn't matter


# Dataframe is a distributed collection of Rows conforming to the schema
# In production we should not infer the Schema, but force it and correct if failures:

carsDFWithSchema = spark.read.json("cars.json", schema=carsSchema)
carsDFWithSchema.show()


# Create a Row manually
myRow = Row("chevrolet chevelle malibu",18,8,307,130,3504,12.0,"1970-01-01","USA")

cars = [
    ("chevrolet chevelle malibu",18,8,307,130,3504,12.0,"1970-01-01","USA"),
    ("buick skylark 320",15,8,350,165,3693,11.5,"1970-01-01","USA"),
    ("plymouth satellite",18,8,318,150,3436,11.0,"1970-01-01","USA"),
    ("amc rebel sst",16,8,304,150,3433,12.0,"1970-01-01","USA"),
    ("ford torino",17,8,302,140,3449,10.5,"1970-01-01","USA"),
    ("ford galaxie 500",15,8,429,198,4341,10.0,"1970-01-01","USA"),
    ("chevrolet impala",14,8,454,220,4354,9.0,"1970-01-01","USA"),
    ("plymouth fury iii",14,8,440,215,4312,8.5,"1970-01-01","USA"),
    ("pontiac catalina",14,8,455,225,4425,10.0,"1970-01-01","USA"),
    ("amc ambassador dpl",15,8,390,190,3850,8.5,"1970-01-01","USA")
]

carsSchemaAdapted = StructType([
    StructField("Name", StringType()),
    StructField("Miles_per_Gallon", LongType()),
    StructField("Cylinders", LongType()),
    StructField("Displacement", LongType()),
    StructField("Horsepower", LongType()),
    StructField("Weight_in_lbs", LongType()),
    StructField("Acceleration", DoubleType()),
    StructField("Year", StringType()),
    StructField("Origin", StringType())
])

manualCarsDF = spark.createDataFrame(cars) # schema auto-inferred
manualCarsDF.show()

manualCarsDFSchema = spark.createDataFrame(cars, schema=carsSchemaAdapted)  # schema auto-inferred
manualCarsDFSchema.show()
print("The datafame has ", manualCarsDFSchema.count(), " rows.")



# Reading a DF:
# - format
# - schema or inferSchema = true
# - path (s3 bucket, local filesystem,
# - zero or more options

# mode, what to do if a record don't conforme to the schema
# failfast ... exception eagerly crash
# permisive (defauklt) is ignore the record with the invalid value

carsSchemaDatasourcesPlay = StructType([
    StructField("Name", StringType()),
    StructField("Miles_per_Gallon", LongType()),
    StructField("Cylinders", LongType()),
    StructField("Displacement", LongType()),
    StructField("Horsepower", LongType()),
    StructField("Weight_in_lbs", LongType()),
    StructField("Acceleration", DoubleType()),
    StructField("Year", StringType()),
    StructField("Origin", StringType())
])

carsDF = spark.read.load(format="json", schema=carsSchemaDatasourcesPlay, mode="PERMISSIVE", path="cars.json")
# use FAILFAST and change Name to be Long and see it fail
carsDF.show()


 # Writing DFs
 # - format  --> json, parquet, orc, ...
 # - save mode = overwrite, append, ignore, errorIfExists --> how to act if file already exist on filesystem
 # - path
 # - zero or more options

# https://sparkbyexamples.com/spark/spark-overwrite-the-output-directory/
carsDF.write.format("json").mode("overwrite").save("pepito.json")
# generate crc to validate integrity and SUCCESS
# In general each partition has its own file, coalesce to N small

# JSON flags
carsSchemaDate = StructType([
    StructField("Name", StringType()),
    StructField("Miles_per_Gallon", LongType()),
    StructField("Cylinders", LongType()),
    StructField("Displacement", LongType()),
    StructField("Horsepower", LongType()),
    StructField("Weight_in_lbs", LongType()),
    StructField("Acceleration", DoubleType()),
    StructField("Year", DateType()),
    StructField("Origin", StringType())
])
# bzip2, gzip, lz4, snappy, deflate Spark decompress automatically
sparkDFFromJSON = spark.read\
    .option("dateFormat", "YYYY-MM-dd") \
    .option("compression", "uncompressed") \
    .load(format="json", schema=carsSchemaDate, mode="PERMISSIVE",  path="cars.json")

sparkDFFromJSON.show(7)

# CSV flags
stocksSchema = StructType([
    StructField("symbol", StringType()),
    StructField("date", DateType()),
    StructField("price", DoubleType())
])

sparkDFFromCSV = spark.read \
    .schema(stocksSchema)\
    .option("header", "true") \
    .option("sep", ",") \
    .option("nullValue", "") \
    .csv("stocks.csv")

sparkDFFromCSV.head(7)


# Parquet ... fast reading of Columns
# Very predictable, no need of many options


sparkDFFromCSV.write.mode("overwrite").save("cars.parquet")

# mode("overwrite") makes don't crash if the file is there




#Text files

spark.read.text("sampleTextFile.txt").show()


#Reading from a remote DB
# docker-compose up in a terminal
#  https://jdbc.postgresql.org/download/
# version 42.2.2

driver = "org.postgresql.Driver"
url = "jdbc:postgresql://localhost:5432/rtjvm"
user = "docker"
password = "docker"

employeesDF = spark.read \
    .format("jdbc") \
    .option("driver", driver) \
    .option("url", url) \
    .option("user", user) \
    .option("password", password) \
    .option("dbtable", "public.employees") \
    .load()

print("From an external database into Spark...:")
employeesDF.show()


# Once you specify the right options is not that scary

# Exercise: read the movies DF, then write it as
# tab-separated values file TSB
# snappy Parquet
# table "public.movies" in the Postgres DB

moviesDF = spark.read.json("movies.json")

moviesDF.write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", "true") \
    .option("sep", "\t") \
    .save("movies.csv") \

#Parquet
moviesDF.write.mode("overwrite").save("movies.parquet")

#save to DF
# default SaveMode: ErrorIfExists.
moviesDF.write \
    .mode("overwrite") \
    .format("jdbc") \
    .option("driver", driver) \
    .option("url", url) \
    .option("user", user) \
    .option("password", password) \
    .option("dbtable", "public.moviesjavi") \
    .save()


#Use of Columns
# Scala  titleColumn = moviesDF.col("Title")
titleColumn = moviesDF.columns
print("mira el tipo de la columna", type(titleColumn[0]))

#Selecting, projection (projecting the df into a new one with less data)
moviesDF.select("title","Release_Date", "Production_Budget").show()
moviesDF.select(moviesDF['title'], moviesDF['Release_Date'], moviesDF["Production_Budget"]/1000000).show()
dataGroupedCounted = moviesDF.groupBy("Production_Budget").count()
print("de que tipo es esto", type(dataGroupedCounted))
print("de que tipo es esto", type(moviesDF))


# very helpful functions
from pyspark.sql.functions import desc, col, column

dataGroupedCounted.orderBy(desc(col="Production_Budget")).show()
dataGroupedCounted.orderBy(desc(col="count")).show()

# "Pirates of the Caribbean: At World's End" had 300 M budget

# Select is super powerful
# case unsensitive
dataFrameToShowSelect = moviesDF.select("title",col("Release_Date").alias("estreno"), column("Production_Budget"), 'Title')

dataFrameToShowSelect.show()

print("col(Title) has type...", type(col("Title")))
print("column(Title) has type...", type(column("Title")))

# formally add a new column
dataFrameToShowSelect.withColumn("nueva columna", column("Production_Budget") * 10000000).show()

# formally rename a  column
rename = dataFrameToShowSelect.withColumnRenamed("estreno", "dia del estreno" )
rename.select("`dia del estreno`").show()

#PySpark es maravilloso no harian falta los backticks

# remove columns
dataFrameToShowSelect.drop("Production_Budget", "Title").show()

# Filter
dataFrameToShowSelect.filter(dataFrameToShowSelect['Production_Budget'] > 250000000).show()

dataFrameToShowSelect.filter(dataFrameToShowSelect['Production_Budget'] == 250000000).show()

# Chase it until you get it
dataFrameToShowSelect.filter((dataFrameToShowSelect['Production_Budget'] > 250000000).__and__
                (dataFrameToShowSelect['Production_Budget'] != 300000000)).show()

# Unioning with dfs with same schema
moreCarsDF = spark.read.load(format="json", schema=carsSchemaDatasourcesPlay, mode="PERMISSIVE", path="more_cars.json")
carsDF.union(moreCarsDF).count()
print("number of cars of more cars...",moreCarsDF.count())
print("number of cars of cars...",carsDF.count())

print("number of cars of the union...",carsDF.union(moreCarsDF).count())


# distinct
carsDF.select("Origin").distinct().show()


# 1. Read the movies DF and select 2 columns of your choice
# 2. Create another column summing up the total profit of the movies = US_Gross + Worldwide_Gross + DVD sales
# 3. Select all COMEDY movies with IMDB rating above 6
#
# Use as many ways as possible

moviesDF = spark.read.option("inferSchema", "true").json("movies.json")
moviesDF.show()

#1 Trivial

#2
moviesDF.select(
    col("Title"),
    col("US_Gross"),
    col("Worldwide_Gross"),
    col("US_DVD_Sales"),
    (col("US_Gross") + col("Worldwide_Gross")).alias("Total_Gross")).show()

moviesDF.selectExpr("Title",
                    "US_Gross",
                    "Worldwide_Gross",
                    "US_Gross + Worldwide_Gross as Total_Gross"
                    ).show()

moviesDF.select("Title", "US_Gross", "Worldwide_Gross") \
.withColumn("Total_Gross", col("US_Gross") + col("Worldwide_Gross")).show()




#3
atLeastMediocreComediesDF = moviesDF.select("Title", "IMDB_Rating") \
    .where((col("Major_Genre") == 'Comedy') & (col("IMDB_Rating") > 6))

atLeastMediocreComediesDF.show()

comediesDF2 = moviesDF.select("Title", "IMDB_Rating") \
    .where(col("Major_Genre") == 'Comedy') \
    .where(col("IMDB_Rating") > 6)

comediesDF2.show()

comediesDF3 = moviesDF.select("Title", "IMDB_Rating")\
.where("Major_Genre = 'Comedy' and IMDB_Rating > 6")

comediesDF3.show()



################
#    AGGREGATIONS AND GROUPING
################

# Counting
from pyspark.sql.functions import count, countDistinct, approx_count_distinct

genresCountDF = moviesDF.select(count(col("Major_Genre"))) # all the values except null
genresCountDF.show()
moviesDF.selectExpr("count(Major_Genre)").show()
moviesDF.select(count("*")).show() # all
moviesDF.select(countDistinct("*")).show() # all
moviesDF.select(countDistinct("Major_Genre")).show() # all

#aprox count
moviesDF.select(approx_count_distinct("Major_Genre")).show() # all
moviesDF.printSchema()

from pyspark.sql.functions import min, max, sum
#min and max
moviesDF.selectExpr("max(IMDB_Rating)").show()
moviesDF.select(min(col("IMDB_Rating"))).show()

#sum
moviesDF.select(sum(col("US_Gross"))).show()
moviesDF.selectExpr("sum(US_Gross)").show()

from pyspark.sql.functions import avg, mean, stddev
#avg
moviesDF.select(avg(col("Rotten_Tomatoes_Rating"))).show()
moviesDF.selectExpr("avg(Rotten_Tomatoes_Rating)").show()

#data science
moviesDF.select(
    mean(col("Rotten_Tomatoes_Rating")),
    stddev(col("Rotten_Tomatoes_Rating"))
).show()

#Grouping
# group by includ the nulls

countByGenreDF = moviesDF \
    .groupBy(col("Major_Genre"))  \
    .count().show()

avgRatingByGenreDF = moviesDF \
.groupBy(col("Major_Genre")) \
.avg("IMDB_Rating").show()

aggregationsByGenreDF = moviesDF \
.groupBy(col("Major_Genre")) \
.agg(
    count("*").alias("N_Movies"),
                 avg("IMDB_Rating").alias("Avg_Rating") )  \
.orderBy(col("Avg_Rating")).show()

# 1. Sum up ALL the profits of ALL the movies in the DF
# 2. Count how many distinct directors we have
# 3. Show the mean and standard deviation of US gross revenue for the movies
# 4. Compute the average IMDB rating and the average US gross revenue PER DIRECTOR

moviesDF \
    .select((col("Worldwide_Gross") + col("US_Gross") + col("US_DVD_Sales") - col("Production_Budget")).alias("profit")) \
    .select(sum(col("profit")))\
    .show()

moviesDF \
.select((col("US_Gross") + col("Worldwide_Gross") + col("US_DVD_Sales")).alias("Total_Gross")) \
.select(sum("Total_Gross")) \
.show()


#2
moviesDF \
.select(countDistinct(col("Director")))\
.show()

#3
moviesDF.select(
    mean("US_Gross"),
    stddev("US_Gross")
).show()

#4
moviesDF.groupBy(col("Director")).agg(sum("US_Gross").alias("Total_US_Gross"),avg("IMDB_Rating").alias("Avg_Rating")) \
    .orderBy(desc(col="Avg_Rating")).show()


# moviesDF \
#     .groupBy(col("Director")) \
#     .agg(
#     avg("IMDB_Rating").alias("Avg_Rating"),
#     sum("US_Gross").alias("Total_US_Gross")) \
#     .orderBy(col("Avg_Rating").desc).show()


# Aggregations are wide tx,
    # One or more input partition contribute to one or more output partitions
    # shuffle is data being moved between nodes
    # big impact in performance
    # to agg at the end, only if necessary, I add to caching when you will reuse


# JOINNING

# employees data
emp = [(1,"Smith",-1,"2018","10","M",3000),
       (2,"Rose",1,"2010","20","M",4000),
       (3,"Williams",1,"2010","10","M",1000),
       (4,"Jones",2,"2005","10","F",2000),
       (5,"Brown",2,"2010","40","",-1),
       (6,"Brown",2,"2010","50","",-1)]
empColumns = ["emp_id","name","superior_emp_id","year_joined","emp_dept_id","gender","salary"]
empDF = spark.createDataFrame(data=emp, schema = empColumns)
empDF.printSchema()
empDF.show(truncate=False)

# departments data
dept = [("Finance",10),
        ("Marketing",20),
        ("Sales",30),
        ("IT",40)]
deptColumns = ["dept_name","dept_id"]
deptDF = spark.createDataFrame(data=dept, schema = deptColumns)
deptDF.printSchema()
deptDF.show(truncate=False)

# inner --> Only where keys match. no match is filter, several matches are N*M key duplicates
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"inner").show(truncate=False)

# Full ... coalesce
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"outer").show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"full").show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"fullouter").show(truncate=False)

# Left --> All left, right only if match. no match is one line, N*M lines if there are matches
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"left").show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"leftouter").show(truncate=False)

# Right --> All right, left only if match. no match is one line,  N*M lines if there are matches
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"right").show(truncate=False)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"rightouter").show(truncate=False)

# Left semi --> Inner returning only columns in left (right acts as a filter)
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"leftsemi").show(truncate=False)

# Left Anti --> Similar, but filter when there is no match
# como hacer left join y filtrar quedandonos con las que tienen null
empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"leftanti").show(truncate=False)

## self join
#empDF.alias("emp1").join(empDF.alias("emp2"), col("emp1.superior_emp_id") == col("emp2.emp_id"),"inner") \
#    .select(col("emp1.emp_id"),col("emp1.emp_id.name"),
#            col("emp2.emp_id").alias("id jefe"),
#            col("emp2.name").alias("jefe")).show(truncate=False)

# Bands and Guitar Players
guitarsDF = spark.read \
.option("inferSchema", "true") \
.json("guitars.json")

guitaristsDF = spark.read \
.option("inferSchema", "true") \
.json("guitarPlayers.json")

bandsDF = spark.read \
.option("inferSchema", "true") \
.json("bands.json")

guitarsDF.show()
guitaristsDF.show()
bandsDF.show()
# inner join guitarist band
# empDF.join(deptDF,empDF.emp_dept_id ==  deptDF.dept_id,"inner").show(truncate=False)

joinCondition = guitaristsDF.band == bandsDF.id # awesome
guitaristsBandsDF = guitaristsDF.join(bandsDF, joinCondition, "inner")

guitaristsBandsDF.show() # you see id and band are the same thing, handle this

#left outer = everything in the inner join + all the rows in the LEFT table, with nulls in where the data is missing
guitaristsDF.join(bandsDF, joinCondition, "left_outer").show()

#right outer = everything in the inner join + all the rows in the RIGHT table, with nulls in where the data is missing
guitaristsDF.join(bandsDF, joinCondition, "right_outer").show()

#outer join = everything in the inner join + all the rows in BOTH tables, with nulls in where the data is missing
guitaristsDF.join(bandsDF, joinCondition, "outer").show()

#semi-joins = everything in the left DF for which there is a row in the right DF satisfying the condition
guitaristsDF.join(bandsDF, joinCondition, "left_semi").show()

#anti-joins = everything in the left DF for which there is NO row in the right DF satisfying the condition
guitaristsDF.join(bandsDF, joinCondition, "left_anti").show()


#things to bear in mind
#guitaristsBandsDF.select("id", "band").show() #this crashes
# Reference 'id' is ambiguous, could be: id, id.

#option 1 - rename the column on which we are joining
guitaristsDF.join(bandsDF.withColumnRenamed("id", "band"), "band")

#option 2 - drop the dupe column
guitaristsBandsDF.drop(bandsDF.id) # need to specify it is a col from bandsDF
# This works as Spark maintains unique identifier with all columns it operates on

#option 3 - rename the offending column and keep the data
bandsModDF = bandsDF.withColumnRenamed("id", "bandId")
guitaristsDF.join(bandsModDF, guitaristsDF.band == bandsModDF.bandId)



# using complex types (tease)
# we have an array
from pyspark.sql.functions import expr
guitaristsDF.join(guitarsDF.withColumnRenamed("id", "guitarId"), expr("array_contains(guitars, guitarId)")).show()
# guitars [1, 5]  guitarId 1,2,3
# join with condition different from equality! match


# using postgres
# 1. show all employees and their max salary
# 2. show all employees who were never managers
# 3. find the job titles of the best paid 10 employees in the company

# \d salaries
# Table "public.salaries"
# Column   |  Type   | Collation | Nullable | Default
# -----------+---------+-----------+----------+---------
# emp_no    | integer |           | not null |
# salary    | integer |           | not null |
# from_date | date    |           | not null |
# to_date   | date    |           | not null |

driver = "org.postgresql.Driver"
url = "jdbc:postgresql://localhost:5432/rtjvm"
user = "docker"
password = "docker"


def readtable(tablename):
    return  spark.read \
    .format("jdbc") \
    .option("driver", driver) \
    .option("url", url) \
    .option("user", user) \
    .option("password", password) \
    .option("dbtable", "public.{}".format(tablename)) \
    .load()


employeesDF = readtable("employees")
salariesDF = readtable("salaries")
deptManagersDF = readtable("dept_manager")
titlesDF = readtable("titles")

employeesDF.show()
salariesDF.show()
deptManagersDF.show()
titlesDF.show()

#1
maxSalariesPerEmpNoDF = salariesDF.groupBy("emp_no").agg(max("salary").alias("maxSalary"))
employeesSalariesDF = employeesDF.join(maxSalariesPerEmpNoDF, "emp_no")

#2
empNeverManagersDF = employeesDF.join(deptManagersDF, employeesDF.emp_no == deptManagersDF.emp_no,"left_anti")

#3
mostRecentJobTitlesDF = titlesDF.groupBy("emp_no", "title").agg(max("to_date"))
bestPaidEmployeesDF = employeesSalariesDF.orderBy(col("maxSalary").desc).limit(10)
bestPaidJobsDF = bestPaidEmployeesDF.join(mostRecentJobTitlesDF, "emp_no")

bestPaidJobsDF.show()










