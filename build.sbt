name := "simpleMLstreamer"

version := "1.0"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "1.6.0",
  "org.apache.spark" %% "spark-mllib" % "1.6.0",
  "com.databricks" %% "spark-csv" % "1.3.0",
  "org.apache.spark" %% "spark-streaming-zeromq" % "1.6.0"
)
