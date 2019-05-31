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


data = pd.read_excel("ap2.xls")

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
####### To Identify Multi-worded Cities #######
# Trail-4
req.sort()
res = [list(i) for j, i in groupby(req,
                                   lambda a: a.split(' ')[0])]
dic = {}
for lis in res:
    dic[lis[0]] = lis[1:]

locations = []
output = {}
placename = ''
upname = ''



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
            paragraph = file.read().decode('utf-8')
            # filename = "hello"
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    global locations    
    locations = []
    global output
    output = {}
    global placename
    placename = ''
    global upname
    upname = ''
    # f = open("hello",'r')
    # paragraph = f.read()
    import pandas as pd
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(paragraph)
    filtered_para = [w for w in word_tokens if not w in stop_words]

    def intel(location):
        for word in dic[location]:
            if word in paragraph:
                location = word
        return location
    ################################################

    # closelist = []
    index = 0
    prem = 0
    for word in filtered_para:
        for area in req:
            if area == word.capitalize():
                prem += 1
                locations.append(intel(word))
                break

        # Spellings
        if prem == 0:
            closelist = difflib.get_close_matches(word, req, 2, 0.8)
            if len(closelist) != 0:
                locations.append(closelist[0])
        prem = 0

    # Only 1 location found 
    if len(locations) == 1:
        if locations[0] in dic2:
            output["condition"] = 2
            thislist = []
            thislist = dic2[locations[0]]
            thislist.append(locations[0])
            output["list"] = thislist
            return Response(json.dumps(output),  mimetype='application/json')
        else:
            placename = locations[0]
            index = data[data['Name of City'] == locations[0]].index.item()
            upname = data.loc[index, "State"]
            llist = []
            llist.append(placename)
            llist.append(upname)
            output["condition"] = 1
            output["list"] = llist
            return Response(json.dumps(output),  mimetype='application/json')

    # Morethan 1 locations found
    elif len(locations) >= 1:
        print("I got two locations")
        print("Which among the following")
        output["condition"] = 3
        output["list"] = locations
        return Response(json.dumps(output),  mimetype='application/json')

    else:
        output["condition"] = 4
        ping = []
        output["list"] = ping
        return Response(json.dumps(output),  mimetype='application/json')

@app.route('/upload/diffloc', methods=['POST'])
def getvalues():
    if request.method == 'POST':
        global locations    
        global output
        output = {}
        global placename
        global upname
        json_data = json.loads(request.data)
        final = str(json_data["name"])
        # final = res.data
        if final in dic2:
            output["condition"] = 2
            thislist = []
            thislist = dic2[final]
            thislist.append(final)
            output["list"] = thislist
            return Response(json.dumps(output),  mimetype='application/json')
        else:
            placename = final
            print(final)
            index = data[data['Name of City'] == final].index.item()
            upname = data.loc[index, "State"]
            print(upname)
            llist = []
            llist.append(placename)
            llist.append(upname)
            output["condition"] = 1
            output["list"] = llist
            return Response(json.dumps(output),  mimetype='application/json')
    

if __name__ == '__main__':
    app.run(debug=True)