#Function to get a dictionary in the style of a .geojson file:
import json
import requests

def GeoJSONdict(df,df_value,locations,colors,scale=1.0):
    '''
    Function that prints a dictionary structure to create a .geojson file.
    df: Pandas dataframe.
    df_value: column of the dataframe containing the values to plot.
    locations: list of locations by name. Case-insensitive. Can be country or city.
    colors: list of colors for the locations to be plotted in.
    scale: size of the polygons, type float or int. Default=1.0
    Prints block of code to create a .geojson file.
    The .geojson file will create a map that marks each location with a 3 sided 
    polygon, with one of its vertices set at the exact coordinates of the location.
    The size of each polygon is determined by the values used and the scale given. 
    Result can be copied and tested in the site http://geojson.io
    '''
    try:
        assert len(colors)>=len(locations), \
        'colors list must be same length or longer than locations list!'

        #class jsDict will be created assubclass of dict, to modify the way 
        #dictionaries are printed. In this case it will allow for double quotes 
        #to be printed instead of single quotes. 
        class jsDict(dict):
            def __str__(self):
                return json.dumps(self)  

        coordinates = []#Coordinates in [lat,lon] format   
        for p in locations:#Iterate over list of location names
           #Use url to get country locations by inserting the country name
            url = '{0}{1}{2}'.format('https://nominatim.openstreetmap.org/search.php?q=',
                                     p,
                                     '&format=json&polygon=0')

            response = requests.get(url).json()[0]
            lst = [response.get(key) for key in ['lat','lon']]
            output = [float(i) for i in lst]
            coordinates.append(output)

        d = {'type': 'FeatureCollection',
              'features': []}

        for i in range(len(df)):

            point_move = df[df_value].values[i]*scale

            d['features'].append(dict(type='Feature',
                                      properties={'stroke':colors[i],
                                                  'stroke-width':2,
                                                  'stroke-opacity':1,
                                                  'fill':colors[i],
                                                  'fill-opacity': 0.65,
                                                  'Location':locations[i],
                                                  'Value':'{:.3f}'.format(df[df_value].values[i])},
                                      geometry={'type':'Polygon',
                                                'coordinates':[[[coordinates[i][1],coordinates[i][0]],
                                      [coordinates[i][1]+point_move,coordinates[i][0]+point_move],
                                      [coordinates[i][1]-point_move,coordinates[i][0]+point_move],
                                      [coordinates[i][1],coordinates[i][0]]                          
                                                               ]]}))
        code = jsDict(d) 
        print(json.dumps(code,indent=2))#Use json.dumps to indent printed version of dictionary.
    except NameError as nerr:
        print('NameError: {} \nPlease '.format(nerr)+
        'import json library and requests library!')
