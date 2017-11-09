import paho.mqtt.client as MqttP
import time
import json
from io import StringIO

def on_connect_def(client, userdata, flags, rc):
    global loop_flag
#    print("Connected with result code "+str(rc))
#    print(" connected with client "+ str(client))
#    print(" connected with userdata "+str(userdata))
#    print(" connected with flags "+str(flags))
    loop_flag=0

# chiamato in risposta ad una pubblicazione 
def on_message_def(client, userdata, msg):
    io = StringIO(msg.payload.decode('utf-8'))
    j = json.load(io)
    print("Received: ",j['Plant'],"-",j['State'],"-",j['Freq_irrigazione'])


def on_log_def(client, userdata, level, buf):
    print("Log called")
#    print(" log:client = "+ str(client))
#    print(" log:level ="+str(level))
#    print(" log:buffer "+str(buf))

def on_subscribe_def(client, userdata, msg, qos):
    print("on subscribe called")
#    print("on_sub: client ="+str(client))
#    print("on_sub: usrdata ="+str(userdata))
#    print("on_sub: msg ="+str(msg))
#    print("on_sub: qos level ="+str(qos))


try:
    mymqttclient = MqttP.Client("PlantProjs") #costruttore di un oggetto client mqtt sul quale operare
    mymqttclient.on_subscribe = on_subscribe_def #assegnamento al metodo on_subscribe la funzione definita precedentemente 
    mymqttclient.on_connect = on_connect_def #assegnamento al metodo on_connect la funzione definita precedentemente
    mymqttclient.on_message = on_message_def #assegnamento al metodo on_message
    mymqttclient.on_log = on_log_def #assegnamento al metodo on_log la funzione definita precedentemente
    mymqttclient.connect("iot.eclipse.org", 1883, 60) # connessione all host su porta 1883 (predefinita per mqtt)
    
    loop_flag=1 #questa variabile usata anche nella funzione on_connect serve a far uscire dal ciclo alla risposta del server e procedere con la stampa dei parametri passati dal server
    counter=0
    while loop_flag==1: 
        print("Waiting for callback to occour ", counter)
        time.sleep(0.1) # pausa di un millisecondo
        counter+=1
        mymqttclient.loop() # serve a fare in modo che il pc osservi sempre eventuali risposte da parte del server 

    #INSERISCI QUA LE SOTTOISCRIZIONI
    #
    #ESEMPIO lo puoi decommentare per provare il code : {
    mymqttclient.subscribe("IoT_plantProj/unisa/grasse")
    #
    #
    #
    #
    
    
    while True: #ascolto 
        mymqttclient.loop()

except Exception as e:
    print('exception ', e)
finally:
    mymqttclient.unsubscribe("IoT_plantProj/unisa/Grassa")
    mymqttclient.disconnect()


    
    
    
    