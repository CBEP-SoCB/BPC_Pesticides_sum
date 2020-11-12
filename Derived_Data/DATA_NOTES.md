# Derived Data on Pesticides in Casco Bay Sediments
We edited the raw data provided by the BPC staff by hand in Excel to produce
simplified data files (mostly as /*.txt files).  We separated multiple tabs in
excel files, deleted data for pesticides that were never detected in Casco Bay,
and deleted data from areas outside of Casco Bay.

Resulting data files include the following:  
*  BPC_2014_Sediment_Locations.txt  
*  BPC_2015_Sediment_Locations.txt  
*  BPC_2015_Stormwater_Locations.txt  
*  BPC_2014_2015_Sediment_Data.txt
*  BPC_2015_Stormwater_Data.txt
*  Analyte_Lists_2015.xlsx
*  Analyte_List_Sediments.xlsx

The most important of these are:  
*  BPC_2014_2015_Sediment_Data.txt  
*  BPC_2015_Stormwater_Data.txt 

Data for pesticides that were observed at levels above the reporting limits at
least twice were split into two data columns, following CBEP convention.  The
first data column includes detection / reporting limits and observed values in a
single data column.  The second column containing a T/F flag that indicates
which locations are non-detects.

For these data, that is problematic, as detection/reporting limits are based on
analysis of whole samples (wet weight) while toxicity is more closely aligned
with concentration of the pesticides as a fraction of (dry) organic-matter.  We
conducted calculations (of dubious value) of  the OC weighted concentration even
for non-detects, but we did not calculate toxicity scores for non-detects.

## Location Codes
Unique numerical Location Codes were given to each sampling location within the
Sediment Samples data, to facilitate analysis and joining tabular to GIS data.

#  Point Locations of Samples
GIS location estimates for sample collection were derived from lat-long data in
the excel and text files. We assumed geographic locations of samples were
collected in the fields using GPS (as was true for sampling that CBEP staff
supported in 2015), and thus are all expressed is in WGS 1984 coordinates.

1.  Data including spatial coordinates were exported to /*.txt files.  
2.  Sediment Location Files data was converted to Shapefiles using python  
  -   "create_bpc_2015_shape_from_points.py"  
  -   "create_bpc_2014_shape_from_points.py"  
3.  Sediment location shapefiles were combined into a single layer in ArcGiS,
    and saved in a personal geodatabase ('GIS_Files.mdb').  
4.  Each Sampling location was given a unique numerical site ID to facilitate
    joins with the pesticide data in ArcGIS.  
5.  2015 Stormwater Sample Locations were read directly into ArcGIS as an event
    layer, exported as a Feature Class in the Geodatabase.

#  Near Impervious Cover Estimates
Impervious cover estimates (calculated only for sediment sample locations) were
based on Maine  IF&W one meter pixel impervious cover data, which is based
largely on data from 2007.  CBEP has a version of this impervious cover data for
the Casco Bay watershed towns in our GIS data archives. Analysis followed the
following steps (Some of these steps only speed up analysis). 

1. Town by town IC data in a Data Catalog were assembled into a large `tif` 
   file using the "Mosaic Raster Catalog"  item from teh context menu fro the
   ArcGIS table of contents.

2. We created a polygon that enclosed all of the Casco Bay sample locations and
   a 2000 meter buffer around each.  Because our version of the Impervious Cover
   layer is limited to Casco Bay Watershed Towns, we can not develop impervious
   cover statistics for nearby sites outside the watershed towns. 

3. We used "Extract by Mask" to extract a smaller version of the impervious
   cover data for just our coastal region.  

4. We used "Aggregate" to reduce the resolution of the impervious cover raster
   to a 5 meter resolution, summing the total impervious cover within the
   5m x 5 m area, generating a raster with values from zero to 25. 

5. We used "Focal Statistics" to generate rasters that show the cumulative area
   of impervious cover (in meters) within 500 m, 1000m and 2000m. 

6. Finally, we extracted the values of the three rasters produced in step 4 at
   each of the sample locations.  We used  'Extract Multi Values to Points'. 

7. Impervious cover data was exported in a text file "imperviousness.txt".

Calculation of "percent imperviousness" values wwas conducted in the R notebook,
`Prepare_)Data.Rmd`. The percent imperviousness values are based on the TOTAL
area of a circle with the specified radius of each sampling location, not the
LAND area within that radius.  We believe that method provides a better synoptic
assessment of urbanization near sampling locations.

# Generation of Simplified Data
Some replicate sediment samples were collected at certain locations, either
replicates at one sample event, or replicates at different times of year.  For
GIS display, we want to show average values.   Averages are calculated with the
R Notebook 'Prepare_Data.Rmd.'  The output file is called
'bifenthrin_by_site.csv.'


