# Derived Data on Pesticides in Casco Bay Sediments
We edited the raw data provided by the BPC staff by hand in Excel to produce
simplified data files (mostly as /*.txt files).  We separated multiple tabs in
excel files, deleted data for pesticides that were never detected in Casco Bay,
and deleted data from areas outside of Casco Bay.

## Geospatial data
### `BPC_2014_Sediment_Locations.txt` 
### `BPC_2015_Sediment_Locations.txt`

Column Name     | Contents                               | Units                         
----------------|----------------------------------------|------
Map Key	(Sometimes unnamed) | Arbitrary Numerical Location Code  | Integer
Town	          | LOCATION  name (not just town name)    | String
Latitude	       | Longitude, WGS 1984                    | decimal degrees
Longitude       | Latitude, WGS 1984                     | decimal degrees


##  Near Impervious Cover Estimates
Impervious cover estimates (calculated only for sediment sample locations in
Casco Bay) were based on Maine IF&W one meter pixel impervious cover data,
which is based largely on data from 2007.  CBEP has a version of this impervious
cover data for the Casco Bay watershed towns in our GIS data archives.

### `imperviousness.txt`
The values in this file represent the cumulative impervious cover within a given
distance of each sample locations.  Note that this is NOT scaled to the 
nearby land area, and thus does not correspond to the way watershed analysis
usually measures imperviousness. The rationale for this non-standard useage is
that we are interested in a metric of "nearby urban" land use, and a coastal 
site with a lot of water nearby is, in some measure, less "urban" than a site 
surrounded by lots of urban land.

Column Name  | Contents                          
-------------|------------------------------------------------------------
OBJECTID     | Arbitrary ID number added by ArcGIS
Town         | The name of the sampling location (more specific than town)
Latitude     | Latitude, WGS 1984, decimal degrees
Longitude    | Longitude, WGS 1984, decimal degrees
Year_        | Year of sample collection.
Location     | Numerical ID code, to facilitate database joins in GIS
imperv500    | Impervious area within a 500 meter circle of sampling point, in square meters
imperv1000   | Impervious area within a 1000 meter circle of sampling point, in square meters
imperv2000   | Impervious area within a 2000 meter circle of sampling point, in square meters

##Sediment Pesticide Data
### `BPC_2014_2015_Sediment_Data.txt`
Data derived from excel spreadsheets provided to CBEP by BPC staff.  Data
contains data on concentration of pesticides in sediment samples, expressed on a
wet weight basis.  Data omits pesticides that were never detected.  For a full 
list of analytes in the study, see `Analyte_List_Sediments.xlsx`, which also 
includes detection limits.

Only bifenthrin was detected often enough to provide useful
data for analysis. The detection limit for bifenthrin was a factor of five or
more lower than for the other pesticide in the study, so lack of detection for
most other compounds may reflect more challenging analytic chemistry.

Column Name | Contents                                            | Units                         
------------|-----------------------------------------------------|-----------
LocCode     | Arbitrary numerical Location Code  | Integer
Location_Descr | Name of Sampling location (Does not fully match "Town" from the geospatial data tables.  | String
Date        | Date of Sample, for sites with multiple samples  | mm/dd/yyyy
Year        | Year of saple collection  | Integer
Coarse      | Percent coarse particles (> Sand) in sediment sample  |  Percent
Sand        | Percent sand particles in sediment sample  |  Percent
Silt        | Percent silt particles  in sediment sample  |  Percent
Clay        | Percent clay particles  in sediment sample  |  Percent
TOC         | Percent total organic carbon  |  Percent
Moisture    | Percent moisture  |  Percent
Bifenthrin_Raw | Concentration of Bifenthrin in sample (wet weight basis).  ND represented by their detection limits.  | ng/g wet
Bifenthrin_ND  | Logical flag identifying non-detects, to allow different analysis conventions  | TRUE or FALSE
Bifenthrin_OC  | Concentration of Bifenthrin as a fraction of the organic matter in the sample .  ND represented by their detection limits.     | ng/g OC dry
BTU_H       | Bifenthrin concentration as a fraction of the LD50 for Hyalella azteca, a freshwater amphipod  | fraction of LD50
BTU_E       | Bifenthrin concentration as a fraction of the LD50 for Eohaustorius estuarius , a marine amphipod  | fraction of LD50
Cypermethrin_RAW | Concentration of Cypermethrin in sample  (wet weight basis).  ND represented by their detection limits.  | ng/g wet
Cypermethrin_ND  | Logical flag identifying non-detects, to allow different analysis conventions  | T/F
Cypermethrin_OC  | Concentration of Cypermethrin as a fraction of the organic matter in the sample .  ND represented by their detection limits.  | ng/g OC dry
CTU_H       | Cypermethrin concentration as a fraction of the LD50 for Hyalella azteca, a freshwater amphipod  | fraction of LD50
CTU_E       | Cypermethrin concentration as a fraction of the LD50 for Eohaustorius estuarius , a marine amphipod  | fraction of LD50
Fenvalerate_RAW | Concentration of Fenvalerate in sample  (wet weight basis).  ND represented by their detection limits.  | ng/g wet
Fenvalerate_ND  | Logical flag identifying non-detects, to allow different analysis conventions  | TRUE or FALSE
Fenvalerate_OC  | Concentration of Fenvalerate as a fraction of the organic matter in the sample .  ND represented by their detection limits.     | ng/g OC dry
FTU_H       | Fenvalerate concentration as a fraction of the LD50 for Hyalella azteca, a freshwater amphipod  | fraction of LD50
FTU_E       | Fenvalerate concentration as a fraction of the LD50 for Eohaustorius estuarius , a marine amphipod	fraction of LD50

Data for pesticides that were observed at levels above the reporting limits at
least twice were split into two data columns, following CBEP convention.  The
first data column includes detection / reporting limits and observed values in a
single data column.  The second column containing a TRUE / FALSE flag that 
indicates which samples were non-detects.

Detection/reporting limits are based on analysis of whole samples (wet weight)
while toxicity is more closely aligned with concentration of the pesticides as a
fraction of (dry) organic-matter.  We conducted calculations (of dubious value)
of  the OC weighted concentration even for non-detects, but we did not calculate
toxicity scores for non-detects.

### `bifenthrin_by_site.csv`
Some replicate sediment samples were collected at certain locations, either
replicates durong one sample event, or collections at different times of year.
For GIS display, we want to show average values.  This file shows mean values of
sediment composition and bifenthrin concentration by location. The last two
columns calculate averages based on a maximum likelihood estimator of the
conditional mean for bifenthrin non-detects based on the assumption of a
left-truncated lognormal distribution.  Similar calculation are provided in the
`Pesticide_analysis_sum`.  The actual code we used to develop these estimates 
is available in file `prepare data.Rmd` in the accompanying detailed 
[GitHub archive](https://github.com/CBEP-SoCB-Details/BPC_Pesticides.git)

Column Name | Contents                                                                   
------------|-----------------------------------------------------
LocCode     | Arbitrary numerical Location Code 
Coarse      | Percent coarse particles (> Sand) in sediment sample 
Sand        | Percent sand particles in sediment sample 
Silt        | Percent silt particles  in sediment sample 
Clay        | Percent clay particles  in sediment sample 
TOC         | Percent total organic carbon  
Moisture    | Percent moisture 
Bifenthrin_Raw | Arithmetic mean of Bifenthrin values (with non detects at detection limit)
Bifenthrin_ND  | TRUE / FALSE value. TRUE if any observations in the mean were non-detects
Bifenthrin_OC  | Arithmetic mean of bifentrin expressed on an organic carbon basis (with non detects at detection limit)
Bifenthrin_ML  | Arithmetic mean of Bifenthrin values (with non detects at maximum likelihood estimate of expected value of censored values)
Bifenthrin_OC_QML | Arithmetic mean of bifentrin expressed on an organic carbon basis (with non detects converted to maximum likelihood estimate of expected value of censored values before rescaling to OC basis).


### `Analyte_List_Sediments.xlsx`
A list of the active ingredients tested for in sediment samples.  Most were 
never detected, but note the relatively high detection limits of some compounds.

Column Name             | Contents                                                           
------------------------|---------------------------------
Pesticide               | Active Ingredient, common name  
Reporting Limit (ug/kg) | Just what is says.

PBO = Piperonyl butoxide, a chemical which enhances the activity of pyrethroid 
pesticides, and so is often a component of pesticide formulations. 

# GIs Data
### Shapefile `BPC_Sediment_Locations

These data are based on `imperviousness.txt`

Column Name  | Contents                          
-------------|------------------------------------------------------------
Year_        | Year of sample collection.
Location     | Numerical ID code, to facilitate database joins in GIS
imperv500    | Impervious area within a 500 meter circle of sampling point, in square meters
imperv1000   | Impervious area within a 1000 meter circle of sampling point, in square meters
imperv2000   | Impervious area within a 2000 meter circle of sampling point, in square meters
