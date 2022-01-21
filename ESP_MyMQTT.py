from umqtt_simple import MQTTClient
import json

class ESP_MyMQTT:
    def __init__(self, config_file_dir = ""):
        # Jeżeli istnieje plik konfiguracyjny to pobierz dane konfiguracyjne sieci
        if (config_file_dir):
            print("Opening config file: 'conf.json'")

            f = open(config_file_dir, "r")
            config_json = f.read()                      # Pobranie danych konfiguracyjnych z pliku config.json
            config_dict = json.loads(config_json)       # Pdekodowanie danych json - zamiana na dictionary
            f.close()
            del config_json

            # Zmienne konfiguracyjne dla clienta mqtt
            self.client_id = config_dict["client_id"]
            self.mqtt_server = config_dict["mqtt_server"]
            self.mqtt_port = int(config_dict["mqtt_port"])
            self.mqtt_user = config_dict["mqtt_user"]
            self.mqtt_pass = config_dict["mqtt_pass"]

            # Obiekt clienta mqtt
            self.client = MQTTClient(self.client_id, self.mqtt_server, self.mqtt_port, self.mqtt_user, self.mqtt_pass)

            del config_dict


    # Funkcja łącząca się z brokerem i subskrybująca tematy
    def connect_and_subscribe(self):
        # self.client.set_callback(self.__mqtt_handler)     # Odkomentować jeśli są jakieś tematy do subskrybowania

        self.client.connect()

        # Wysłanie informacji o dostępności urządzenia
        # self.client.publish(self.topic_pub_availability, "online")


        # ---------- subskrybcja tematów mqtt -----------
        # Tutaj można podać tematy, które mają zostać subskrybowane

        # self.client.subscribe(self.topic_sub_state)

        # -----------------------------------------------

        print('Connected to MQTT broker.')
        return self.client


    # Funkcja pobierająca informacje z serwera i wykonująca polecenia z __mqtt_handler()
    def get_mqtt_data(self):
        self.client.check_msg()


    # Funkcja wysyłająca dane do pojedyńczego tematu
    def send_state(self, topic, value):
        self.client.publish(topic, value)


    # Funkcja subskrybująca pojedyńczy temat
    def subscribe_topic(self, topic):
        self.client.subscribe(topic)

    # Funkcja wywoływana przy zmianie stanu w subskrybowanym temacie
    def __mqtt_handler(self, topic, msg):
        print((topic, msg))