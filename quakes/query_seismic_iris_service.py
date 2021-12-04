# valores normalizados se llama eso,
# no es algo de otro mundo

norte = "18d 16min 16seg WEST - 28d 59min 20sec NORTH"
sur = "17d 26min 40sec WEST - 28d 16min 44sec NORTH"
# maxlat=28.984&minlon=-18.237&maxlon=-17.364&minlat=28.212
query = "https://service.iris.edu/fdsnws/event/1/query?includeallorigins=false&includeallmagnitudes=false&includearrivals=false&orderby=time&format=xml&maxlat=28.984&minlon=-18.237&maxlon=-17.364&minlat=28.212&nodata=404&limit=20&offset=2"

root = savexml(query)

for elem in root.getiterator():
    # Skip comments and processing instructions,
    # because they do not have names
    if not (
        isinstance(elem, etree._Comment)
        or isinstance(elem, etree._ProcessingInstruction)
    ):
        # Remove a namespace URI in the element's name
        elem.tag = etree.QName(elem).localname
