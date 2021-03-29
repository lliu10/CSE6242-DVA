// Databricks notebook source
// STARTER CODE - DO NOT EDIT THIS CELL
import org.apache.spark.sql.functions.desc
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import spark.implicits._
import org.apache.spark.sql.expressions.Window

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
val customSchema = StructType(Array(StructField("lpep_pickup_datetime", StringType, true), StructField("lpep_dropoff_datetime", StringType, true), StructField("PULocationID", IntegerType, true), StructField("DOLocationID", IntegerType, true), StructField("passenger_count", IntegerType, true), StructField("trip_distance", FloatType, true), StructField("fare_amount", FloatType, true), StructField("payment_type", IntegerType, true)))

// COMMAND ----------

// STARTER CODE - YOU CAN LOAD ANY FILE WITH A SIMILAR SYNTAX.
val df = spark.read
   .format("com.databricks.spark.csv")
   .option("header", "true") // Use first line of all files as header
   .option("nullValue", "null")
   .schema(customSchema)
   .load("/FileStore/tables/nyc_tripdata.csv") // the csv file which you want to work with
   .withColumn("pickup_datetime", from_unixtime(unix_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy HH:mm")))
   .withColumn("dropoff_datetime", from_unixtime(unix_timestamp(col("lpep_dropoff_datetime"), "MM/dd/yyyy HH:mm")))
   .drop($"lpep_pickup_datetime")
   .drop($"lpep_dropoff_datetime")

// COMMAND ----------

// LOAD THE "taxi_zone_lookup.csv" FILE SIMILARLY AS ABOVE. CAST ANY COLUMN TO APPROPRIATE DATA TYPE IF NECESSARY.

// ENTER THE CODE BELOW

var taxiSchema = StructType(Array(StructField("LocationID", IntegerType, true), StructField("Borough", StringType, true), 
                                  StructField("Zone", StringType, true), StructField("service_zone", StringType, true)))
                                  
val taxi_zone = spark.read
   .format("com.databricks.spark.csv")
   .option("header", "true") // Use first line of all files as header
   .option("nullValue", "null")
   .schema(taxiSchema)
   .load("/FileStore/tables/taxi_zone_lookup.csv") // the csv file which you want to work with 


// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
// Some commands that you can use to see your dataframes and results of the operations. You can comment the df.show(5) and uncomment display(df) to see the data differently. You will find these two functions useful in reporting your results.
display(df)
// df.show(5) // view the first 5 rows of the dataframe

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
// Filter the data to only keep the rows where "PULocationID" and the "DOLocationID" are different and the "trip_distance" is strictly greater than 2.0 (>2.0).

// VERY VERY IMPORTANT: ALL THE SUBSEQUENT OPERATIONS MUST BE PERFORMED ON THIS FILTERED DATA

val df_filter = df.filter($"PULocationID" =!= $"DOLocationID" && $"trip_distance" > 2.0)
df_filter.show(5)

// COMMAND ----------

// PART 1a: The top-5 most popular drop locations - "DOLocationID", sorted in descending order - if there is a tie, then one with lower "DOLocationID" gets listed first
// Output Schema: DOLocationID int, number_of_dropoffs int 

// Hint: Checkout the groupBy(), orderBy() and count() functions.

// ENTER THE CODE BELOW
val top_do_loc = df_filter.groupBy("DOLocationID")
                            .count()
                            .withColumnRenamed("count","number_of_dropoffs")
                            .orderBy($"number_of_dropoffs".desc, $"DOLocationID".asc)
                            
val top_do_loc_5 = top_do_loc.limit(5)

top_do_loc_5.show()

// COMMAND ----------

// PART 1b: The top-5 most popular pickup locations - "PULocationID", sorted in descending order - if there is a tie, then one with lower "PULocationID" gets listed first 
// Output Schema: PULocationID int, number_of_pickups int

// Hint: Code is very similar to part 1a above.

// ENTER THE CODE BELOW
val top_pu_loc = df_filter.groupBy("PULocationID").count().withColumnRenamed("count","number_of_pickups")
                               .orderBy($"number_of_pickups".desc, $"PULocationID".asc)

val top_pu_loc_5 = top_pu_loc.limit(5)

top_pu_loc_5.show()


// COMMAND ----------

// PART 2: List the top-3 locations with the maximum overall activity, i.e. sum of all pickups and all dropoffs at that LocationID. In case of a tie, the lower LocationID gets listed first.
// Output Schema: LocationID int, number_activities int

// Hint: In order to get the result, you may need to perform a join operation between the two dataframes that you created in earlier parts (to come up with the sum of the number of pickups and dropoffs on each location). 

// ENTER THE CODE BELOW
val all_activity = top_pu_loc.join(top_do_loc, top_pu_loc("PULocationID") <=> top_do_loc("DOLocationID"))

val max_activity = all_activity.select($"PULocationID", $"number_of_pickups" + $"number_of_dropoffs")
                               .withColumnRenamed("PULocationID", "LocationID")
                               .withColumnRenamed("(number_of_pickups + number_of_dropoffs)", "number_activities")
                               .orderBy($"number_activities".desc, $"LocationID".asc)

val max_activity_3 = max_activity.limit(3)

max_activity_3.show()


// COMMAND ----------

// PART 3: List all the boroughs in the order of having the highest to lowest number of activities (i.e. sum of all pickups and all dropoffs at that LocationID), along with the total number of activity counts for each borough in NYC during that entire period of time.
// Output Schema: Borough string, total_number_activities int

// Hint: You can use the dataframe obtained from the previous part, and will need to do the join with the 'taxi_zone_lookup' dataframe. Also, checkout the "agg" function applied to a grouped dataframe.

// ENTER THE CODE BELOW
val boroughs_activity = max_activity.join(taxi_zone, "LocationID").select("Borough", "number_activities")
val boroughs_activity_count = boroughs_activity.groupBy("Borough").count().withColumnRenamed("count", "total_number_activities").orderBy($"total_number_activities".desc)

boroughs_activity_count.show()


// COMMAND ----------

// PART 4: List the top 2 days of week with the largest number of (daily) average pickups, along with the values of average number of pickups on each of the two days. The day of week should be a string with its full name, for example, "Monday" - not a number 1 or "Mon" instead.
// Output Schema: day_of_week string, avg_count float

// Hint: You may need to group by the "date" (without time stamp - time in the day) first. Checkout "to_date" function.

// ENTER THE CODE BELOW
val day_avg = df_filter.groupBy(
  date_format(to_date($"pickup_datetime"),"EEEE").as("Day")).agg(avg("PULocationID").as("avg_count")).
  select("Day", "avg_count").orderBy($"avg_count".desc).limit(2)

day_avg.show()

// COMMAND ----------

// PART 5: For each particular hour of a day (0 to 23, 0 being midnight) - in their order from 0 to 23, find the zone in Brooklyn borough with the LARGEST number of pickups. 
// Output Schema: hour_of_day int, zone string, max_count int

// Hint: You may need to use "Window" over hour of day, along with "group by" to find the MAXIMUM count of pickups

// ENTER THE CODE BELOW 
val zone_count = df_filter.join(taxi_zone, df_filter("PULocationID") <=> taxi_zone("LocationID"))
                            .where($"Borough" === "Brooklyn")
                            .withColumn("pickup_datetime", hour($"pickup_datetime"))
                            .withColumnRenamed("pickup_datetime", "hour_of_day")
                            .groupBy("hour_of_day", "Zone")
                            .agg(count("Zone").as("max_count")) // count all Zones for a given hour
                            .withColumn("rank", rank().over(Window.partitionBy($"hour_of_day").orderBy($"max_count".desc))) // rank each max_count per hour
                            .select("hour_of_day","zone","max_count").where($"rank" === 1).orderBy("hour_of_day") // Select the top ranked max_count for each hour


                         
zone_count.show(50)


//reference: https://stackoverflow.com/questions/64364563/scala-spark-use-window-function-to-find-max-value

// COMMAND ----------

// PART 6 - Find which 3 different days of the January, in Manhattan, saw the largest percentage increment in pickups compared to previous day, in the order from largest increment % to smallest increment %. 
// Print the day of month along with the percent CHANGE (can be negative), rounded to 2 decimal places, in number of pickups compared to previous day.
// Output Schema: day int, percent_change float


// Hint: You might need to use lag function, over a window ordered by day of month.
// ENTER THE CODE BELOW

var win = Window.orderBy("day")

val manhattatan_table = df_filter.join(taxi_zone, df_filter("PULocationID") <=> taxi_zone("LocationID")).where($"Borough" === "Manhattan").where(month(to_date($"pickup_datetime")) === 1).withColumn("pickup_datetime",dayofmonth($"pickup_datetime")).withColumnRenamed("pickup_datetime", "day").groupBy("day").agg(count("day").as("day_count"))


val part6 = manhattatan_table.withColumn("day_before", lag("day_count", 1, "<default_value>") over win).withColumn("change", (($"day_count" - $"day_before")/$"day_before") *100).withColumn("percent_change", round(col("change"),2)).orderBy($"percent_change".desc).limit(3).select("day", "percent_change")

part6.show(20)

// COMMAND ----------


