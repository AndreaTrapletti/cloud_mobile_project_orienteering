import json, boto3, botocore.exceptions
from xml.dom import minidom
import re
class func :
    def simulator(self,xmldoc):
        atleti=[]
        risultati=[]
        nomi = xmldoc.getElementsByTagName("Given")
        cognomi = xmldoc.getElementsByTagName("Family")
        risultati  = xmldoc.getElementsByTagName("Result")

        tempi = []
        waypoint =[]
        temp = []
        
        for k in range(len(risultati)):
            if risultati[k].getElementsByTagName('Status')[0].firstChild.data=='DidNotStart':
                tempi.append(5000)
                waypoint.append(0)
                continue 
            split =  risultati[k].getElementsByTagName("SplitTime")
            print(k)
            for j in range(len(split)):
                if (split[j].getAttribute('status')!="Missing" and split[j].getAttribute("status")!="Additional"):
                   
                    tempo = split[j].getElementsByTagName("Time")
                    
                    if len(tempo)==0:  #[0].firstChild.data == 0:
                        temp.append(0)
                    else:
                        temp.append(tempo[0].firstChild.data)
                    
            tempi.append(self.massimo(temp))
            waypoint.append(len(temp))
            temp = []
        for n in range (len(nomi)):
            nome = nomi[n].firstChild.data
            cognome = cognomi[n].firstChild.data
            tempo = tempi[n]
            atleti.append([nome,cognome,tempo,waypoint[n]]) 
            
        atleti = sorted(atleti, key = lambda x: (-int(x[3]),x[2]))  
        return self.dizionario(atleti)
        
    def massimo(self,lista):
        a = 0 
        for x in lista : 
            if int(x) > a:
                a = int(x)
        return a
        
    def dizionario(self, lista): 
        y = '{ "atleti": ['
        for x in lista:
            nome = str(x[0])
            nome = re.sub('[\']', '', nome)
            
            cognome = str(x[1])
            cognome = re.sub('[\']', '', cognome)
            
            atleta = {
                "nome": nome,
                "cognome": cognome,
                "tempo" : x[2],
                "N_controllo" : x[3]
            }
            
            
            y = y + str(atleta) + ","
        y = y + "]}"
        print(y)
        
        y = y.rsplit(',', 1)
        y = y[0] + y[1]
        y = re.sub('[\']', '\"', y)
        return y
    def scrittura(self, cres, id):
        doc = minidom.Document()
        root = doc.createElement("ResultList")
        doc.appendChild(root)
        tempChild = doc.createElement(cres)
        root.appendChild(tempChild)
        # Write Text
        nodeText = doc.createTextNode(str(cres))
        tempChild.appendChild(nodeText)
        return doc
        filename = str(id) +"result.xml"
        doc.writexml( open("caso.xml", 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
 
        doc.unlink()
        return    
    
    def trasforma_in_ore(self, secondi):
        tempo = ""
        minuti = int(secondi/60)
        secondi = int(secondi%60)
        if secondi<10:
            secondi = str(0) + str(secondi)
        tempo = str(minuti) + " : " + str(secondi)
        return tempo
        
        
    
