import json 
import Model
import os 
import datetime

import requests


date_today = str(datetime.date.today())


class Control:
    NAME_FILE_DATE = f"result_scrap_{date_today}.json"
    def __init__(self, time: list, number: list, name_run: list):
        self.time = time
        self.number = number
        self.name_run = name_run
        self.data = {}
        self.noms = []
        self.ages = []
        self.num_pmus = []
        self.nombre_courses = []
        self.nombre_places = []
        self.nombre_place_deuxiemes = []
        self.nombre_place_troisiemes = []
        self.nombre_victoires = []


    def save_data(self, data: list):
        with open(self.NAME_FILE_DATE, "a") as f_data:
            json.dump(data, f_data, indent=1, ensure_ascii=False)


    def get_data(self, course: list[str]):  # recupere les donne de l'api
        data = []
        for index, number in enumerate(course):
            data.append({"heure": None, "number": None, "nom_course": None, "participants":
                    {"nom": [], "age": [], "numPmu": [], "nombre course": [], "nombre placée": [], "nombre placée second": [], "nombre placée troisieme": [], "nombre victoire": [], "chance de gagner": [], "chance_gagner_place":[]}})
                    
            url = f"{Model.URL_API+Model.DATE_URL}/{number.upper()[:-2]}/{number.upper()[-2:]}/participants?specialisation=OFFLINE"
            data[index]["heure"] = self.time[index]
            data[index]["number"] = number
            data[index]["nom_course"] = self.name_run[index]

            r = requests.get(url)

            if r.ok:
                result_json = r.json()["participants"]
                for element in result_json:
                    data[index]["participants"]["nom"].append(element["nom"])
                    data[index]["participants"]["age"].append(element["age"])
                    data[index]["participants"]["numPmu"].append(element["numPmu"])
                    data[index]["participants"]["nombre course"].append(element["nombreCourses"])
                    data[index]["participants"]["nombre placée"].append(element["nombrePlaces"])
                    data[index]["participants"]["nombre placée second"].append(element["nombrePlacesSecond"])
                    data[index]["participants"]["nombre placée troisieme"].append(element["nombrePlacesTroisieme"])
                    data[index]["participants"]["nombre victoire"].append(element["nombreVictoires"])

                    prono = Model.Pronostic(data, index)
                    data_with_prono = prono.pourcent_win() #retorune le nouveuax dictionnaire avec les pourcenatage de gagne est de placement pour cahque joueur  
            prono.more_chance_win()
        # self.save_data(data_with_prono)
        return "Données sauvegarder" 

