from msilib.schema import Class
from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.dom.minidom import Node
tempoX = 1100


class func: 
    def writer(self, doc):
        xmldoc = minidom.parse(doc)
        
        NmeGara = xmldoc.getElementsByTagName('Name')[0].firstChild.data
        start = xmldoc.getElementsByTagName('StartTime')
        date = start[0].getElementsByTagName('Date')[0].firstChild.data
        time = start[0].getElementsByTagName('Time')[0].firstChild.data
        gare=  xmldoc.getElementsByTagName('ClassResult')
        data = ET.Element('ResultList')
        #Elementi di ResultList
        event = ET.SubElement(data,'Event')
        #Elementi di Event
        ET.SubElement(event,'Name').text = NmeGara
        
        #StartTime
        ET.SubElement(event,'Date').text = date
        ET.SubElement(event,'StartTime').text=time
        #Elementi di ClassResult
        for i in range(len(gare)):
            ClassResult = ET.SubElement(data,'ClassResult')
            classi = ET.SubElement(ClassResult, 'Class')
            ET.SubElement(classi,'Name').text =xmldoc.getElementsByTagName('Name')[1].firstChild.data 
            Result = ET.SubElement(ClassResult, 'Result')
            list = self.simulator(xmldoc)
            for x in range(len(list)):
                if list[x][4]== i+1 :
                    person = ET.SubElement(Result, 'Person')
                    ET.SubElement(person,'Given').text = list[x][0]
                    ET.SubElement(person,'Family').text = list[x][1]
                    ET.SubElement(person,'Time').text = list[x][2]
                    ET.SubElement(person,'Control').text = str(list[x][3])
                else:
                    break
                    
        tree = ET.ElementTree(data).write("risultatoParziale.xml",encoding='utf-8', xml_declaration=True)
        
        return
    def simulator(self, xmldoc):
        atleti=[]
        gare= xmldoc.getElementsByTagName('ClassResult')

        for i in range(len(gare)):
            xmldoc = gare[i]
            risultati=[]
            nomi = xmldoc.getElementsByTagName("Given")
            cognomi = xmldoc.getElementsByTagName("Family")
            risultati  = xmldoc.getElementsByTagName("Result")

            tempi = []
            waypoint =[]
            for k in range(len(risultati)):
                if risultati[k].getElementsByTagName('Status')[0].firstChild.data=='DidNotStart':
                    tempi.append(tempoX*5)
                    waypoint.append(0)
                    break
                tempo =  risultati[k].getElementsByTagName("Time")
                for r in range(1,len(tempo)):
                    if int(tempo[r].firstChild.data)==tempoX:
                        tempi.append(tempo[r].firstChild.data)
                        waypoint.append(r)
                        break
                    elif int(tempo[r].firstChild.data) > tempoX:
                        tempi.append(tempo[r-1].firstChild.data) 
                        waypoint.append(r-1)
                        break
            for n in range (len(nomi)):
                nome = nomi[n].firstChild.data
                cognome = cognomi[n].firstChild.data
                tempo = tempi[n]
                atleti.append([nome,cognome,tempo,waypoint[n],i+1]) 
            
        
        atleti = sorted(atleti, key = lambda x: (x[4],-int(x[3]),x[2])) 
        return atleti 