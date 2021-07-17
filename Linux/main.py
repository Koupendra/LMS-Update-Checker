import requests, re, sqlite3, warnings, time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
warnings.filterwarnings("ignore")
import notify2
notify2.init('LMS-Update-Checker')

ua = UserAgent()
head = {'User-Agent':ua.chrome}
url = "https://lms.ssn.edu.in/login/index.php"
with open("Config", 'r') as f:
	user = f.readline().rstrip()
	passwd = f.readline().rstrip()
	os = f.readline().rstrip()
	
conn = sqlite3.connect("Courses.db")
cur = conn.cursor()

courses = {}
cache = list(cur.execute("""SELECT * FROM Courses"""))
for i in cache:
	courses[i[0]] = i[1]

data = {'username': user, 'password': passwd, 'anchor': ""}
r = requests.Session()
s = r.post(url, headers=head, data=data, verify=False)


for course in courses:
        old_topics = list(cur.execute("SELECT titles from {}".format(course)))
        old_topics = [j[0] for j in old_topics]
        cur.execute("DELETE FROM {}".format(course))
        url = courses[course]
        s = r.get(url, headers=head, verify=False).text
        soup = BeautifulSoup(s, 'html.parser')
        part = soup.find("ul", class_="topics")

        updates = []
        refresh = []
        for section in part:
                if not section:
                        continue
                sub = section.find_all("span", class_="instancename")

                for item in sub:
                        subpattern = r"""instancename\"\>(.+)\<span class=\"accesshide\"\>"""
                        submatch = re.findall(subpattern, str(item))
                        if not submatch:
                                continue
                        refresh.append(submatch[0])

        for content in refresh:
                if content not in old_topics:
                        updates.append(content)
                cur.execute("""INSERT INTO "{}" (Titles) VALUES ("{}")""".format(course, content))

        if updates:
                if len(updates)>1:
                        notify2.Notification("LMS-Update-Checker", "{} has got {} and {} other update(s)".format(course.upper(), updates[0], len(updates)-1), "Moodle.ico").show()
                else:
                       	notify2.Notification("LMS-Update-Checker", "{} has got {} update".format(course.upper(), updates[0]), "Moodle.ico").show()
                
                time.sleep(5)
conn.commit()
conn.close()
r.close()
