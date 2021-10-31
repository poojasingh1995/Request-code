import requests
import json
import os

if os.path.isfile("json_data_pushing.json"):
    with open ("json_data_pushing.json","r") as saral_data:
        course_data=json.load(saral_data)
# API calling
else:
    saral_course_api = " http://saral.navgurukul.org/api/courses"     
    saral_url = requests.get(saral_course_api)                        
    # convert into json
    course_data = saral_url.json()
    # pushing data into json file
    with open ("json_data_pushing.json","w") as saral_data:
        json.dump(course_data,saral_data,indent = 4)
    # to find out courses name

serial_no = 0
for index in course_data["availableCourses"]:
    print(serial_no+1 ,index["name"], index["id"])
    serial_no=serial_no+1

# taking user input to print all topic of one specific courses:
Courses_name =int(input("Enter the topic number that you want to learn:- "))
parent_id=course_data["availableCourses"][Courses_name-1]["id"]
print(course_data["availableCourses"][Courses_name-1]["name"])

next_previous_user=input("do you want to go with this code (yes/no):-")
if next_previous_user=="no":
    index=0
    while index<len(course_data["availableCourses"]):
        Courses = (course_data["availableCourses"][index]["name"])
        print(index+1," ",Courses,course_data["availableCourses"][index]["id"])
        index+=1
    available_Courses = int(input("Enter your courses number that you want to learn:-"))
    print(course_data["availableCourses"][available_Courses-1]["name"])
# calling api
if os.path.isfile("parents.json"):
    with open ("parents.json","r") as child_data:
        parent_data=json.load(child_data)
else:
    parents_api = ("http://saral.navgurukul.org/api/courses/"+str(parent_id)+"/exercises")
    # converting parent data into Json
    parent_url = requests.get(parents_api)
    parent_data = parent_url.json()

    # pushing data into json file:
    with open ("parents.json","w") as child_data:
        json.dump(parent_data,child_data,indent=4)

#for printing the details of the specific courses:
serial_no_1=0
for index in parent_data["data"]:
    print("      ",serial_no_1+1,".",index["name"])
    if len(index["childExercises"])>0:
        s_no= 0
        for j in index['childExercises']:
            s_no+=1
            print( "            ",s_no,j['name'])
    else:
        print("             1",index["slug"])
    serial_no_1+=1

topic_no = int(input("Enter the topic number:- "))
serial_no_3= 0
my_list=[]
for l in parent_data['data']:
    serial_no_3+=1
    if topic_no == serial_no_3:
        user_input_3=input("do you want to go previous or next:- ")
        if user_input_3=="p":
            serial_no_1=0
            for i in parent_data["data"]:
                print("      ",serial_no_1+1,".",i["name"])
                if len(i["childExercises"])>0:
                    s_no= 0
                    for j in i['childExercises']:
                        s_no+=1
                        print( "               ",s_no,j['name'])
                else:
                    print("                1",i["slug"])
                serial_no_1+=1
# question_no = int(input("Enter the question number:- "))
    # code for slug having childexercise(more than one question):
             
question = 0
while question < len(parent_data["data"][topic_no-1]["childExercises"]):
    print("     ", question+1 ,parent_data["data"][topic_no-1]["childExercises"][question]["name"])
    slug = (parent_data["data"][topic_no-1]["childExercises"][question]["slug"])
    if os.path.isfile("question.json"):
        with open("question.json","r") as convert_1:
            convert_data=json.load(convert_1)
    else:

        child_exercises_url = ("http://saral.navgurukul.org/api/courses/" +  str(parent_id) +"/exercise/getBySlug?slug=" + slug )
        Data_3 = requests.get(child_exercises_url)
        convert_data = Data_3.json()
        with open("question.json","w") as convert_1:
            json.dump(convert_data,convert_1,indent=4)
        my_list.append(convert_data["content"])
    question+=1
    print(convert_data["content"])

questions_no = int(input("choose the specific questions no :- "))
question=questions_no-1
print(my_list[question])
while questions_no > 0 :
    next_question = input("do you want to go next question or previous question n/p:- ")
    if questions_no == len(my_list):
        print("next page")
    if next_question == "p" :
        if questions_no == 1:
            print("no more questions")
            break
        elif questions_no > 0:
            questions_no = questions_no - 2
            print(my_list[questions_no])
    elif next_question == "n":
        if questions_no < len(my_list):
            index