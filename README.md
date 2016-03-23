* For the sake of simplicity, we prepare a **synthetic data set** consisting of random points `(y, x1, x2)` which approximately satisfy the following linear relationship:

![equation](http://www.sciweavers.org/tex2img.php?eq=y%20%5Capprox%20c_1%20x_2%20%2B%20c_2%20x_2&bc=White&fc=Black&im=gif&fs=12&ff=arev&edit=0)  

where the coefficients `(c1 = 3.2, c2 = 0.6)` and the intensity of the noise serve as control parameters.

- Adopting supervised learning terminology, one may refer to `y` as a **label** and to each instance of `(x1, x2)` as a **feature vector**.  Naturally, the objective then becomes to uncover the values of the coefficients `(c1, c2)` given the feature vectors 
and their labels. 

- In order to **mimic streaming data**, one can generate batches of feature vectors and labels (60 at a time in our case) and save them as new HDFS files every second or so in a directory that the spark streaming application uses a input source.
> _(You can do this by running the bash script dataStreamer.sh directly from the command line.)_

- Every time a new batch of data is produced, the spark application applies a least squares minimizer (**StreamingLinearRegressionWithSGD** in our case) which **updates the regression coefficients `(c1, c2)`**.
> _(You can do this by running linearPublisher.scala directly from your IDE for simplicity)_

- The final step consists in providing a **real time visualization** of the model and of its history.  For example, one may be interested in gaining a deeper insight into the dynamics of the model (as the contents of the data stream may change in time) or may want to be alerted immediately if the model starts to misbehave (abnormal coefficients).

- This can be accomplished through the **publish-subscribe** messaging pattern by using ZeroMQ.  In our case, the spark streaming application acts as the publisher in order to communicates via a TCP socket with a **HTTP web server** which acts as the subscriber and prepares a visual rendering of the dynamics of the model (`localhost:5556`).
> _(For this, you'll need to have started the flask server by running flaskSubscriber.py)_

+ The illustration provides a cartoon summary of the flow of data described above:
<p align="center">
<img src="src/main/resources/demoLinearStream.gif" width="700"/>
</p>
