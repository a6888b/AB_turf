import time 

from  Model import get_tab, InfoCourse
from  Controller import Control


start = time.perf_counter()

tab = get_tab()
info_course = InfoCourse(tab)

times_course = info_course.get_content("div", "course-start-time", "times")
links = info_course.get_all_links()
number_course = info_course.get_course_number(links)
status = info_course.get_content("span", "capitalize", "status")
names_course = info_course.get_content(
    "div", "flex flex-row justify-between", "names course")

data_all_api = Control(times_course, number_course, names_course)
data_all_api.get_data(number_course)
print(time.perf_counter() - start)