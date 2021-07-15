import requests, re, sqlite3, warnings, time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
warnings.filterwarnings("ignore")

ua = UserAgent()
head = {'User-Agent':ua.chrome}
url = "https://lms.ssn.edu.in/login/index.php"
with open("Config", 'r') as f:
	user = f.readline().rstrip()
	passwd = f.readline().rstrip()
	os = f.readline().rstrip()
	if os=="Windows":
		from win10toast import ToastNotifier
	elif os=="Linux":
		import notify2
		notify2.init('LMS-Update-Checker')
	else:
		print("Unsupported Operating System! Exiting...")
		exit(-1)
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
        s = r.get(url, headers=head).text
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
                if os=="Linux":
                        notify2.Notification("Summary", "Some body text","notification-message-im").show()
                else:
                        toaster = ToastNotifier()
                        if len(updates)>1:
                                toaster.show_toast("LMS-Update-Checker","{} has got {} and {} other update(s)".format(course.upper(), updates[0], len(updates)-1), icon_path="Moodle.ico", duration=15)
                        else:
                                toaster.show_toast("LMS-Update-Checker","{} has got {} update".format(course.upper(), updates[0]), icon_path="Moodle.ico", duration=15)
                time.sleep(5)
conn.commit()
conn.close()
r.close()
