import time 
import os 

from  Model import get_tab, InfoCourse
from  Controller import Control



def main():
    start = time.perf_counter()

    tab = get_tab()
    info_course = InfoCourse(tab)
    times_course = info_course.get_content("div", "course-start-time", "times")
    names_course = info_course.get_content(
        "div", "flex flex-row justify-between", "names course")

    links = info_course.get_all_links()
    number_course = info_course.get_course_number(links)
    status = info_course.get_content("span", "capitalize", "status")

    data_all_api = Control(times_course, number_course, names_course)
    print(data_all_api.get_data(number_course), time.perf_counter() - start)


if os.path.exists(Control.NAME_FILE_DATE): 
    continuer = input("Les donne sont deja enregistrer pour les match d'aujord'hui, voulez vous les re-sevaugarder (y/N): ")
    if continuer == "y":
        os.remove(Control.NAME_FILE_DATE)
        main()
        exit()
    else: 
        exit()
main()


