# Derived Data on Pesticide LEvels
We edited the raw data provided by the BPC staff by hand to generate simplified data files (mostly as /*.txt files) as follows:

*  BPC_2014_Sediment_Locations.txt  
*  BPC_2015_Sediment_Locations.txt  
*  BPC_20154_Stormwater_Locations.txt  
*  BPC_2014_2015 _Sediment_Data.txt
*  Analyte Lists 2015.xlsx
*  Analyte List Sediments.xlsx

Data follows CBEP convention by including detection / reporting limits and observed values in a single data column, with a separate column containing a flag that indicates which locations are non-detects.

For these data, that is problematic, as detection/reporting limits are based on analysis of whole samples (wet weight) while toxicity is more closely aligned with concentration of the pesticides as a fraction of (dr) organic-matter.  We conducted calculations (of dubious value) of  the OC weighted concetration even for non-detects, but we did not calculate toxicity scores for non-detects.

# Location Codes
Arbitrary numerical codes were given to each location within the Sediment Samples data, to facilitate analysis and joinng tabular toGIS data.

#  Point Locations of Samples
GIS location estimates for sample collection were derived from lat-long data in the excel and text files. We assumed geographic locations of samples were collected in the fields using GPS (as was true for sampling that CBEP staff supported in 2015), and thus are all expressed is in WGS 1984 coordinates

1.  Data including spatial coordinates were exported to txt files.  
2.  Sediment Location Files data was converted to Shapefiles using simple python scripts  
  -   "create bpc 2015 shape from points.py"  
  -   "create bpc 2014 shape from points.py"  
3. Files were combined in ArcGiS, and saved in a personal geodatabase (GIS_Files.mdb)  
4.  2015 Stormwater Sample Locations were read directly into ArcGIS as an event layer, exported as a Feature Class in the Geodatabase.  All sample points ouside the Casco BAy region were deleted.  

#  Near Impervious Cover Estimates
Impervious cover estimates (calculated only for sedimetn sample locations) were based on Maine  IF&W one meter pixel impervious cover data, which is based largely on data from 2007.  CBEP has a version of this impervious cover data for the Casco Bay watershed towns in our GIS data archives. Analysis followed the following steps.  (Some of these steps only speed up analysis).

1. We created a polygon that enclosed all of the Casco Bay sample locations and a 2000 meter buffer around each.  Because outr version of the IMpervious Cover layer is limited to Casco Bay Watershed Towns, we can not develop impervious cover statistics for nearby sites outside the watershed towns. 

2.  We used "Extract by Mask" to extract a smaller version of the impervious cover data for just that region. 

3.  We used "Aggregate" to reduce the resolution of the impervious cover raster to a 5 meter resolution, summing the total impervious cover within the 5m x 5 m area, generating a raster with values from zero to 25. 

4.  We used "Focal Statistics" to generate rasters that show the cummulative area of impervious cover (in meters) within 500 m, 1000m and 2000m. 

5.  Finally, we extracted the values of the three rasters produced in step 4 at each of the sample locations.  We used  'Extract Multi Values to Points'.  

6. Impervious cover data was exported in a text file "imperviousness.txt"

# Generation of simplified Data
Some replicate sediment samples were collected at certail locations, either replicates at one sample event, or replicates at different times of year.  here we want to report only single values for each sample location.  Averages are calculated with the script
