from ts3plugin import ts3plugin
from websocket import create_connection
import ts3lib, ts3defines
from influxdb import InfluxDBClient
import datetime
from PythonQt.QtCore import QTimer


class influxts(ts3plugin):
	"""docstring for overlayplugin"""
	name = "influxPing"
	requestAutoload = True
	version = "0.1"
	apiVersion = 21
	author = "Scratch"
	description = "Logs ping to InfluxData"
	offersConfigure = False
	commandKeyword = ""
	infoTitle = ""
	menuItems = []
	hotkeys = []
	influx = InfluxDBClient('localtoast', 8086, 'root', 'root', database='teamspeak')
	timer = QTimer()
	
	def __init__(self):
		self.timer.timeout.connect(self.check)
		self.timer.start(1000)
		

	def check(self):
		time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		jsonlist = []
		for i in ts3lib.getServerConnectionHandlerList()[1]:
			ping = self.ping(i)
			jsonlist.append({
				"measurement": "ping",
				"tags": {
					"IP": ts3lib.getConnectionVariableAsString(i, ts3lib.getClientID(i)[1], ts3defines.ConnectionProperties.CONNECTION_SERVER_IP)[1]
				},
				"time": time,
				"fields": {
					"ping": ping[0],
					"deviation": ping[1]
				}
			})
		self.influx.write_points(jsonlist)
				

	def ping(self, schid):
		return (ts3lib.getConnectionVariableAsDouble(schid, ts3lib.getClientID(schid)[1], ts3defines.ConnectionProperties.CONNECTION_PING)[1], ts3lib.getConnectionVariableAsDouble(schid, ts3lib.getClientID(schid)[1], ts3defines.ConnectionProperties.CONNECTION_PING_DEVIATION)[1])