import requests,re
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

head = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
url = "https://lms.ssn.edu.in/login/index.php"
with open("Details.txt", 'r') as f:
    user = f.readline().rstrip()
    passwd = f.readline().rstrip()
    temp = [i.rstrip() for i in f.readlines()]
courses = {}
for i in temp:
    t = i.split()
    courses[t[0]] = t[1]
data = {'username': user, 'password': passwd, 'anchor': ""}
r = requests.Session()
s = r.post(url, headers=head, data=data)
updates = []
for course in courses:
    url = courses[course]
    s = r.get(url, headers=head)
    soup = BeautifulSoup(s.content, 'html.parser')
    part = soup.find_all("div", class_="card-body")
    with open(course+".html",'r+') as f:
        old_links = f.read()
        part1 = str(part[1].encode("utf-8"))
        patt = r"https\:\/\/lms\.ssn\.edu\.in\/mod\/resource\/view\.php\?id=\d+"
        match1 = "\n".join(re.findall(patt, part1))
        if match1 != old_links:
            updates.append(course)
            f.write(match1)
if updates:
    toaster = ToastNotifier()
    toaster.show_toast("LMS",', '.join(updates)+" has got updates",duration=10)