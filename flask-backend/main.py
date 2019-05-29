from flask import Flask, render_template, request, flash, Response
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from itertools import groupby
import difflib
import xlrd
import pandas as pd
import json

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt'])
app = Flask(__name__)
CORS(app)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', token="Flask done")

@app.route('/upload', methods=['POST','GET'])
def getvalue():
    if request.method == 'POST':
        # if 'file' not in request.files:
        #     flash('No file part')
        file = request.files['file']
        # if file.filename == '':
        #     flash('No selected file')
        if file and allowed_file(file.filename):
            filename = "hello"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
    f = open("hello",'r')
    paragraph = f.read()
    # paragraph = "i'm from Ranchi"
    import pandas as pd
    stop_words = set(stopwords.words('english'))
    placename = ''
    upname = ''
    data = pd.read_excel("ap2.xls")
    print("Enter the paragraph to find locations:")
    # paragraph = "I'm from Srinagar"
    word_tokens = word_tokenize(paragraph)
    filtered_para = [w for w in word_tokens if not w in stop_words]
    req = list(data.loc[:, 'Name of City'])
    req2 = data[['Name of City', 'State']]
    samenames = pd.concat(g for _, g in req2.groupby("Name of City") if len(g) > 1)

    #######
    dic2 = {}
    for row in samenames.iterrows():
        key = row[1][0]
        value = row[1][1]
        if key in dic2:
            dic2[key].append(value)
        else:
            dic2[key] = []
            dic2[key].append(value)

######################################################################################################33##################################################
    def same(location):
        print("In which among the following is the " + location)
        for word in dic2[location]:
            print(word)
        while True:
            upperlevel = input()
            if upperlevel in dic2[location]:
                break
            else:
                print("Something's wrong.. Enter Again")
        return [location, upperlevel]


    ####### To Identify Multi-worded Cities #######
    # Trail-4
    req.sort()
    res = [list(i) for j, i in groupby(req,
                                       lambda a: a.split(' ')[0])]
    dic = {}
    for lis in res:
        dic[lis[0]] = lis[1:]


    def intel(location):
        for word in dic[location]:
            if word in paragraph:
                location = word
        return location
    ################################################


    locations = []
    closelist = []
    index = 0
    prem = 0
    for word in filtered_para:
        for area in req:
            if area == word.capitalize():
                prem += 1
                locations.append(intel(word))
                break

######################################################################################################33##################################################
        # Spellings
        if prem == 0:
            closelist = difflib.get_close_matches(word, req, 2, 0.8)
            if len(closelist) != 0:
                for i in range(len(closelist)):
                    print("Is it " + str(closelist[i]) + '?')
                    print("yes/no :")
                    close = input()
                    if close == 'yes':
                        locations.append(closelist[i])
        prem = 0


    for index, name in enumerate(locations):
        if name in dic2:
            locations[index] = same(name)

    # Only 1 location found
    if len(locations) == 1:
        if isinstance(locations[0], list):
            placename = locations[0][0]
            upname = locations[0][1]
            print("You live in " + locations[0][0] + ', ' + locations[0][1])
        else:
            placename = locations[0]
            index = data[data['Name of City'] == locations[0]].index.item()
            print("You live in " + locations[0] + ', ' + data.loc[index, "State"])
            upname = data.loc[index, "State"]
            

    # Morethan 1 locations found
    elif len(locations) >= 1:
######################################################################################################33##################################################
        print("I got two locations")
        print("Which among the following")
        for name in locations:
            if isinstance(name, list):
                print(str(name[0]))
            else:
                print(str(name))
        while True:
            final = input()
            for lis in locations:
                if isinstance(lis, list):
                    if lis[0] == final:
                        placename = lis[0]
                        upname = lis[1]
                        print("You live in " + lis[0] + ', ' + lis[1])
                        break
                else:
                    if lis == final:
                        placename = lis
                        index = data[data['Name of City'] == final].index.item()
                        print("You live in " + lis + ', ' +
                              data.loc[index, "State"])
                        upname = data.loc[index, "State"]
                        break

            else:
                print("Somethings's wrong.. Enter again")
                continue
            break
    else:
        print("No locations found")
    # return render_template('index.html', n=str(placename), m=str(upname))
    data ={}
    data["pn"] = str(placename)
    data["un"] = str(upname)

    return Response(json.dumps(data),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)