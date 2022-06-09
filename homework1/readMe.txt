# TCM-TraplettiVerdiGiudici
  progetto tecnologie cloud e mobile
-  Nel file lambdaFunction è presente il codice principale della funzione lambda (uno dei servizi di AWS comprende appunto le lambda function che consentono di gestire
al meglio qualsiasi chiamata API), che smista in base al tipo di richiesta che riceve. 
- Nel repository funzione_lambda si trova anche il file funzioni.py che raccoglie funzioni utilizzate dalla funzione lambda principale.
- Nella cartella Simulatore è presente il file python simulatore (che utilizza la classe presente nel file funzioni.py). Il simulatore è un piccolo pezzo di software che 
simula l'invio di richieste API al nostro Cloud (per caricare gli XML contenti le gare orienteering)
- nella cartella authorizer è presente il file py contente la funzione lambda per l'autorizzazione per caricare nel DB e nel bucket del nostro cloud nuove gare 
orienteering tramite richieste POST.
