import requests
from datetime import date

ipserver = "192.168.1.8"
port = "8080"
appname="icescrum"

def getDate(str_date):
    tmp = str_date.split('T')[0].split('-')
    return date(int(tmp[0]),int(tmp[1]),int(tmp[2])+1)
    
class Icescrum(object):
    @staticmethod
    def get_json(url):
        headers = {'Accept':'application/json'}
        r = requests.get(url, auth=('rafel', 'rafel'), headers=headers)	
        return r.json()
    
class Task(object):
    def __init__(self, projectid, taskid=None):
        self.projectid=projectid
        self.id=None
        self.name=None
        self.description=None
        self.state = 0
        self.estimation=0
        self.doneDate=None
        self.parentStory=None
        
        if taskid is not None:
            task = Task.parseJSON(Icescrum.get_json('http://%s:%s/%s/ws/p/%s/task/%d' % (ipserver, port, appname, projectid, taskid)), projectid)
            self.id=task.id
            self.name=task.name
            self.description=task.description
            self.state = task.state
            self.estimation=task.estimation
            self.doneDate=task.doneDate
            self.parentStory=task.parentStory
     
    @staticmethod
    def parseJSON(data, projectid):
        t = Task(projectid=projectid)
        t.id = int(data['id'])
        t.name = data['name']
        t.description = data['description']
        t.state = int(data['state'])
        t.estimation = int(data['estimation'])
        t.doneDate = data['doneDate']
        t.parentStory = data['parentStory']
        
        return t
    
    def __repr__(self):
        return '<Task Object: %s>' % self.name
    
class Story(object):
    def __init__(self, projectid, storyid=None):
        self.projectid=projectid
        self.id = None
        self.name = None
        self.state = 0
        self.description = None
        self.effort = 0
        self.doneDate = None
        self.tasks = []
        
        if storyid is not None:
            story = Story.parseJSON(Icescrum.get_json('http://%s:%s/%s/ws/p/%s/story/%d' % (ipserver, port, appname, projectid, storyid)), projectid)
            self.id = story.id
            self.name = story.name
            self.state = story.state
            self.description = story.description
            self.effort = story.effort
            self.doneDate = story.doneDate
            self.tasks = story.tasks
        
    @staticmethod
    def parseJSON(data, projectid):
        s = Story(projectid=projectid)
        s.id = int(data['id'])
        s.name = data['name']
        s.state = int(data['state'])
        s.description = data['description']
        s.effort = int(data['effort'])
        s.doneDate = data['doneDate']
        for task in data['tasks']:
            s.tasks.append(Task(projectid=projectid, taskid=int(task['id'])))
        return s
    
    def __repr__(self):
        return '<Story Object: %s>' % self.name
    
class Sprint(object):
    def __init__(self, projectid, sprintid=None):
        self.projectid=projectid
        self.id = None
        self.state = 0
        self.orderNumber = 0
        self.startDate = None
        self.endDate = None
        self.stories = []
        self.goal = None
        
        if sprintid is not None:
            sprint = Sprint.parseJSON(Icescrum.get_json('http://%s:%s/%s/ws/p/%s/sprint/%d' % (ipserver, port, appname, projectid, sprintid)), projectid)
            self.id = sprint.id
            self.state = sprint.state
            self.orderNumber = sprint.orderNumber
            self.startDate = getDate(sprint.startDate)
            self.endDate = getDate(sprint.endDate)
            self.stories = sprint.stories
            self.goal = sprint.goal
    
    @staticmethod
    def parseJSON(data, projectid):
        s = Sprint(projectid=projectid)
        s.id = int(data['id'])
        s.state = int(data['state'])
        s.orderNumber = int(data['orderNumber'])
        s.startDate = data['startDate']
        s.endDate = data['endDate']
        s.goal = data['goal']
        for story in data['stories']:
            s.stories.append(Story(projectid=projectid, storyid=int(story['id'])))
        return s
    
    def __repr__(self):
        return '<Sprint Object: S%02d>' % self.orderNumber
            
class Release(object):
    def __init__(self, projectid, releaseid = None):
        self.projectid=projectid
        self.id = None
        self.name = None
        self.state = 0
        self.orderNumber = 0
        self.startDate = None
        self.endDate = None
        self.sprints = []
        self.goal = None
        
        if releaseid is not None:
            rel = Release.parseJSON(Icescrum.get_json('http://%s:%s/%s/ws/p/%s/release/%d' % (ipserver, port, appname, projectid, releaseid)), projectid)
            self.id = rel.id
            self.name = rel.name
            self.state = rel.state
            self.orderNumber = rel.orderNumber
            self.startDate = rel.startDate
            self.endDate = rel.endDate
            self.sprints = rel.sprints
            self.goal = rel.goal
            
    @staticmethod
    def parseJSON(data, projectid):
        r = Release(projectid=projectid)
        r.id = int(data['id'])
        r.name = data['name']
        r.state = int(data['state'])
        r.orderNumber = int(data['orderNumber'])
        r.startDate = data['startDate']
        r.endDate = data['endDate']
        r.goal = data['goal']
        for sprint in data['sprints']:
            r.sprints.append(Sprint(projectid=projectid, sprintid=int(sprint['id'])))
        return r
        
    def __repr__(self):
        return '<Release Object: %s>' % self.name
    
class ScrumProject(object):
    def __init__(self, projectid="SM"):
        self.releases = []
        rel_list = Icescrum.get_json('http://%s:%s/%s/ws/p/%s/release/' % (ipserver, port, appname, projectid))
        for rel in rel_list:
            self.releases.append(Release.parseJSON(rel, projectid))
                
    def get_sprint(self, sprintid):
        for r in self.releases:
            for s in r.sprints:
                if s.id == sprintid:
                    return s    
        return None
    
    def get_story(self, storyid):
        for r in self.releases:
            for s in r.sprints:
                for st in s.stories:
                    if st.id == storyid:
                        return st
        return None
    
    def get_task(self, taskid):
        for r in self.releases:
            for s in r.sprints:
                for st in s.stories:
                    for t in st.tasks:
                        if t.id == taskid:
                            return t
        return None

    def get_current_sprint(self):
        for r in self.releases:
            for s in r.sprints:
                if s.state == 2:
                    return s
        return None

    def get_next_sprint(self):
        pass
        #sprints = self.icescrum.get_json('http://%s:8080/icescrum/ws/p/%s/sprint' % (self.ipserver, self.idproject))
        #planned_sprints = [sprint for sprint in sprints if sprint['state'] == 1]
        #sorted_planned_sprints = sorted(planned_sprints, key=itemgetter('startDate'))
        #return sorted_planned_sprints[0]
