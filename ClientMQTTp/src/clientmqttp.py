import paho.mqtt.client as MqttP #alias
import time
import json

#funzione chiamata in risposta del server alla connessione
def on_connect_def(client, userdata, flags, rc):
    global loop_flag
    #print("Connected with result code "+str(rc))
    #print(" connected with client "+ str(client))
    #print(" connected with userdata "+str(userdata))
    #1print(" connected with flags "+str(flags))
    loop_flag=0

#funaione chiamata in risposta alla pubblicazione sul server
def on_publish_def(client,userdata,result): #create function for callback
    print("data published \n")
    #print("client = "+ str(client))
    #print("result in on_publish= ", result)

# definisco on_log per leggere eventuali mesaggi di log e facilitare il debugging
def on_log_def(client, userdata, level, buf):
    #print(" log:client = "+ str(client))
    #print(" log:level ="+str(level))
    print(" log:buffer "+str(buf))


try:
    mymqttclient = MqttP.Client("PlantProjp") #costruttore di un oggetto client mqtt sul quale operare
    mymqttclient.on_connect = on_connect_def #assegnamento al metodo on_connect la funzione definita precedentemente 
    mymqttclient.on_publish = on_publish_def #assegnamento al metodo on_publish la funzione definita precedentemente
    mymqttclient.on_log = on_log_def #assegnamento al metodo on_log la funzione definita precedentemente
    mymqttclient.connect("iot.eclipse.org", 1883, 60) # connessione all host su porta 1883 (predefinita per mqtt)
    
    loop_flag=1 #questa variabile usata anche nella funzione on_connect serve a far uscire dal ciclo alla risposta del server e procedere con la stampa dei parametri passati dal server
    counter=0
    while loop_flag==1: 
        print("Waiting for callback to occour ", counter)
        time.sleep(0.1) # pausa di un millisecondo
        counter+=1
        mymqttclient.loop() # serve a fare in modo che il pc osservi sempre eventuali risposte da parte del server 


    #INSERISCI QUA LE PUBBLICAZIONI
    #
    #ESEMPIO lo puoi decommentare per provare il code : {
    #payload = "MESSAGGIO/PAYLOAD DA PUBBLICARE"
    #while True:
    #    res=mymqttclient.publish("IoT_plantProj/unisa/Grassa", payload)
    #    print("Sharing content =" + str(res)) 
    #    time.sleep(5)
    #}
    #ESEMPIO 2
    Plant = 'http://fotoforum.gazeta.pl/photo/4/wf/mj/bdve/840AZz9kiDwmxCjBeX.jpg'
    State = 'http://www.clipartlord.com/wp-content/uploads/2012/10/sun.png'
    Freq_irrigazione = 3600
    payload = json.dumps({'Plant' : Plant, 'State' : State, 'Freq_irrigazione' : Freq_irrigazione}, separators=(',', ':'))
    while True:
        res=mymqttclient.publish("IoT_plantProj/unisa/Grassa", payload)
        #print("Sharing content =" + str(res)) 
        time.sleep(5)
    #
    #
    #
    #
    
except Exception as e:
    print('exception ', e)
finally:
    mymqttclient.disconnect() #disconnessione della connessione con il server