import requests,re
from bs4 import BeautifulSoup

head = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
url = "https://lms.ssn.edu.in/login/index.php"
user = input("Email: ")
passwd = input("Password: ")
r = requests.Session()
data = {'username': user, 'password': passwd, 'anchor': ""}
s = r.post(url, headers=head, data=data)
soup = BeautifulSoup(s.content, 'html.parser')

results = soup.find_all('a', class_="list-group-item list-group-item-action")
n = int(input("Number of courses: "))
my_courses = [input("Course {}: ".format(i)) for i in range(1, n+1)]
with open('Details.txt', 'w') as f:
    f.write("{}\n{}\n".format(user, passwd))
    for course in my_courses:
        for result in results:
            if course in str(result):
                match = re.findall(r"href=\"(.+)\"", str(result))
                url = match[0]
                f.write("{} {}\n".format(course, url))
                break
        s = r.get(url, headers=head)
        soup = BeautifulSoup(s.content, 'html.parser')
        part = soup.find_all("div", class_="card-body")
        part = str(part[1].encode("utf-8"))
        patt = r"/https\:\/\/lms\.ssn\.edu\.in\/mod\/[a-z]+\/view\.php\?id=\d+"
        match1 = "\n".join(re.findall(patt, part))
        with open(course+".txt", 'w') as f1:
            f1.write(match1)
