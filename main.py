import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

url = "https://www.flipkart.com/search?q=best+mobile+under+100000&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_4_25_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_4_25_na_na_na&as-pos=4&as-type=RECENT&suggestionId=best+mobile+under+100000&requestId=f3666fc6-3e12-41f5-a7a7-eb85e0ab4278&as-searchtext=best%20mobile%20under%20100000"

r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")
max = soup.find("div",class_="_2MImiq")
span  = max.findChild("span")
span_split = span.text.split()
max = int(span_split[-1])
#print(max)
#print(soup)

df  = pd.DataFrame(columns=["Name","Price","Rating","Product Link"])


for i in tqdm(range(2,408)):
    name = soup.find_all("div",class_="_4rR01T")
    name = [x.text for x in name]
    price = soup.find_all("div",class_="_30jeq3 _1_WHN1")
    price = [x.text for x in price]
    rating = soup.find_all("div",class_=re.compile(r'\b_3LWZlK\b'))
    rating = [x.text for x in rating]
    rating = rating[:len(price)]
    product_link = soup.find_all("a",class_="_1fQZEK")
    product_link = ["https://www.flipkart.com"+x.get("href") for x in product_link]
    df2 = pd.DataFrame({
    "Name": name,
    "Price": price,
    "Rating": rating,
    "Product Link": product_link
})
    df = pd.concat([df,df2])
    nplink = f"https://flipkart.com/search?q=best+mobile+under+100000&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_4_25_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_4_25_na_na_na&as-pos=4&as-type=RECENT&suggestionId=best+mobile+under+100000&requestId=f3666fc6-3e12-41f5-a7a7-eb85e0ab4278&as-searchtext=best+mobile+under+100000&page={i}"
    url = nplink
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")


df = df.reset_index(drop=True)
df.to_excel('data.xlsx', index=False)