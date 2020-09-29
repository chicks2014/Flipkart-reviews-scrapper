# load libraries
from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import re
app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def searchreview():
    searchString = request.form['content'].replace(" ", "")
    try:
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString  # preparing the URL to search the product on flipkart
        uClient = uReq(flipkart_url)  # requesting the webpage from the internet
        flipkartPage = uClient.read()  # reading the webpage
        uClient.close()  # closing the connection to the web server
        flipkart_html = bs(flipkartPage, "html.parser")  # parsing the webpage as HTML
        bigboxes = flipkart_html.findAll("div", {
            "class": "bhgxx2 col-12-12"})  # seacrhing for appropriate tag to redirect to the product link
        del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
        box = bigboxes[0]  # taking the first iteration (for demo)
        productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  # extracting the actual product link
        prodRes = requests.get(productLink)  # getting the product page from server
        prod_html = bs(prodRes.text, "html.parser")  # parsing the product page as HTML
        ratingBox = prod_html.find_all('div', {'class': "ebepc-"})
        overallBox = prod_html.find_all('div', {'class': "_251bNL"})
        customerImg = prod_html.find_all('div', {'class': "_2-BQtO"})

        try:
            ratingNumber = ratingBox[0].div.div.div.find('div', {'class': '_1i0wk8'}).text

        except:
            ratingNumber = 'No number'

        try:
            star = ratingBox[0].div.div.div.find('div', {'class': '_2txNna'}).text
        except:
            star = 'No Rating'

        try:
            num_ratings = ratingBox[0].div.div.div.contents[1].div.span.text[:-1]

        except:
            num_ratings = 'No number'

        try:
            num_reviews = ratingBox[0].div.div.div.contents[2].div.span.text
        except:
            num_reviews = 'No Review'

        try:
            ov1 = overallBox[0].div.contents[0].div.svg.find('text', {'class': 'PRNS4f'}).text
        except:
            ov1 = 'No Rating'
        try:
            ov11 = overallBox[0].div.contents[0].div.find('div', {'class': '_3wUVEm'}).text
        except:
            ov11 = 'No Rating'

        try:
            ov2 = overallBox[0].div.contents[1].div.svg.find('text', {'class': 'PRNS4f'}).text
        except:
            ov2 = 'No Rating'
        try:
            ov21 = overallBox[0].div.contents[1].div.find('div', {'class': '_3wUVEm'}).text
        except:
            ov21 = 'No Rating'

        try:
            ov3 = overallBox[0].div.contents[2].div.svg.find('text', {'class': 'PRNS4f'}).text
        except:
            ov3 = 'No Rating'
        try:
            ov31 = overallBox[0].div.contents[2].div.find('div', {'class': '_3wUVEm'}).text
        except:
            ov31 = 'No Rating'

        try:
            ov4 = overallBox[0].div.contents[3].div.svg.find('text', {'class': 'PRNS4f'}).text
        except:
            ov4 = 'No Rating'
        try:
            ov41 = overallBox[0].div.contents[3].div.find('div', {'class': '_3wUVEm'}).text
        except:
            ov41 = 'No Rating'

        try:
            imgs = []
            for i in range(len(customerImg[0].contents)):
                styletext = customerImg[0].contents[i].attrs['style']
                imgs.append(Find(styletext)[0].replace('/178','/512'))
        except:
            img1 = 'No img'

        # reviews = []
        mydict = {"Product": searchString, "rate": ratingNumber, "star": star, "ov1": ov1,
              "ov11": ov11, "ov2": ov2, "ov21": ov21, "ov3": ov3,
              "ov31": ov31, "ov4": ov4, "ov41": ov41,
              'num_ratings': num_ratings, 'num_reviews': num_reviews}  # saving that detail to a dictionary
     # x = table.insert_one(mydict) #insertig the dictionary containing the rview comments to the collection

        # reviews.append(mydict)
        return render_template('index.html', reviews=mydict, imgs=imgs)  # showing the review to the user

    except Exception as e:
        print(e)
    return 'something is wrong'


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

if __name__ == "__main__":
    app.run(port=8001, debug=True)
