import xml.etree.ElementTree as et
import io
import csv
import math

doc = et.parse("Άγιος Γεώργιος.kml")  # Change with the filepath to your kml file

R = 6371  # Earth radius
rawdata = []
data = []

nmsp = '{http://www.opengis.net/kml/2.2}'

# Extracts the data:
#   a) placemarker name
#   b) coordinates
#from the kml file and appends them in rawdata array
def extractdata():
    for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):
        marker = pm.find('{0}name'.format(nmsp)).text

        for ls in pm.iterfind('.//{0}coordinates'.format(nmsp)):
            coordinates = ls.text.strip().replace('\n','')

            rawdata.append({"marker": marker, "coordinates": coordinates})


# Writes a csv file named rawcoordinates.csv with the latitude, longitude coordinates
def writerawdatacsv():
    try:
        with io.open('rawcoordinates.csv', mode='a', newline='') as csvw:
            write = csv.writer(csvw)
            write.writerow(['Marker', 'Latitude', 'Longitude', 'Coordinate 3'])
            for entry in rawdata:
                name = entry['marker']
                position = entry['coordinates'].split(",")
                write.writerow([name,position[0],position[1],position[2]])
        print('Your data csv with latitude, longitude coordinates is ready!')
    except csv.Error as e:
        print(e)


# Transforms latitude, longitude coordinates to x, y, z coordinates
def longlattoxy():
    for entry in rawdata:
        name = entry['marker']
        position = entry['coordinates'].split(",")

        x = R * math.cos(float(position[0])) * math.cos(float(position[1]))
        y = R * math.cos(float(position[0])) * math.sin(float(position[1]))
        z = R * math.sin(float(position[0]))

        data.append({"marker": name, "x": x, "y": y, "z": z})


# Writes a csv file named coordinates.csv with the x, y, z coordinates
def writedatacsv():
    try:
        with io.open('coordinates.csv', mode='a', newline='') as csvw:
            write = csv.writer(csvw)
            write.writerow(['Marker', 'x', 'y', 'z'])
            for entry in data:
                name = entry['marker']
                x = entry['x']
                y = entry['y']
                z = entry['z']
                write.writerow([name,x,y,z])
        print('Your data csv with x,y,z coordinates is ready!')
    except csv.Error as e:
        print(e)


extractdata()
longlattoxy()
writerawdatacsv()
writedatacsv()

# print(rawdata)
# print(data)