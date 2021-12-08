Load Pesticides Data And Report out Summary Bifenthrin Data
================
Curtis C. Bohlen, Casco Bay Estuary Partnership

-   [Introduction](#introduction)
    -   [Sediment Data](#sediment-data)
    -   [Stormwater Samples](#stormwater-samples)
-   [Load Libraries](#load-libraries)
-   [Load Data](#load-data)
    -   [File References](#file-references)
    -   [Load IC Data](#load-ic-data)
    -   [Load Pyrethroid Concentration
        Data](#load-pyrethroid-concentration-data)
    -   [Load Stormwater Data](#load-stormwater-data)
-   [Calculate Sediment Site Bifenthrin
    Averages](#calculate-sediment-site-bifenthrin-averages)
    -   [Correlations](#correlations)
    -   [Export summary table](#export-summary-table)
-   [Import IC metrics into
    conc\_data](#import-ic-metrics-into-conc_data)

<img
    src="https://www.cascobayestuary.org/wp-content/uploads/2014/04/logo_sm.jpg"
    style="position:absolute;top:10px;right:50px;" />

# Introduction

This notebook prepares BPC Pesticides data from Casco Bay for further
analysis.

## Sediment Data

In 2014 and 2015, the Maine Board of Pesticides Control collected
sediment samples from the Coast of Maine and Casco Bay, and analyzed
them for presence of selected pesticides, especially certain pyrethroid
pesticides.

The only pyrethroid that was observed consistently was bifenthrin,
perhaps because bifenthrin could be detected in sediment samples at
substantially lower concentrations than the other pesticides on the
testing panel. Concentrations (expressed on organic carbon weighted
basis) were on the order of one and a half to two orders of magnitude
below LC50 values for two species of crustaceans for which sediment
toxicity data were available.

Our principal goal is to produce a MAP of average bifenthrin
concentrations and a FIGURE showing the relationship between bifenthrin
concentration and extent of nearby impervious surfaces (as a rough
measure of urbanization).

## Stormwater Samples

In 2015, the BPC collected stormwater samples from streams and storm
drain outfalls near where sediment samples were collected in 2014. These
samples were analyzed both for pyrethroids and for a comprehensive list
of 101 pesticides (see ‘Anylate\_Lists\_2010.xlsx’), including
insecticides, herbicides, and fungicides. The list of pesticides does
not include banned organochlorine pesticides like DDT and Chlordane, but
focuses on pesticides in present-day use, many of which are thought to
have relatively short lifespans in the aquatic environment.

# Load Libraries

``` r
library(tidyverse)
```

    ## Warning: package 'tidyverse' was built under R version 4.0.5

    ## -- Attaching packages --------------------------------------- tidyverse 1.3.1 --

    ## v ggplot2 3.3.5     v purrr   0.3.4
    ## v tibble  3.1.6     v dplyr   1.0.7
    ## v tidyr   1.1.4     v stringr 1.4.0
    ## v readr   2.1.0     v forcats 0.5.1

    ## Warning: package 'ggplot2' was built under R version 4.0.5

    ## Warning: package 'tidyr' was built under R version 4.0.5

    ## Warning: package 'dplyr' was built under R version 4.0.5

    ## Warning: package 'forcats' was built under R version 4.0.5

    ## -- Conflicts ------------------------------------------ tidyverse_conflicts() --
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

``` r
library(GGally)
```

    ## Warning: package 'GGally' was built under R version 4.0.5

    ## Registered S3 method overwritten by 'GGally':
    ##   method from   
    ##   +.gg   ggplot2

``` r
library(CBEPgraphics)
load_cbep_fonts()

library(LCensMeans)
```

# Load Data

## File References

``` r
conc_fn <- 'BPC_2014_2015_Sediment_Data.txt'
geogr_fn <- 'imperviousness.txt'
storm_fn <- 'BPC_2015_Stormwater_Data.txt'
```

## Load IC Data

Note that the total IC coverage listed includes IC within the designated
radius of the sample point. Since each sample point is on a shoreline, a
portion of that circle lies in the ocean, and is not on land. Thus the
percent imperviousness calculated here (based on the TOTAL area of those
circles, not the LAND area within those circles) underestimates local
IC, but provides a better estimate of the potential impact of overall
urbanization on local conditions.

``` r
ic_data <- read.delim(geogr_fn, sep = ',') %>%
  select(-OBJECTID, -Latitude, -Longitude) %>%
  rename(yr = 'Year_') %>%
  mutate(pctI500 = imperv500 / (pi*500^2),
         pctI1000 = imperv1000 / (pi*1000^2),
         pctI2000 = imperv2000 / (pi*2000^2)) %>%
  filter(Location != 8)       # Remove Boothbay Location
```

## Load Pyrethroid Concentration Data

``` r
conc_data <- read.delim(conc_fn, skip = 1) %>%
  select(1:15)
```

## Load Stormwater Data

While we load the Stormwater Data, data is from a handful of sites, and
we observe only a handful of pesticides regularly. We do not conduct any
further analysis with it here

The most frequently observed pesticides are

``` r
storm_data <- read.delim(storm_fn, skip = 1)
```

# Calculate Sediment Site Bifenthrin Averages

Here we use a function from CBEP’s LCensMeans package to estimate the
maximum likelihood value of the (unobserved) concentrations in
non-detects. It offers a statistically better justified estimate than
replacing non-detects with the detection or reporting limit.

We calculate site averages, effectively pooling results from multiple
samples from individual sampling locations. This hides temporal trends,
but is just what we need to prepare GIS maps.

Note that one of two Little Flying Point replicates was a non-detect,
the other was not, so pooling the two values is problematic. We proceed
anyway.

``` r
avg_data <- conc_data %>%
  group_by(LocCode) %>%
  summarize(across(Coarse:BTU_E, mean, na.rm=TRUE), .groups='drop') %>%
  mutate(Bifenthrin_ND = Bifenthrin_ND>0) %>%
  mutate(pct500   = ic_data$pctI500[match(LocCode, ic_data$Location)],
         pct1000  = ic_data$pctI1000[match(LocCode, ic_data$Location)],
         pct2000  = ic_data$pctI2000[match(LocCode, ic_data$Location)])


ml_estimator_Raw <- sub_cmeans(avg_data$Bifenthrin_Raw,
                                               avg_data$Bifenthrin_ND)
avg_data <- avg_data %>%
  mutate(Bifenthrin_ML     = ml_estimator_Raw) %>%
  mutate(Bifenthrin_OC_QML = Bifenthrin_ML * 100* (100/(100-Moisture)) / TOC)
```

## Correlations

``` r
cor(avg_data[c(8, 10, 2:7)], use = 'pairwise')
```

    ##                Bifenthrin_Raw Bifenthrin_OC     Coarse       Sand       Silt
    ## Bifenthrin_Raw      1.0000000     0.8934583 -0.3699136 -0.4256472  0.5009337
    ## Bifenthrin_OC       0.8934583     1.0000000 -0.3289451 -0.1211026  0.2303410
    ## Coarse             -0.3699136    -0.3289451  1.0000000  0.3206778 -0.5881366
    ## Sand               -0.4256472    -0.1211026  0.3206778  1.0000000 -0.9463166
    ## Silt                0.5009337     0.2303410 -0.5881366 -0.9463166  1.0000000
    ## Clay                0.4207935     0.1647330 -0.6134993 -0.9097272  0.9345921
    ## TOC                 0.6468131     0.3412946 -0.4561349 -0.8339714  0.8670606
    ## Moisture            0.6087258     0.3176551 -0.4874381 -0.8312350  0.8720723
    ##                      Clay        TOC   Moisture
    ## Bifenthrin_Raw  0.4207935  0.6468131  0.6087258
    ## Bifenthrin_OC   0.1647330  0.3412946  0.3176551
    ## Coarse         -0.6134993 -0.4561349 -0.4874381
    ## Sand           -0.9097272 -0.8339714 -0.8312350
    ## Silt            0.9345921  0.8670606  0.8720723
    ## Clay            1.0000000  0.7892633  0.8043373
    ## TOC             0.7892633  1.0000000  0.9396898
    ## Moisture        0.8043373  0.9396898  1.0000000

As expected, Bifenthrin concentrations are positively correlated with
silt, clay, total organic carbon, and moisture. The pesticide is
concentrated in depositional environments. Conversely, it is negatively
correlated with sand.

``` r
cor(avg_data[c(8, 10, 13:15)], use = 'pairwise', method = 'pearson')
```

    ##                Bifenthrin_Raw Bifenthrin_OC    pct500   pct1000   pct2000
    ## Bifenthrin_Raw      1.0000000     0.8934583 0.7642628 0.6922496 0.6253453
    ## Bifenthrin_OC       0.8934583     1.0000000 0.7772502 0.7296783 0.6727516
    ## pct500              0.7642628     0.7772502 1.0000000 0.9710473 0.8962388
    ## pct1000             0.6922496     0.7296783 0.9710473 1.0000000 0.9619669
    ## pct2000             0.6253453     0.6727516 0.8962388 0.9619669 1.0000000

The correlations with the IC metrics are important. The radius around
each sampling point makes only a small difference in the correlation.
Repeating the analysis with Spearman’s Rank Correlations or Kendall’s
Tau does not change the general conclusions (not shown).

## Export summary table

``` r
avg_data %>% select(-BTU_E, -BTU_H, - pct500, -pct1000, -pct2000) %>%
  write_csv('bifenthrin_by_site.csv')
```

# Import IC metrics into conc\_data

``` r
ml_estimator_Raw <- sub_cmeans(conc_data$Bifenthrin_Raw,
                                               conc_data$Bifenthrin_ND)

conc_data <- conc_data %>%
  mutate(pct500   = ic_data$pctI500[match(LocCode, ic_data$Location)],
         pct1000  = ic_data$pctI1000[match(LocCode, ic_data$Location)],
         pct2000  = ic_data$pctI2000[match(LocCode, ic_data$Location)]) %>%
  mutate(Bifenthrin_ML = ml_estimator_Raw) %>%
  mutate(Bifenthrin_OC_QML = Bifenthrin_ML * 100* (100/(100-Moisture)) / TOC)
```
