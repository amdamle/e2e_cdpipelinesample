# Databricks notebook source
df = spark.read.option("header","true").option("inferSchema","true").csv("/mnt/adbauto/titanic.csv")
df.count()

# COMMAND ----------

df.createTempView("titanic_v")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from titanic_v where Age >25