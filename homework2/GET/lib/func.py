import json, boto3, botocore.exceptions
from xml.dom import minidom
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
            for j in range(len(split)):
                if (split[j].getAttribute('status')!="Missing" and split[j].getAttribute("status")!="Additional"):
                  
                    tempo = split[j].getElementsByTagName("Time")
                 
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
        dic = {}
        a = 1
        for x in lista:
            atleta = {
                "nome" : x[0],
                "cognome" : x[1],
                "tempo": x[2],
                "N_controllo" : x[3]
            }
            dic["atleta" + str(a)]= atleta
            a = a+1
        return dic
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
        
        
        
    
