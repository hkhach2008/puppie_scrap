from requests import Session
from bs4 import BeautifulSoup
import csv
from time import sleep

with open("sighn_in.txt", "r") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
}

beeds = [
    "labrador-retriever",
    "french-bulldog",
    "golden-retriever",
    "german-shepherd-dog",
    "poodle",
    "english-bulldog",
    "beagle",
    "rottweiler",
    "dachshund",
    "pembroke-welsh-corgi",
    "australian-shepherd",
    "yorkshire-terrier",
    "boxer",
    "cavalier-king-charles-spaniel",
    "siberian-husky",
    "bernese-mountain-dog",
    "pomeranian",
    "shih-tzu",
    "chihuahua",
    "maltese",
]

requests = Session()
# requests.get("https://puppies.com/", headers=headers)


def login():
    post_data = {
        "email": lines[0],
        "password":	lines[1]
    }

    requests.post("https://puppies.com/api/auth/token", headers=headers, json=post_data, allow_redirects=True)
    
    

def get_PuppieUrl():
    login()
    for i in beeds:
        for k in range(0, 10):
            url = f"https://puppies.com/find-a-puppy/{i}?page={k}"
            # print(url)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            puppies = soup.find("div", class_="sc-gsDKAQ jVXNKC").find_all("a", class_="")
            if puppies != None:
                for j in puppies:
                    yield "https://puppies.com" + j.get("href")
            else:
                break



def get_SellerUrl():
    for i in get_PuppieUrl():
        try:
            response = requests.get(i, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            seller_url = soup.find("div", class_="jp t d nd aw ne").find("a").get("href")
            yield "https://puppies.com" + seller_url
        except:
            continue

        

def get_data():
    for i in get_SellerUrl():
        try:
            response = requests.get(i, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            name = soup.find("h1", class_="ks kt ku t aw kv kw kx").text
            # print(name)
            with open("data.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow([name])
        except:
            continue

def main():
    # pass
    get_data()
    # get_PuppieUrl()

if __name__ == "__main__":
    main()