// Databricks notebook source
display(dbutils.fs.ls("dbfs:/FileStore/tables/assignment/"))

// COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/assignment/Country.csv")

// COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/assignment/Match_results.csv")

// COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/assignment/Players.csv")

// COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/assignment/Player_Assists_Goals.csv")

// COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/assignment/Player_Cards.csv")

// COMMAND ----------

dbutils.fs.head("dbfs:/FileStore/tables/assignment/Worldcup_History.csv")

// COMMAND ----------

// MAGIC %sql
// MAGIC select * from country

// COMMAND ----------

// Load each CSV into a DataFrame
val countryDF = spark.read.option("header", "true").option("inferSchema", "true").csv("dbfs:/FileStore/tables/assignment/Country.csv")
val matchResultsDF = spark.read.option("header", "true").option("inferSchema", "true").csv("dbfs:/FileStore/tables/assignment/Match_results.csv")
val playersDF = spark.read.option("header", "true").option("inferSchema", "true").csv("dbfs:/FileStore/tables/assignment/Players.csv")
val playerAssistsGoalsDF = spark.read.option("header", "true").option("inferSchema", "true").csv("dbfs:/FileStore/tables/assignment/Player_Assists_Goals.csv")
val playerCardsDF = spark.read.option("header", "true").option("inferSchema", "true").csv("dbfs:/FileStore/tables/assignment/Player_Cards.csv")
val worldcupHistoryDF = spark.read.option("header", "true").option("inferSchema", "true").csv("dbfs:/FileStore/tables/assignment/Worldcup_History.csv")

// Create temporary views for each table
countryDF.createOrReplaceTempView("COUNTRY")
matchResultsDF.createOrReplaceTempView("MATCHES")
playersDF.createOrReplaceTempView("PLAYER")
playerAssistsGoalsDF.createOrReplaceTempView("PLAYER_STATISTICS")
playerCardsDF.createOrReplaceTempView("DISCIPLINARY_RECORD")
worldcupHistoryDF.createOrReplaceTempView("PAST_WINNERS")


// COMMAND ----------

val query1 = spark.sql("""
  SELECT DISTINCT Winner AS Country_Name
  FROM PAST_WINNERS
""")
query1.show()


// COMMAND ----------

val query1 = worldcupHistoryDF.select("Winner").distinct()
query1.show()

// COMMAND ----------

val query2 = spark.sql("""
  SELECT Winner AS Country_Name, COUNT(*) AS Number_of_Worldcups_Won
  FROM PAST_WINNERS
  GROUP BY Winner
  ORDER BY Number_of_Worldcups_Won DESC
""")
query2.show()


// COMMAND ----------

import org.apache.spark.sql.functions.desc

// Task 2: Retrieve the list of country names that have won a World Cup and the number of World Cups each has won, in descending order.
val query2 = worldcupHistoryDF.groupBy("Winner")
  .count()
  .withColumnRenamed("count", "Number_of_Worldcups_Won")
  .orderBy(desc("Number_of_Worldcups_Won"))
query2.show()


// COMMAND ----------

val query3 = spark.sql("""
  SELECT Capital
  FROM COUNTRY
  WHERE Population > 100
  ORDER BY Population ASC
""")
query3.show()


// COMMAND ----------

val query3 = countryDF.filter("Population > 100")
  .select("Capital")
  .orderBy("Population")
query3.show()

// COMMAND ----------

val query4 = spark.sql("""
  SELECT DISTINCT Stadium
  FROM MATCHES
  WHERE Team1_score > 4 OR Team2_score > 4
""")
query4.show()


// COMMAND ----------

val query4 = matchResultsDF.filter("Team1_score > 4 OR Team2_score > 4")
  .select("Stadium")
  .distinct()
query4.show()

// COMMAND ----------

val query5 = spark.sql("""
  SELECT DISTINCT Host_city
  FROM MATCHES
  WHERE Stadium LIKE 'Estadio%'
""")
query5.show()


// COMMAND ----------

val query5 = matchResultsDF.filter("Stadium LIKE 'Estadio%'")
  .select("Host_city")
  .distinct()
query5.show()

// COMMAND ----------

val query6 = spark.sql("""
  SELECT Stadium, COUNT(*) AS Number_of_Matches
  FROM MATCHES
  GROUP BY Stadium
""")
query6.show()


// COMMAND ----------

val query6 = matchResultsDF.groupBy("Stadium")
  .count()
  .withColumnRenamed("count", "Number_of_Matches")
query6.show()

// COMMAND ----------

val query7 = spark.sql("""
  SELECT Fname, Lname, DOB
  FROM PLAYER
  WHERE Height > 198
""")
query7.show()


// COMMAND ----------

val query7 = playersDF.filter("Height > 198")
  .select("Fname", "Lname", "DOB")
query7.show()

// COMMAND ----------

val query8 = spark.sql("""
  SELECT p.Fname, p.Lname, p.Position, ps.Goals
  FROM PLAYER p
  JOIN PLAYER_STATISTICS ps ON p.Player_id = ps.Player_id
  JOIN DISCIPLINARY_RECORD dr ON p.Player_id = dr.Player_id
  WHERE p.Is_captain = TRUE
    AND (dr.No_of_Yellow_cards > 2 OR dr.No_of_Red_cards > 1)
""")
query8.show()


// COMMAND ----------

val query8 = playersDF
  .join(playerAssistsGoalsDF, "Player_id")
  .join(playerCardsDF, "Player_id")
  .filter("Is_captain = true AND (No_of_Yellow_cards > 2 OR No_of_Red_cards > 1)")
  .select("Fname", "Lname", "Position", "Goals")
query8.show()
