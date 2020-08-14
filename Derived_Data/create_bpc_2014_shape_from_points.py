# From https://glenbambrick.com/2016/01/09/csv-to-shapefile-with-pyshp/

# import libraries
import shapefile
import csv
try:
    import tkinter as tk   # Python 3
except:
    import Tkinter as tk   # Python 2
        


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
with open('BPC 2014 Water Quality ccb for analysis.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    # skip the header
    header = next(reader, None)
    print(header)

    types  = [('C', 15, 0), ('N',12,6), ('N',12,6), ('N',8,5), ('N',8,5),
              ('N',8,5), ('N',8,5), ('N',8,5), ('N',8,5), ('N',8,5), ('N',8,5),
              ('N',8,5), ('N',8,5), ('N',8,5), ('N',8,5), ('N',8,5)]
    
    t,l,d = zip(*types)
    p = zip(header,t,l,d)
#    for  i in p:
#        print(i)
    
    #Character, Numbers, Longs, Dates, or Memo

## Create the field names and data type for each.
    for item in p:
        if item[0]:
                bpc_shp.field(item[0], item[1], item[2], item[3])

##loop through each of the rows and assign the attributes to variables
    # count the features
    counter = 0
    for row in reader:
        # the following explicit aproach is for Python 2
        Town = row[0]
        Latitude = row[1]
        Longitude = row[2]
        Coarse = row[3]
        Sand= row[4]
        Silt = row[5]
        Clay = row[6]
        TOC = row[7]
        Moisture = row[8]
        Bifenthrin_Raw = row[9]
        Bifenthrin = row[10]
        Cypermethrin = row[11]
        BTU_H = row[12]
        BTU_E = row[13]
        CTU_H = row[14]
        CTU_E = row[15]									

        counter += 1
#       # create the point geometry
        bpc_shp.point(float(Longitude),float(Latitude))
#       # add attribute data
#       bpc_shp.record(*row)   # requires Python 3
        bpc_shp.record(Town, Latitude, Longitude, Coarse, Sand, Silt, Clay,
                       TOC, Moisture, Bifenthrin_Raw, Bifenthrin, Cypermethrin,
                       BTU_H, BTU_E, CTU_H, CTU_E)

        print "Feature " + str(counter) + " added to Shapefile."
#
# save the Shapefile
bpc_shp.save("BPC_Locations.shp")

# create a projection file
with open("BPC_Locations.prj", "w") as prj:
    epsg = getWKT_PRJ("4979")  # Should be WGS 84  alt: 4326
    prj.write(epsg)
    