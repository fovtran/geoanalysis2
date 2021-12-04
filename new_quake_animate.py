# diego
from geoanalysistools.geo import *
from numba import vectorize

df = gpd.read_file( 'data/lapalma-datetime-slice.geojson', driver="GeoJSON" )
df[["Date"]] = df[["Date"]].apply(pd.to_datetime)
gdf = GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitud, df.latitud))
#df2 = pd.DataFrame( {'Vents': ['Vent 1'], 'Name': ['Dolly'], 'latitud': [28.58], 'longitud': [-17.84]} )

R={}
if False:
    for i, d in enumerate( gdf.Date ):
        next = []
        if d in R:
            prev = R[d]
            data = gdf.loc[ gdf['Date'] == d ].evid.values
            if prev is not None:
                R[d] = prev.append(data)
        else:
            print("adding ", d)
            data = gdf.loc[ gdf['Date'] == d ].evid.values
            R[d] = next.append( data )

#with moviewriter.saving(fig, 'myfile.mp4', dpi=100):
#    for j in range(n):
#        update_figure(j)
#        moviewriter.grab_frame()

class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, numpoints=50):
        self.numpoints = numpoints
        self.stream = self.data_stream()
        self.fig, self.ax = plt.subplots()
        self.data = []
        self.frames = df.groupby(pd.Grouper(key='Date', freq='1D'))
        self.ani = FuncAnimation(self.fig, self.update, frames=self.frames, init_func=self.setup_plot, interval=100, blit=False)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        self.scat = self.ax.plot([], [], c='r')
        #self.scat = self.ax.scatter([], [], c='r', s=2, vmin=0, vmax=1, cmap="jet", edgecolor="k")
        #self.ax.axis([gdf.latitud.min(), gdf.longitud.min(), gdf.latitud.max(), gdf.longitud.max()])
        return self.scat,

    def data_stream(self):
        xy = (xdata, ydata)
        while False:
            yield xy

    def update(self, i):
        """Update the scatter plot."""
        xdata, ydata = [],[]
        for evid in i[1].Date.values:
            ev = df.loc[ gdf.Date == evid ]
            xdata.append(ev['longitud'].to_numpy())
            ydata.append(ev['latitud'].to_numpy())

        print(xdata)
        self.data = (xdata, ydata)
        self.scat.set_data(self.data)

        #self.scat.set_offsets(self.data)
        # Set sizes...
        #self.scat.set_sizes(300 * abs(data[:, 2])**1.5 + 100)
        # Set colors..
        #self.scat.set_array(data[:, 3])
        return self.scat,


if __name__ == '__main__':
    a = AnimatedScatter()
    plt.show()
