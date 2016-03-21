from flask import Flask, render_template, Response
import zmq
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import StringIO
import matplotlib.pyplot as plt

app = Flask(__name__)
app.context = zmq.Context()
port = '5555'

def doublePlotter(fig, ax, timeData, xData, yData):
	ax[0].plot(timeData, xData, color='r', linewidth=2); ax[1].plot(timeData, yData, color='b', linewidth=2)
	ax[0].set_ylabel('coeff1'); ax[1].set_ylabel('coeff2')
	ax[0].axhline(3.2, color='k', ls='dashed'); ax[1].axhline(0.6, color='k', ls='dashed')
	canvas = FigureCanvas(fig)
	picOutput = StringIO.StringIO()	
	canvas.print_png(picOutput)
	return picOutput.getvalue()

def generateImage():
	historyTime, historyCoeff1, historyCoeff2 = [], [], []
	fig, ax = plt.subplots(2, sharex=True)
	sock = app.context.socket(zmq.SUB)
	sock.connect("tcp://localhost:%s" % port)
	sock.setsockopt(zmq.SUBSCRIBE, '')
    	while True:
		rawMewssage = sock.recv()
		msg = rawMewssage.split('\t')
		msgTime, msgContent = msg[0], msg[1]
		coeffTime = float(msgTime.replace(' ms', ''))
		coeffVals = msgContent.replace('[','').replace(']','').split(',')
		coeff1, coeff2 = float(coeffVals[0]), float(coeffVals[1])
		historyTime.append(coeffTime); historyCoeff1.append(coeff1); historyCoeff2.append(coeff2)
		print zip(historyTime, historyCoeff1, historyCoeff2)
		frame = doublePlotter(fig, ax, historyTime, historyCoeff1, historyCoeff2)	
        	yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/streamPath')
def stream():
	return Response(generateImage(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5556, threaded=True)

