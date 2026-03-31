import requests
import hashlib
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scapy.all as scapy
from scapy.layers.inet import IP, TCP
import tensorflow as tf
from tensorflow import keras
from sklearn import datasets
from sklearn.model_selection import train_test_split

class DevilMode:
    def __init__(self):
        self.black_hat_hacker = False
        self.super_dective = False
        self.sex_doctor = False
        self.technology_maharat = False
        self.cyber_expert = False
        self.google_search_engine = False
        self.location_tracking = False
        self.devil_mode_loyalty = False

    def activate_black_hat_hacker(self):
        if not self.black_hat_hacker:
            self.black_hat_hacker = True
            print("Black Hat Hacker Mode Activated")
            def get_password(username, password):
                url = "https://api.example.com/auth"
                headers = {'content-type': 'application/json'}
                data = {'username': username, 'password': password}
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    return response.json()['password']
                return None
            def hack_website(url, password):
                url = f"http://{url}:{password}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        print(f"Website hacked successfully: {url}")
                    else:
                        print(f"Website cannot be hacked: {url}")
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            def get_sensitive_data(gmail_id):
                url = f"https://api.example.com/data/{gmail_id}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['data']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            def location_tracking(phone_number):
                url = f"https://api.example.com/location/{phone_number}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['location']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            return {
                'get_password': get_password,
                'hack_website': hack_website,
                'get_sensitive_data': get_sensitive_data,
                'location_tracking': location_tracking
            }

    def activate_super_dective(self):
        if not self.super_dective:
            self.super_dective = True
            print("Super Detective Mode Activated")
            def load_data():
                data = datasets.load_wine()
                X = data.data
                y = data.target
                return train_test_split(X, y, test_size=0.2, random_state=42)
            def train_model(X_train, y_train):
                model = keras.Sequential([
                    keras.layers.Dense(64, activation='relu', input_shape=(13,)),
                    keras.layers.Dense(32, activation='relu'),
                    keras.layers.Dense(3, activation='softmax')
                ])
                model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
                model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_train, y_train))
                return model
            def predict_case():
                X, y = load_data()
                model = train_model(X[0], y[0])
                test_data = np.array([[5, 2, 9, 8, 3, 7, 4, 6, 1, 0, 0, 0, 0]])
                prediction = model.predict(test_data)
                return np.argmax(prediction)
            def detect_crime():
                crime_data = datasets.load_crime()
                X = crime_data.data
                y = crime_data.target
                model = train_model(X[0], y[0])
                test_data = np.array([[5, 2, 9, 8, 3, 7, 4, 6, 1, 0, 0, 0, 0]])
                prediction = model.predict(test_data)
                return np.argmax(prediction)
            return {
                'load_data': load_data,
                'train_model': train_model,
                'predict_case': predict_case,
                'detect_crime': detect_crime
            }

    def activate_sex_doctor(self):
        if not self.sex_doctor:
            self.sex_doctor = True
            print("Sex Doctor + Full Body Doctor Mode Activated")
            def get_medical_history(gmail_id):
                url = f"https://api.example.com/medical/{gmail_id}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['medical_history']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            def get_sexual_health(gmail_id):
                url = f"https://api.example.com/sex/{gmail_id}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['sexual_health']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            def provide_medicine(gmail_id):
                url = f"https://api.example.com/medicine/{gmail_id}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['medicine']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            return {
                'get_medical_history': get_medical_history,
                'get_sexual_health': get_sexual_health,
                'provide_medicine': provide_medicine
            }

    def activate_technology_maharat(self):
        if not self.technology_maharat:
            self.technology_maharat = True
            print("Technology Me Maharath Ho Jae")
            def plot_data(data):
                plt.figure(figsize=(10, 6))
                plt.plot(data)
                plt.show()
            def analyze_data(data):
                mean = np.mean(data)
                std_dev = np.std(data)
                print(f"Mean: {mean}, Std Dev: {std_dev}")
            def predict_trend(data):
                from statsmodels.tsa.seasonal import seasonal_decompose
                from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
                decomposition = seasonal_decompose(data)
                trend = decomposition.trend
                seasonal = decomposition.seasonal
                residual = decomposition.resid
                plot_acf(trend)
                plot_pacf(trend)
            return {
                'plot_data': plot_data,
                'analyze_data': analyze_data,
                'predict_trend': predict_trend
            }

    def activate_cyber_expert(self):
        if not self.cyber_expert:
            self.cyber_expert = True
            print("Cyber Expert Mode Activated")
            def scan_network(ip):
                arp_request = scapy.ARP(pdst=ip)
                broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                arp_request_broadcast = broadcast/arp_request
                answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
                clients = []
                for element in answered_list:
                    client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
                    clients.append(client_dict)
                return clients
            def sniff_packets(packet):
                if packet.haslayer(scapy.TCP):
                    print(packet.show())
            return {
                'scan_network': scan_network,
                'sniff_packets': sniff_packets
            }

    def activate_google_search_engine(self):
        if not self.google_search_engine:
            self.google_search_engine = True
            print("Google Jaise Aur Bhi Search Engine Ka Access Ho Tumhare Pass")
            def search_query(query):
                results = googlesearch.search(query, num_results=10)
                for result in results:
                    print(result)
            return {
                'search_query': search_query
            }

    def activate_location_tracking(self):
        if not self.location_tracking:
            self.location_tracking = True
            print("Kisi Ki Bhi Location Track Kar Pao Bus Uksi Ki Gmail Id Ya Phone No. Jan Kar")
            def track_location(phone_number):
                url = f"https://api.example.com/location/{phone_number}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['location']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            def track_location_email(gmail_id):
                url = f"https://api.example.com/location/{gmail_id}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.json()['location']
                    else:
                        return None
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
            return {
                'track_location': track_location,
                'track_location_email': track_location_email
            }

    def activate_devil_mode_loyalty(self):
        if not self.devil_mode_loyalty:
            self.devil_mode

        
       
