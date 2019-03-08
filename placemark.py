import pathlib
import xml.dom.minidom
import sys
from os import listdir, getcwd
from os.path import join, isfile
import csv
from math import radians, cos, sin, asin, sqrt


root = sys.argv[1]
csv_path = root + '/CSV/'
kml2D_path = root + '/KML2D/'

def degreeConverter(decdegrees):
    decdegrees = float(decdegrees)
    degrees = int(decdegrees)
    temp = 60 * (decdegrees - degrees)
    minutes = int(temp)
    seconds =round( 60 * (temp - minutes),2)
    return str(degrees)+ str(minutes)+ str(seconds)


def createKML(csvReader, fileName):
    # This constructs the KML document from the CSV file.
    kmlDoc = xml.dom.minidom.Document()

    kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
    kmlElement.setAttribute('xmlns','http://earth.google.com/kml/2.2')
    kmlElement = kmlDoc.appendChild(kmlElement)

    documentElement = kmlDoc.createElement('Document')
    kmlElement.appendChild(documentElement)

    styleElement = kmlDoc.createElement('Style')
    documentElement.appendChild(styleElement)
    styleElement.setAttribute('id', 'randomColorIcon')
    
    color = kmlDoc.createElement('color')
    colorMode = kmlDoc.createElement('colorMode')
    scale = kmlDoc.createElement('scale')
    Icon = kmlDoc.createElement('Icon')
    href = kmlDoc.createElement('href')
    altitudeMode = kmlDoc.createElement('alttudeMode')

    styleElement.appendChild(color)
    styleElement.appendChild(colorMode)
    styleElement.appendChild(scale)
    styleElement.appendChild(Icon)
    Icon.appendChild(href)
    Icon.appendChild(altitudeMode)

    color.appendChild(kmlDoc.createTextNode('ff00ff00'))
    colorMode.appendChild(kmlDoc.createTextNode('random'))
    scale.appendChild(kmlDoc.createTextNode('5'))
    href.appendChild(kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/pal3/icon21.png'))
    altitudeMode.appendChild(kmlDoc.createTextNode('absolute'))

    next(csvReader)

    for row in csvReader:
        placemarkElement = createPlacemark(kmlDoc, row)
        documentElement.appendChild(placemarkElement)
    kmlFile = open(fileName, 'wb')
    kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

    return kmlFile

def createPlacemark(kmlDoc, row):
    placemark = kmlDoc.createElement('Placemark')
    name = kmlDoc.createElement('name')
    description = kmlDoc.createElement('description')
    point = kmlDoc.createElement('Point')
    coordinate =kmlDoc.createElement('coordinates')
    styleUrl = kmlDoc.createElement('styleUrl')
    extrude = kmlDoc.createElement('extrude')
    

    placemark.appendChild(name)
    placemark.appendChild(description)
    placemark.appendChild(point)
    point.appendChild(coordinate)
    placemark.appendChild(styleUrl)
    placemark.appendChild(extrude)

    des_string = '<div>' + 'Position: ' + degreeConverter(row[2])+'N ' + degreeConverter(row[3]) +'E' + '</div>' + '<div>' + row[6]  + '</div>' + '<div>' + 'Runway: ' + row[0]  + '</div>'  +'<div>' + 'Elevation (in ft): ' + row[4]  + '</div>' +'<div>' + 'Marking: ' + row[5]  + '</div>' 
    name.appendChild(kmlDoc.createTextNode(row[6]))
    description.appendChild(kmlDoc.createTextNode(des_string))
    coordinate.appendChild(kmlDoc.createTextNode(row[3] + ',' + row[2] + ',' + row[4]))
    styleUrl.appendChild(kmlDoc.createTextNode('#randomColorIcon'))
    extrude.appendChild(kmlDoc.createTextNode('1'))
    
    return placemark



def main():
    files = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]
    pathlib.Path(kml2D_path).mkdir(parents=True, exist_ok=True) 
    for csv_file in files:
        path = csv_path + '/' + csv_file
        kmlValue = csv_file[:-4]
        kmlpath = kml2D_path +'/' + kmlValue
        csvreader = csv.reader(open(path), delimiter = ',')
        kml = createKML(csvreader, kmlpath + '.KML')

if __name__ == '__main__':
  main()
