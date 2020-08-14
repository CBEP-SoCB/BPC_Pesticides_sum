# Started with an example from From https://glenbambrick.com/2016/01/09/csv-to-shapefile-with-pyshp/

# import libraries
import shapefile
import csv


# funtion to generate a .prj file
def getWKT_PRJ (epsg_code):
    import urllib
    wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    remove_spaces = wkt.read().replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output

# create a point shapefile
bpc_shp = shapefile.Writer(shapefile.POINT)

# for every record there must be a corresponding geometry.
bpc_shp.autoBalance = 1


# access the CSV file
with open('BPC 2015 Water Quality Sampling Locations.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    # skip the header
    header = next(reader, None)
    print(header)
    header[0] = ''

    types  = [('N', 4, 0), ('C',20,0), ('N',8,5), ('N',8,5)]
    
    t,l,d = zip(*types)
    p = zip(header,t,l,d)
#    for  i in p:
#        print(i)
    
    #Character, Numbers, Longs, Dates, or Memo

## Create the field names and data type for each.
    for item in p:
        if item[0]:
                bpc_shp.field(item[0], item[1], item[2], item[3])
                item[0], item[1], item[2], item[3]

##loop through each of the rows and assign the attributes to variables
    # count the features
    counter = 0
    for row in reader:
       # print row[1], row[2], row[3]
        # the following explicit aproach is for Python 2
        Key = row[0]
        Town = row[1]
        Latitude = row[2]
        Longitude = row[3]

#       # create the point geometry
        bpc_shp.point(float(Longitude),float(Latitude))
#       # add attribute data
#       bpc_shp.record(*row)   # requires Python 3
        bpc_shp.record(Town, Latitude, Longitude)

        print "Feature " + str(counter) + " added to Shapefile."
#
# save the Shapefile
bpc_shp.save("BPC_2015_Locations.shp")

# create a projection file
with open("BPC_2015_Locations.prj", "w") as prj:
    epsg = getWKT_PRJ("4979")  # Should be WGS 84  alt: 4326
    prj.write(epsg)
    