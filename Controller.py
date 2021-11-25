import json 
import Model

import requests

class Control:
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


    def save_data(self, data: dict):
        with open(f"result_scrap.json", "a", encoding="utf-8") as f_data:
            json.dump(data, f_data, indent=1, ensure_ascii=False)


    def get_data(self, course: list[str]):  # recupere les donne de l'api
        for index, number in enumerate(course):
            data = {"heure": None, "number": None, "nom_course": None, "participants":
                    {"nom": [], "age": [], "numPmu": [], "nombre course": [], "nombre placée": [], "nombre placée second": [], "nombre placée troisieme": [], "nombre victoire": [], "chance de gagner": [], "chance_gagner_place":[]}}
            url = f"{Model.URL_API+Model.DATE_URL}/{number.upper()[:-2]}/{number.upper()[-2:]}/participants?specialisation=OFFLINE"
            data["heure"] = self.time[index]
            data["number"] = number
            data["nom_course"] = self.name_run[index]

            r = requests.get(url)

            if r.ok:
                result_json = r.json()["participants"]

                for element in result_json:
                    data["participants"]["nom"].append(element["nom"])
                    data["participants"]["age"].append(element["age"])
                    data["participants"]["numPmu"].append(element["numPmu"])
                    data["participants"]["nombre course"].append(
                        element["nombreCourses"])
                    data["participants"]["nombre placée"].append(
                        element["nombrePlaces"])
                    data["participants"]["nombre placée second"].append(
                        element["nombrePlacesSecond"])
                    data["participants"]["nombre placée troisieme"].append(
                        element["nombrePlacesTroisieme"])
                    data["participants"]["nombre victoire"].append(
                        element["nombreVictoires"])
                    prono = Model.Pronostic(data)
                    data_with_prono = prono.pourcent_win() #retorune le nouveuax dictionnaire avec les pourcenatage de gagne est de placement pour cahque joueur  
                self.save_data(data_with_prono)
        return "Données sauvegarder"