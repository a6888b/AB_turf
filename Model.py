import datetime as date 

import requests
import bs4 

URL = "https://www.pmu.fr/point-de-vente/"
URL_API = "https://online.turfinfo.api.pmu.fr/rest/client/62/programme/"
DATE = date.datetime.now()
DATE_URL = DATE.strftime("%d%m20%y")

def get_tab():  # renvoie lee tableaux avec tout les match present
    r = requests.get(URL)
    if r.ok:
        soup = bs4.BeautifulSoup(r.content, "lxml")
        return[ tab for tab in soup.find_all("div", class_="css-1f5cnfe e91l0ui0")] # css-r7epeu e91l0ui0



class InfoCourse:
    def __init__(self, tab: list):
        self.tab = tab

    # methode pour recuperer les donne voulus
    def get_content(self, balise_html: str, class_html: str, for_):
        elements = []
        for course in self.tab:
            for element in course.find_all(balise_html, class_=class_html):
                match for_:
                    case "times":
                        elements.append(element.span.string)
                    case "names course":
                        elements.append(element.h3.text)
                    case "status":
                        elements.append(element.string)
        return elements

    # recuper le nombre de la course (R1/C3)
    def get_course_number(self, links: list):
        number_courses = []
        for link in links:
            number_courses.append("".join(link.split("/")[-3:]))
        return number_courses


    def get_all_links(self):  # recupere les lien du tableaux pour les traiter
        links = []
        for course in self.tab:
            for link in course.find_all("a"):
                links.append(link["href"])
        return links


class Pronostic:
    def __init__(self, data: dict):
        self.data = data 

    def get_number_cours(self): 
        return self.data["participants"]["nombre course"]

    def get_number_victory(self): 
        return self.data["participants"]["nombre victoire"]
    
    def get_place(self): 
        return self.data["participants"]["nombre placée"]

    def get_place_secondary(self): 
        return self.data["participants"]["nombre placée second"]

    def get_place_three(self): 
        return self.data["participants"]["nombre placée troisieme"]
    
    def get_all_detail(self):
        return self.get_number_cours, self.get_number_victory, self.get_place, self.get_place_secondary, self.get_place_three

    def pourcent_win(self):
        for index, _ in enumerate(self.get_number_cours()): 
            try: 
                pourcent_place = 100*(self.get_place()[index] + self.get_place_secondary()[index]+ self.get_place_three()[index])/self.get_number_cours()[index]
                pourcent_victory = 100*self.get_number_victory()[index]/self.get_number_cours()[index]
            except ZeroDivisionError: 
                pourcent_place = 0 
                pourcent_victory = 0

        self.data["participants"]["chance_gagner_place"].append(pourcent_place)
        self.data["participants"]["chance de gagner"].append(pourcent_victory)
        return self.data