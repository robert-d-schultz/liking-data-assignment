from scipy.stats.stats import pearsonr
from scipy.spatial.distance import cosine
from scipy import polyval, polyfit
import re
import os
from datetime import datetime, timezone
from dateutil import parser
import operator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import pickle


import feature_extractor as fe


# preprocess the chat logs into tuples (date/time, speaker, message)
def load_data():
    # build list of filenames
    filenames = []
    for path, subdirs, files in os.walk('./data/'):
        for name in files:
            if name.endswith('.html'):
                filenames.append(os.path.join(path, name))

    tuples = []
    for filename in filenames:
        print("processing " + filename + "...")
        base = os.path.basename(filename)
        name = os.path.splitext(base)
        master_dt_obj = datetime.strptime(name[0][0:-3], '%Y-%m-%d.%H%M%S%z')
        with open(filename) as f:
            lines = f.readlines()
        for line in lines[1:-1]:
            # assume speaker based on font color (red=patrick, blue=rob)
            m = re.search('\<font color\=\"\#([A-Z0-9]+)\"\>', line)
            if not m:
                continue
            speaker = ""
            if m.group(1) == 'A82F2F':
                speaker = 'patrick'
            if m.group(1) == '16569E':
                speaker = 'rob'

            # get the time from the log, use the date and timezone from the filename
            n = re.search('\<font size\=\"2\"\>\(([0-9A-Z\:\s]+)\)\<\/font\> \<b\>', line)
            if not n:
                print(filename)
            date = n.group(1)
            dt_obj = parser.parse(date)
            final_dt_obj = master_dt_obj.replace(hour=dt_obj.hour,minute=dt_obj.minute,second=dt_obj.second)

            # get the message
            o = re.search('\<\/b\>\<\/font\> (.*)\<br\/\>$', line)
            if not o:
                print(filename)
            message = o.group(1)

            tuples.append([final_dt_obj,speaker,message])
    print(len(tuples))
    tuples.sort(key=operator.itemgetter(0))
    # concatenate consecutive tuples spoken by the same person
    # keep the first and last time/dates
    concat_tuples = [[tuples[0][0],tuples[0][0],tuples[0][1],tuples[0][2]]]
    for i in range(1,len(tuples)):
        if concat_tuples[-1][2] == tuples[i][1]:
            concat_tuples[-1][1] = tuples[i][0] # replace last date in concat_tuples[-1] with the date in tuple[i]
            concat_tuples[-1][3] = concat_tuples[-1][3] + ' ' + tuples[i][2] # concatenate the two messages (with a space between)
        else:
            concat_tuples.append([tuples[i][0],tuples[i][0],tuples[i][1],tuples[i][2]])

    pickle.dump(concat_tuples, open("pickle/tuples.p", "wb"))
    print(len(concat_tuples))
    return concat_tuples

if __name__ == "__main__":
    tuples = []
    if not os.path.exists("pickle/tuples.p"):
        tuples = load_data()
    else:
        tuples = pickle.load(open("pickle/tuples.p", "rb" ))

    docs = [t[3] for t in tuples]
    feat_vecs = fe.extract_features(docs)

    # uses first timestamp and ignores last timestamp
    date_objs = [t[0] for t in tuples]

    # pearson correlations between consecutive messages
    '''corrs = []
    for i in range(len(feat_vecs)-1):
        a = feat_vecs[i]
        b = feat_vecs[i+1]
        corr = pearsonr(a,b)
        corrs.append(corr[0])'''

    # cosine similarity between consecutive messages
    coss = []
    labels = []
    for i in range(len(feat_vecs)-1):
        a = feat_vecs[i]
        b = feat_vecs[i+1]
        cos = cosine(a,b)
        if math.isnan(cos):
            continue
        else:
            cos = 1 - cos
            labels.append(date_objs[i])
            coss.append(cos)

    # cosine similarity plotted overtime
    fig, ax = plt.subplots(1)
    fig.autofmt_xdate()
    plt.plot(labels, coss, 'r,')
    xfmt = mdates.DateFormatter('%d-%m-%y %H:%M')
    ax.xaxis.set_major_formatter(xfmt)


    # simple linear regression
    labels_s = [(t-datetime(2014,1,1, tzinfo=timezone.utc)).total_seconds() for t in labels]
    (ar,br)=polyfit(labels_s,coss,1)
    print(ar)
    print(br)
    xr=polyval([ar,br],labels_s)
    print(xr[0])
    print(xr[-1])
    plt.plot(labels, xr, color='blue',linewidth=3)

    plt.show()
