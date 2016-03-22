import akka.actor.ActorSystem
import akka.util.ByteString
import akka.zeromq.{Bind, SocketType, ZMQMessage, ZeroMQExtension}
import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.regression.{LabeledPoint, StreamingLinearRegressionWithSGD}
import org.apache.spark.streaming.{Seconds, StreamingContext}

object LinearPublisher {

  def streamParser(s: String) = {
    val parts = s.split(",", -1)
    val label = parts(0).toDouble
    val features = Vectors.dense(parts.drop(1).map(_.toDouble))
    LabeledPoint(label, features)
  }

  def main(args: Array[String]): Unit = {

    Logger.getLogger("org").setLevel(Level.WARN)
    Logger.getLogger("akka").setLevel(Level.WARN)
    val logger = Logger.getLogger(LinearPublisher.getClass.getName)

    val conf = new SparkConf().setMaster("local[*]").setAppName("LinearMLpublisher")
    val ssc = new StreamingContext(conf, Seconds(1))
    ssc.checkpoint("forCheckpoints/")

    val Seq(url, topic) = Seq("tcp://127.0.0.1:5555", "lrModel")
    val acs: ActorSystem = ActorSystem()
    val pubSocket = ZeroMQExtension(acs).newSocket(SocketType.Pub, Bind(url))

    val lines = ssc.textFileStream("src/main/bash/dataDir/")
    val fvs = lines map streamParser

    lines.print(5)

    val model = new StreamingLinearRegressionWithSGD().setInitialWeights(Vectors.zeros(2)).setStepSize(0.0001)
    model.trainOn(fvs)

    val myPreds = fvs.transform { (rdd, time) =>
      val latest = model.latestModel()
      val randMessage = ByteString(time.toString + "\t" + latest.weights.toString)
      pubSocket ! ZMQMessage(randMessage)
      rdd.map(x => (x, latest.intercept, latest.weights))
    }

    myPreds.print(5)

    sys.ShutdownHookThread {
      logger.info("Attempted graceful exit")
      ssc.stop(true, true)
      logger.info("Stopped")
    }

    ssc.start()
    ssc.awaitTermination()
  }

}
