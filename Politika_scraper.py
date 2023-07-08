#Scrapes the Latin alphabet Politika.rs website news archive > XML output

from bs4 import BeautifulSoup
import requests

agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
politika = "https://www.politika.rs"
end = "Sadržaj ove stranice privremeno nije dostupan zbog podizanja novog portala. Uskoro ce svi sadržaji postati dostupni. Hvala na strpljenju."

# Enter year to parse, post-2005
year = 2006

# Determine link to archive
for i in range (1,13):
    page = 1
    
    if i<10:
        url = "https://www.politika.rs/sr/articles/archive/" + str(year) +"/0" + str(i) + "/14/page:" + str(page) + "?url="
    else:
        url = "https://www.politika.rs/sr/articles/archive/" + str(year) + "/" + str(i) + "/14/page:" + str(page) + "?url="

    checkresponse = requests.get(url, headers = agent)
    checksoup = BeautifulSoup(checkresponse.text, 'html.parser')
    check = checksoup.find('h1')
    checkend = check.text.strip()

    print(url)
    
    # Iterate pages until an error page is encountered
    while checkend != end:
    
        response = requests.get(url, headers = agent)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find('body').find_all('a', href=True)
        count = 0

        # Write text to a new file
        outpath = str(year) + "-" + str(i) + "-14-" + str(page) + " Politika.xml"
        print("Writing text to:", outpath)
        f = open(outpath, "w", encoding='utf-8', newline='')
        
        # Add TEI header
        print('Adding header')
        with open("TEI header.txt") as header:
            for line in header:
                f.write(line)

        # Grab text from linked articles
        for x in links:
            if "clanak" in x['href']:
                newurl = politika + x['href']
                newresponse = requests.get(newurl, headers = agent)
                newsoup = BeautifulSoup(newresponse.text, 'html.parser')
                naziv = newsoup.find('h1')
                vest = newsoup.find('div', {"id": "text-holder"})

                # Since they're double linked in the source code
                if (count % 2 == 0):
                    txt1 = naziv.text.strip() + "\n"
                    txt2 = vest.text.strip() + "\n"
                    txt3 = txt1 + txt2
                    f.write(txt3)
                count += 1
                checkend = check.text.strip()
                
        # Add TEI closed tags at the end
        print('Adding footer', flush=True)
        with open("TEI closed tags.txt") as footer:
            for line in footer:
                f.write(line)
            
        page += 1
        checkend = check.text.strip()
        
        # Scuffed ~continuation~
        if i<10:
            url = "https://www.politika.rs/sr/articles/archive/" + str(year) +"/0" + str(i) + "/14/page:" + str(page) + "?url="
        else:
            url = "https://www.politika.rs/sr/articles/archive/" + str(year)  + "/" + str(i) + "/14/page:" + str(page) + "?url="
        checkresponse = requests.get(url, headers = agent)
        checksoup = BeautifulSoup(checkresponse.text, 'html.parser')
        check = checksoup.find('h1')
        checkend = check.text.strip()
        print(url)
