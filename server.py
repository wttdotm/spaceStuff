from flask import Flask, send_file
from flask import Response
from flask import render_template


# Space Stuff
import astropy.units as u
from astropy.coordinates.sky_coordinate import SkyCoord
from astroquery.skyview import SkyView
from astropy.units import Quantity
from astroquery.gaia import Gaia
from random import randrange
import matplotlib
matplotlib.use('Agg') 
import matplotlib.patches as patches


from astroquery.simbad import Simbad


import matplotlib.pyplot as plt
import numpy as np

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

import datetime

from astropy.coordinates import EarthLocation
from astropy.time import Time
from astropy import units as u

# observing_location = EarthLocation(lat=46.57*u.deg, lon=7.65*u.deg)
# observing_time = Time(datetime.datetime.utcnow(), scale='utc', location=observing_location)
# LST = observing_time.sidereal_time('mean')


@app.route('/<lat>/<long>')
def showlatLong(lat, long):
    print(lat, long)
    lon = float(long)*u.degree
    lat = float(lat)*u.degree
    # show the user profile for that user
    # return f'{lat}, {long}'

    observing_location = EarthLocation(lat=lat, lon=lon)
    observing_time = Time(datetime.datetime.utcnow(), scale='utc', location=observing_location)
    LST = observing_time.sidereal_time('mean')
    print(LST.degree)

    coord = SkyCoord(ra=LST.degree, dec=lat, unit=(u.degree, u.degree), frame='icrs')
    width = u.Quantity(10, u.arcmin)
    height = u.Quantity(10, u.arcmin)
    r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
    r.sort('phot_g_mean_mag')
    # r.sort('ref_epoch')

    nameOfStar = r['DESIGNATION'][0]
    starRA = r['ra'][0]
    starDEC = r['dec'][0]
    newCoord = SkyCoord(ra=starRA, dec=starDEC, unit=(u.degree, u.degree), frame='icrs')
    images = SkyView.get_images(newCoord, survey=['DSS'], radius=u.Quantity(2, u.arcmin), grid=True, gridlabels = True, pixels=300)
    # return images[0][0].data
    plt.imshow(images[0][0].data, cmap='cubehelix')
    # plt.title(f"Name of star:\n{nameOfStar}")
    
    # get rid of axes etc
    plt.axis('off')
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
              hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    

    # buffer it??
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
    
    # close fig
    plt.close() 
    buf.seek(0)

    # Send buffer 
    print("sending image back")
    return send_file(buf, mimetype='image/png')
    # # plt.figtext(0.5, 0.08, f"References to star found: {ref_count} \n asc: {starRA} desc: {starDEC}", ha="center", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
    # # ax.add_patch(rect)
    # # plt.annotate(0,0,f"References to star found: {result} \n asc: {starRA} desc: {starDEC}")
    # # plt.show()
    return 'done'

    # output = io.BytesIO()
    # FigureCanvas(plt).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, port=8001)