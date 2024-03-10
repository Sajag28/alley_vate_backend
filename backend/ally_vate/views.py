from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import os 
import random
from .openai import call_openai_api
from django.views.decorators.http import require_http_methods
from .email import send_email
# Create your views here.

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
question_list = ['''Which topics/concepts were most challenging?''',
                 '''Did teaching methods/pace hinder your learning? Suggestions?''',
                 '''Any gaps in course content that need addressing?''',
                 '''Effective time management/study techniques to share?''',
                 '''Barriers to accessing academic support services?''',
                 '''To what extent did this course meet your expectations in terms of learning objectives and content coverage?''',
                 '''Conversely, are there any areas where you feel the course could be strengthened to enhance student learning?''',
                 '''Did the assigned readings (textbook chapters, articles) effectively complement the lectures and support your understanding of the material?''',
                 '''How would you rate the clarity and effectiveness of the instructor's presentations and explanations in conveying course content?''',
                 '''Were the online resources, such as videos or simulations, readily accessible and helpful in reinforcing concepts covered in class?''',
                 '''Did you find the instructions for assignments and assessments clear and unambiguous?''',
                 '''To what degree did the assignments and assessments accurately evaluate your comprehension of the course material?''',
                 '''Were the assigned readings relevant to the course content?''',
                 '''Were assignment instructions clear and easy to follow?''']

search_ques = []
score = 0  # Initialize score outside of the function

@csrf_exempt
@require_http_methods(["POST"]) 
def retrieve(request):
    global score
    global search_ques  # Make sure to use global keyword here
    ini = json.loads(request.body.decode("utf-8"))
    question = ini["queryResult"]["queryText"]
    query = ini["queryResult"]["queryText"]
    
    if "no" in query or "stop" in query:
        if score > 0:
            search_ques.clear()
            print("Final score is:", score)
            final = "There is no need of the mentor for you, You can do it again by trying"
            response = {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [final],
                        }
                    }
                ]
            }
            score = 0  # Reset score
            subject="No need of Mentor Assistance"
            message=''' Dear Student,
                        Based on the assessment taken by you, there is nor need of the mentoe for you, have faith in yourseld and you can do it'''
            send_email(subject,message,"sajagagrawal28@gmail.com")
            return JsonResponse(response)
        else:
            search_ques.clear()
            print("Final Score is:", score)
            final = "There is serious need of mentor"
            response = {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [final],
                        }
                    }
                ]
            }
            score = 0  # Reset score
            subject="Request for Mentor Assistance"
            message='''Dear Student,
                       Based on the assessment taken by you there is serious need of the Mentor
                     '''
            send_email(subject,message,"sajagagrawal28@gmail.com")
            return JsonResponse(response)
    else:    
        if ini["queryResult"]["queryText"] != "ok start":
            answer = ini["queryResult"]["queryText"]
            judgment = call_openai_api(question, answer)
            if "good" in judgment.lower() or "yes" in judgment.lower() or "neutral" in judgment.lower():
                score += 1
                print("Score is now:", score)
            else:
                score -= 1
                print("Score is now:", score)
                
            num = random.randint(0, len(question_list)-1)
            question_new = question_list[num]
            if question_new in search_ques:
                num = (num + 1) % (len(question_list)-1)
                question_new = question_list[num]
            search_ques.append(question_new)
            response = {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [question_new],
                        }
                    }
                ]
            }
            return JsonResponse(response)

    num = random.randint(0, len(question_list)-1)
    question_new = question_list[num]
    if question_new in search_ques:
        num = (num + 1) % (len(question_list)-1)
        question_new = question_list[num]
    search_ques.append(question_new)
    response = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [question_new],
                }
            }
        ]
    }
    return JsonResponse(response)
