import requests, re, sqlite3, platform, warnings, time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
warnings.filterwarnings("ignore")

ua = UserAgent()
head = {'User-Agent':ua.chrome}
url = "https://lms.ssn.edu.in/login/index.php"
print("Enter your credentials for LMS below")
user = input("Email: ")
passwd = input("Password: ")
student_name = input("Your name as registered in LMS: ")
r = requests.Session()
data = {'username': user, 'password': passwd, 'anchor': ""}
s = r.post(url, headers=head, data=data, verify=False)


if student_name not in s.text:
    print("Invalid Credentials/ Details! Restart setup and use correct details.")
    time.sleep(3)
    print("Quitting setup...")
    time.sleep(5)
    exit(-1)
    
soup = BeautifulSoup(s.content, 'html.parser')

os = platform.system()
with open('Config', 'w') as config:
    config.write("{}\n{}\n{}".format(user, passwd, os))

results = soup.find_all('a', class_="list-group-item list-group-item-action")
n = int(input("Number of courses: "))
my_courses = [input("Subject Code for Course {}: ".format(i)).lower() for i in range(1, n + 1)]


with open("Courses.db", "w") as f:
    pass

conn = sqlite3.Connection("Courses.db")
conn.execute("""CREATE TABLE Courses (code TEXT not null, url TEXT not null)""")
cur = conn.cursor()

valid_courses = []
for course in my_courses:
	flg = 0
	for result in results:
		if course in str(result).lower():
			match = re.findall(r"href=\"(.+)\"", str(result))
			url = match[0]
			flg = 1
			cmd = """INSERT INTO Courses (code, url) VALUES ("{}", "{}")""".format(course, url)
			cur.execute(cmd)
			valid_courses.append(course.upper())
			break
	if not flg:
		print("Subject Code {} not found in LMS! Skipping course...".format(course))
		continue
	
	cur.execute("CREATE TABLE {} (Titles TEXT NOT NULL)".format(course))
	
	s = r.get(url, headers=head, verify=False).text
	soup = BeautifulSoup(s, 'html.parser')
	part = soup.find("ul", class_="topics")
	
	for section in part:
		if not section:
			continue
		sub = section.find_all("span", class_="instancename")

		for item in sub:
			subpattern = r"""instancename\"\>(.+)\<span class=\"accesshide\"\>"""
			submatch = re.findall(subpattern, str(item))
			if not submatch:
				continue
			cur.execute("""INSERT INTO "{}" (Titles) VALUES ("{}")""".format(course, submatch[0]))

conn.commit()
conn.close()
r.close()
print("Setup Successful!")
print("Added the following courses to monitor:  ")
print("\n".join(valid_courses))
time.sleep(3)
print("Exiting...")
time.sleep(2)
