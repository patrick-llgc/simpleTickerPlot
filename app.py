from flask import Flask, render_template, request, redirect
import numpy as np
from analyzeAndPlot import *



app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # request was a POST
        app.vars['tickerSymbol'] = request.form['tickerSymbol'].upper()
        app.vars['typeOfData'] = []
        if request.form.getlist('Close') == ['1']:
            app.vars['typeOfData'].append('Close')
        if request.form.getlist('Open') == ['1']:
            app.vars['typeOfData'].append('Open')
        if request.form.getlist('Adjusted Close') == ['1']:
            app.vars['typeOfData'].append('Adjusted Close')

        f = open('log/logfile','a')
        f.write(datetime.now().strftime('%Y%m%d%H%M%S')+ \
            '\t%5s\n' % (app.vars['tickerSymbol']) + \
            '\tRequested prices:' +', '.join(app.vars['typeOfData']) + '\n')
        f.close()
        return redirect('/graph')
    


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'GET':
        if len(app.vars['typeOfData']) < 1:
            return render_template('index.html')
        # app.vars['typeOfData'] =['Open','Close']
        analyzeAndPlot(app.vars['tickerSymbol'], app.vars['typeOfData'])  # change Open to parameters
        htmlfilename = '_' + app.vars['tickerSymbol']+'.html'
        

        return render_template(htmlfilename)
        # after body, inser the following
        #<h1>Generated graph for GOOG<br><a href="/index">Back</a></h1>
        #return PKI.html
    else:
        # request was a POST
        return render_template('index.html')


if __name__ == '__main__':
    app.run(port=33507, debug=True)




