import openrouteservice
from openrouteservice import convert
from geopy.distance import geodesic
import time
import datetime
import folium
import webbrowser
import pika
import json
import ast


firstcoord = ""
coords = ((5.482373,51.438115),(5.483191,51.438205))
print (coords)
totalDistance =  0;
traveledDistance = 0
travelString = ""
toTravelDistance = 1
coordinates = ""
d = int(7)/10
client = openrouteservice.Client(key='5b3ce3597851110001cf6248bc38a58bed6c482bb48e670dff6a3f85')

def getcoordinates(coord):
	#print (coords+"HERE")
	geometry = client.directions(coords)['routes'][0]['geometry']
	decoded = convert.decode_polyline(geometry)
	global coordinates
	coordinates = decoded['coordinates']
	old_time = datetime.datetime.now()
	global totalDistance
	totalDistance =  0;
	start(coord)
	
def send(message,coord):
	print(message)
	global firstcoord
	connstring2 = "simulation_queue"
	connstring2 += coord
	print ("The first coord is " + coord)
	print("THE CONSTRING IS" + connstring2)
	connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue=connstring2, durable=True)
	channel.basic_publish(
    exchange='',
    routing_key=connstring2,
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
	if message=='clear':
		print("closing connection")
		connection.close()

def calc_distance(coordinates1,coordinates2):
	#pathStr = "C:\\Users\\Damhuis\\Downloads\\Maps\\test"
	#pathStr += ".html"
	#tooltip = str(i)
	#m = folium.Map(location=[coordinates1,coordinates2],zoom_start=40)
	#folium.Marker([coordinates[i][1],coordinates[i][0]], popup='<i>Mt. Hood Meadows</i>', tooltip=tooltip).add_to(m)
	#m.save(pathStr)
	#webbrowser.open('file://' + pathStr)
	global traveledDistance
	traveledDistance = 0
	global travelString
	global toTravelDistance
	print (coordinates1)
	print (coordinates2)
	toTravelDistance = geodesic(coordinates2, coordinates1).m
	print (toTravelDistance)
	travelString = ""
	message = str(coordinates1)
	message += ","
	message += str(coordinates2)
	return message
	
def travel(coordinates1,coordinates2):
	global traveledDistance
	global travelString
	traveledDistance += d
	travelString += "Walked "
	travelString += str(d)
	travelString += "m "
	travelString += "towards new point "
	travelString += str(coordinates1)
	travelString += "from point "
	travelString += str(coordinates2)
	travelString += "distance to next point is "
	travelString += str(toTravelDistance-traveledDistance)
	travelString += "m"
	travelString = ""
	time.sleep(.01)

def start(coord):
	print(coordinates)
	for i in range(len(coordinates)-1):
		message = calc_distance(coordinates[i],coordinates[i+1])
		totravelstring = "need to travel"
		totravelstring += str(toTravelDistance)
		while((toTravelDistance-traveledDistance)>0):
			travel(coordinates[i+1],coordinates[i])
		send(message,coord)
		global totalDistance
		totalDistance += geodesic(coordinates[i], coordinates[i+1]).m
	print("Stopping")
	send("stops",coord)
	send("clear",coord)
def receive():
	
	x1 = 0.0
	x2 = 0.0
	y1 = 0.0
	y2 = 0.0
	global firstcoord

	def callback(ch, method, properties, body):
		print(" [x] Received %r" % body)
		global coords
		coords = str(body)
		coords = coords.replace("b","")
		coords = coords.replace(":",",")
		print (coords)
		splitcoords = coords.split(',')
		print(range(len(splitcoords)))
		for z in range(len(splitcoords)):
			if z==0:
				xstr = splitcoords[z].replace("'","")
				xstr = xstr.replace("(","")
				print (xstr)
				x1 = ast.literal_eval(xstr)
				firstcoord = xstr
				print ("FIRST COORDS IS " + firstcoord + xstr)
				print("x1")
				print (x1)
			if z==1:
				xstr = splitcoords[z].replace("'","")
				xstr = xstr.replace("(","")
				xstr = xstr.replace(")","")
				print (xstr)
				x2 = ast.literal_eval(xstr)
				print("x2")
				print (x2)
			if z==2:
				xstr = splitcoords[z].replace("'","")
				xstr = xstr.replace("(","")
				xstr = xstr.replace(")","")
				print (xstr)
				y1 = ast.literal_eval(xstr)
				print (y1)
			if z==3:
				xstr = splitcoords[z].replace("'","")
				xstr = xstr.replace("(","")
				xstr = xstr.replace(")","")
				print (xstr)
				y2 = ast.literal_eval(xstr)
				print (y2)
			print (str(z))
		coordinatesrec1 = (x1,x2)
		coordinatesrec2 = (y1,y2)
		coordinatesrec = (coordinatesrec1,coordinatesrec2)
		print (coordinatesrec)
		coords = coordinatesrec
		print (coords)
		ch.basic_ack(delivery_tag=method.delivery_tag)
		getcoordinates(xstr)
		if body!="":
			print("clossing receiver")
			connection.close()
			
	connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	countrec = 0
	connstring = str("coordinates_receiver4")
	channel.queue_declare(queue=connstring, durable=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(queue=connstring, on_message_callback=callback)

	channel.start_consuming()

receive()
#getcoordinates() 





	



