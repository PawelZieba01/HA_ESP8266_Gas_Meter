import json
import network
import usocket as socket
from uselect import select
from time import sleep

class ESP_uNetwork:
    
    def __init__(self, config_file_dir = ""):
        #jeżeli istnieje plik konfiguracyjny to pobierz dane konfiguracyjne sieci
        if(config_file_dir):

            print("Opening config file: 'conf.json'")

            f = open(config_file_dir, "r")
            config_json = f.read()                          # pobranie danych konfiguracyjnych z pliku config.json
            config_dict = json.loads(config_json)           # zdekodowanie danych json - zamiana na dictionary
            f.close()
            del config_json

            #konfiguracja sieci z pliku
            self.static_ip = config_dict["static_ip"]
            self.mask_ip = config_dict["mask_ip"]
            self.gate_ip = config_dict["gate_ip"]
            self.dns_ip = config_dict["dns_ip"]
            self.ssid = config_dict["ssid"]
            self.password = config_dict["password"]

            del config_dict
            print("Config from file saved..")


    #ręczna konfiguracja sieci
    def set_net_config(self, ssid, password, static_ip, gate_ip, mask_ip="255.255.255.0", dns_ip="8.8.8.8"):
        self.ssid = ssid
        self.password = password
        self.static_ip = static_ip
        self.gate_ip = gate_ip
        self.mask_ip = mask_ip
        self.dns_ip = dns_ip


    #połącz z punktem dostępowym
    def connect_to_AP(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.sta_if.active(True)
        if not self.sta_if.isconnected():

            print("Connecting with " + self.ssid +"...")

            self.sta_if.connect(self.ssid, self.password)
            while not self.sta_if.isconnected():
                print(".")
                sleep(0.2)
        self.sta_if.ifconfig((self.static_ip, self.mask_ip, self.gate_ip, self.dns_ip))

        print("WLAN config:", self.sta_if.ifconfig())



    #uruchomienie punktu dostępowego
    def start_AP(self, ssid, password):
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, password=password)

        while ap.active() == False:
            pass

        print('AP activated')
        print(ap.ifconfig())



    #nasłuchiwanie zapytań http
    def set_server_listening(self, addr="", port=80):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if(not addr):
            addr = self.static_ip

        self.s.bind((addr, port))
        self.s.listen(1)
        print("Listening with " + str(addr) + " at port " + str(port))
        

    #funkcja odbierająca połączenia z timeoutem
    def get_request(self, handler_fun, timeout=1):
        r, w, err = select((self.s,), (), (), timeout)
        if r:
                try:
                    conn, addr = self.s.accept()
                    handler_fun(conn, addr)
                except OSError as e:
                    pass

    # Funkcja zwracająca ststus połączenia z AP
    def check_connection_with_AP(self):
        return self.sta_if.isconnected()
