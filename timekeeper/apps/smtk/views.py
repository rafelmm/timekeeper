from django.shortcuts import render
import requests
from datetime import date
from .icescrum import ScrumProject
import calendar

scrumProject = None

def get_json(url):
    headers={'Accept':'application/json'}
    r = requests.get(url, auth=('rafel','rafel'), headers=headers)    
    return r.json()

# Create your views here.
def indexView(request):
    global scrumProject
    if scrumProject is None:
        scrumProject = ScrumProject("SM")
    current_sprint = scrumProject.get_current_sprint()
            
    return render(request, 
                  "smtk/index.html",
                  {'sprint':current_sprint,
                   'stories': current_sprint.stories}
                  )
    
def storyView(request, storyid):
    global scrumProject
    if scrumProject is None:
        scrumProject = ScrumProject("SM")
    story = scrumProject.get_story(int(storyid))
    return render(request, 
                  "smtk/story.html",
                  {'story':story,
                   'tasks': story.tasks}
                  )

def taskView(request, taskid):
    global scrumProject
    if scrumProject is None:
        scrumProject = ScrumProject("SM")
    task = scrumProject.get_task(int(taskid))
    return render(request, 
                  "smtk/task.html",
                  {'task':task}
                )
    
def calendarView(request):
    global scrumProject
    if scrumProject is None:
        scrumProject = ScrumProject("SM")
        
    current_sprint = scrumProject.get_current_sprint()
    
    today = date.today()
    cal = {
           "month": today.strftime("%B"),
           "year": today.year,
           "days":[]
           }
    
    sem = [0]*7
    for d in range(1,calendar.monthrange(today.year, today.month)[1]+1):
        wd = date(today.year, today.month, d).weekday()
        sem[wd]={
                 "number": d,
                 "state":'',
                 }
            
        if wd==5 or wd==6:
            sem[wd]['state']='noworkingday'
        elif date(today.year, today.month, d) >= current_sprint.startDate and date(today.year, today.month, d) <= current_sprint.endDate:
            if d==3:
                sem[wd]['state']='completed'
            elif date(today.year, today.month, d) < today:
                sem[wd]['state']='current'
        else:
            sem[wd]['state']='closed'
        
            
        if date(today.year, today.month, d) == today:
            sem[wd]['state']+=' today'
            
        if wd==6:
            cal['days'].append(list(sem))
            sem=[0]*7
            
    if any(sem)!=0:
        cal['days'].append(list(sem))
    
    return render(request, 
                  "smtk/calendar.html", 
                  {
                   'cal':cal,
                   'sprint': current_sprint,
                   })