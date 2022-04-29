import uuid
import json
import boto3
from datetime import date
from xml.dom import minidom
bucket_name= "xmlverdi" 
tempoX = 1100
class simulator:
        
    def simulatore(self,file):
        encoded_string = file.encode("utf-8")
        
        atleti=[]
        global bucket_name,tempoX
        xmldoc = minidom.parseString(encoded_string)
        gare=  xmldoc.getElementsByTagName('ClassResult')
        xmldoc = gare[0]
        risultati=[]
        nomi = xmldoc.getElementsByTagName("Given")
        cognomi = xmldoc.getElementsByTagName("Family")
        risultati  = xmldoc.getElementsByTagName("Result")
        
        
        tempi = []
        waypoint =[]
        for k in range(len(risultati)): 
            tempo =  risultati[k].getElementsByTagName("Time")
            for r in range(1,len(tempo)):
                if int(tempo[r].firstChild.data)==tempoX:
                    tempi.append(tempo[r]) 
                    waypoint.append(r)
                    break
                elif int(tempo[r].firstChild.data) > tempoX:
                    tempi.append(tempo[r-1]) 
                    waypoint.append(r-1)
                    break
        for n in range (len(nomi)):
            chiave = "atleta"+ str(n+1)
            nome = nomi[n].firstChild.data
            cognome = cognomi[n].firstChild.data
            
            if n>=len(tempi):
                tempo = 5000
            else : 
                tempo = tempi[n].firstChild.data
            
            atleti.append([nome,cognome,tempo,waypoint[n]]) 
            
            
        
        
        atleti = sorted(atleti, key = lambda x: (-int(x[3]),x[2])) 
       
        return atleti 
