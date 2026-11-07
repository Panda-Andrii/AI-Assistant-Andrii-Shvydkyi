import requests

url = "https://www.whenisthenextmcufilm.com/api"
response = requests.get(url)

print("When is the next MCU film \n")

if response.ok:
    film = response.json()
    print(film["title"])
    print(f"releases in", film["days_until"], "days" )
    print("\nRelease Date: ", film["release_date"])
    print("\nProduction Type: ", film["type"])
    print("\nWhat's afterwards?", film['following_production']['title'])
else:
    response.raise_for_status()