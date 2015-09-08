import requests
from pandas import *
from bokeh.plotting import figure, show, output_file, vplot, save 
from bokeh.charts import TimeSeries
# from bokeh.io import output_notebook
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components

def analyzeAndPlot(tickerSymbol, typeOfData):
#    tickerSymbol = 'PKI'
#    typeOfData = 'Open'
    rjson = requests.get('https://www.quandl.com/api/v3/datasets/YAHOO/'+tickerSymbol+'.json?auth_token=L9jUoYTsWeow-DN_EraF')
    data = rjson.json()
    data = data['dataset']
    mydict = {data['column_names'][column]:np.array(data['data'])[:,column] for column in range(len(data['column_names']))}
    
    def newdate(mystring):
        yyyy, mm, dd = mystring.split('-')
        dt = datetime( int(yyyy), int(mm), int(dd))
        return dt
    df = DataFrame(mydict)
    df.Date = df.Date.apply(newdate)
    df = df.set_index('Date').sort_index(ascending=True)
    
    output_file("stocks.html", title=tickerSymbol+"Data")
    
    # p1 = figure(x_axis_type = "datetime")
    # # p1.title = datetime.now().strftime('%m/%d/%Y')
    # p1.line(df.index, df[typeOfData], color='red', legend=tickerSymbol)
    # p1.title = tickerSymbol + " Stock Prices : " + datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    # p1.grid.grid_line_alpha=0.3
    # p1.xaxis.axis_label = 'Date'
    # p1.yaxis.axis_label = 'Price'

    # df2 = df.astype(float)[['Open','Close','Adjusted Close']]
    df2 = df.astype(float)[typeOfData]
    p1 = TimeSeries(df2.reset_index(), index='Date', legend=True, title=tickerSymbol + ' Stock Prices', xlabel='Date', ylabel='Prices')

    
    outputOption = 2  # output options
    if outputOption == 1:
        # option 1: using bokeh.plotting.save to directly save to html file
        save(p1)  # need to import from bokeh.plotting!
    elif outputOption == 2:
        # option 2: using bokeh.embed.file_html to save to standalone html file
        html = file_html(p1, CDN, "my plot")
        f = open('./templates/_'+tickerSymbol+'.html','w')
        returnBtn =  '<h1>Generated graph for '+tickerSymbol+'<br><a href="/index">Back</a></h1>'
        html = html.replace('<body>','<body>'+returnBtn)
        f.write('%s' % html)
        f.close()
    elif outputOption == 3:
        # option 2: using bokeh.embed.components to save to html components
        script, div = components(p1)
        f = open(tickerSymbol+'.html','w')
        f.write('%s' % script)
        f.close()
