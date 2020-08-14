Load Pesticides Data And Report out SUmamry Bifenthrin Data
================
Curtis C. Bohlen, Casco Bay Estuary Partnership

  - [Introduction](#introduction)
  - [Load Libraries](#load-libraries)
  - [Load Data](#load-data)
      - [Folder References](#folder-references)
      - [Load Stormwater Data](#load-stormwater-data)
          - [What Pesticides Were Detected in
            Stormwater?](#what-pesticides-were-detected-in-stormwater)
          - [Maximum Observed Value and Approcximate Number of
            Detections](#maximum-observed-value-and-approcximate-number-of-detections)
      - [Related Aquatic Life
        Benchmarks](#related-aquatic-life-benchmarks)
  - [Summary of Caso Bay
    Observations](#summary-of-caso-bay-observations)
  - [Results](#results)

<img
    src="https://www.cascobayestuary.org/wp-content/uploads/2014/04/logo_sm.jpg"
    style="position:absolute;top:10px;right:50px;" />

# Introduction

in 2015, the BPC collected stormwater samples from streams and storm
drain outfalls near where sediment samples were collected in 2014. These
samples were analyzed both for pyrethroids and for a comprehensive list
of 101 pesticides (see ‘Anylate\_Lists\_2015.xlsx’), including
insecticides, herbicides, and fungicides. The list of pesticides does
not include banned organochlorine pesticides like DDT and chlordane, but
focuses on pesticides in present-day use, many of which are thought to
have relatively short lifespans in the aquatic environment.

# Load Libraries

``` r
library(tidyverse)
```

    ## -- Attaching packages --------------------------------------------------------------------------------------------------- tidyverse 1.3.0 --

    ## v ggplot2 3.3.2     v purrr   0.3.4
    ## v tibble  3.0.3     v dplyr   1.0.0
    ## v tidyr   1.1.0     v stringr 1.4.0
    ## v readr   1.3.1     v forcats 0.5.0

    ## -- Conflicts ------------------------------------------------------------------------------------------------------ tidyverse_conflicts() --
    ## x dplyr::filter() masks stats::filter()
    ## x dplyr::lag()    masks stats::lag()

# Load Data

## Folder References

``` r
sibfldnm <- 'Derived_Data'
parent   <- dirname(getwd())
sibling  <- file.path(parent,sibfldnm)

fn    <- 'BPC_2015_Stormwater_Data.txt'
fpath <- file.path(sibling,fn)
```

## Load Stormwater Data

``` r
storm_data <- read.delim(fpath, skip = 1)
```

### What Pesticides Were Detected in Stormwater?

Because the two laboratories used different methods for reporting their
results, some of these are below detection limits, an some are below
reporting limits. This serves only as a GENRAL indication of the number
of detections for each pesticide.

``` r
Pesticides <- tibble(Pesticide = names(storm_data)) %>%
  filter(! grepl('ND', Pesticide))  %>%
  filter(! grepl('Flag', Pesticide))  %>%
  filter(c(rep(FALSE,2),rep(TRUE,15))) %>%
 mutate(Pesticide = if_else(Pesticide == 'twofourD', '2,4 D', Pesticide)) %>%
  pull(Pesticide)
knitr:: kable(Pesticides, col.names = c('Pesticide'), caption = 'Pesticides Detected in Stormwater Entering Casco Bay, 2015 BPC Stormwater Study')
```

| Pesticide            |
| :------------------- |
| 2,4 D                |
| Imidacloprid         |
| MCPP                 |
| Metolachlor          |
| Imazapyr             |
| Triclopyr            |
| Hydroxyatrazine      |
| Prometon             |
| Bifenthrin           |
| cis\_Permethrin      |
| trans\_Permethrin    |
| Fipronil             |
| Fipronil\_desulfinyl |
| Fipronil\_sulfide    |
| Fipronil\_sulfone    |

Pesticides Detected in Stormwater Entering Casco Bay, 2015 BPC
Stormwater Study

### Maximum Observed Value and Approcximate Number of Detections

Because of the way the two laboratories reported results, these are not
strictly consistent, but they provide a rough idea of relative abundance
of detects. Number of detects is slightly higher for the first few
pesticides because Montana Laboratory gave the value “Q” for values
above detection limit but below reporting limit, while the other
laboratory offered estimated values, flagged with “J”.

The primary pesticides of concern (based on number of detects) are \*
2,4 D \* Imidacloprid \* MCPP \* Metolachlor \* Bifethrin \* Fipronil
(and its metabolites)

We restrict our focus to them.

## Related Aquatic Life Benchmarks

We can look at EPA Aquatic Life Benchmarks for those pesticides (all in
ug/l) from
[here](https://www.epa.gov/pesticide-science-and-assessing-pesticide-risks/aquatic-life-benchmarks-and-ecological-risk).

``` r
fn    <- 'Aquatic_Life_Benchmarks.txt'
fpath <- file.path(sibling,fn)

ALB_data <- read.delim(fpath, skip=1) %>% select (-Comment)
```

# Summary of Caso Bay Observations

``` r
part1 <- storm_data %>% select(contains('ND')) %>%
  summarize_all(function (x) sum(!x)) %>%
  rename_all(~substr(., 1, nchar(.)-3)) %>%
  rename(`2,4 D` = twofourD) %>%
  t() %>%
  as.data.frame() %>%
  rename(Detects = V1) %>%
 rownames_to_column('Pesticide')

part1 <- part1 %>% filter(Pesticide %in% c('2,4 D', 'Imidacloprid', 'MCPP', 'Metolachlor', 'Bifenthrin', 'Fipronil'))

part2 <- storm_data %>% select(twofourD, Imidacloprid, MCPP, Metolachlor, Bifenthrin, Fipronil) %>%
  mutate(Fipronil = Fipronil / 1000) %>%    # Adjust Units (measured in ng/l)
  summarize_all(function (x) max(x)) %>%
  rename(`2,4 D` = twofourD) %>%
  t() %>%
  as.data.frame() %>%
  rename(`Maximum Concentration` = V1) %>%
  rownames_to_column('Pesticide')

sum_data <- bind_cols(part1, part2) %>% select(-3) %>% rename(Pesticide = Pesticide...1)
```

    ## New names:
    ## * Pesticide -> Pesticide...1
    ## * Pesticide -> Pesticide...3

``` r
options(knitr.kable.NA = '')
left_join(sum_data, ALB_data, by= 'Pesticide') %>%
  knitr::kable(align = "rccrrcccccc", format.args = list(scientific=FALSE))
```

|    Pesticide | Detects | Maximum Concentration |        Type | Fish\_Acute | Fish\_Chronic | InvertAcute | Inver\_Chronic | NonVascular\_Plants | Vascular\_Palnt |
| -----------: | :-----: | :-------------------: | ----------: | ----------: | :-----------: | :---------: | :------------: | :-----------------: | :-------------: |
|        2,4 D |    6    |        4.60000        |   Herbicide |             |               |  12500.000  |                |                     |      299.2      |
| Imidacloprid |    7    |        0.14000        | Insecticide |  114500.000 |    9000.00    |    0.385    |     0.0100     |                     |                 |
|         MCPP |    6    |        1.10000        |   Herbicide |   46500.000 |               |  45500.000  |   50800.0000   |         14          |     1300.0      |
|  Metolachlor |    1    |        0.15000        |   Herbicide |    1900.000 |     30.00     |   550.000   |     1.0000     |          8          |      21.0       |
|   Bifenthrin |    7    |        0.01600        | Insecticide |       0.075 |     0.04      |    0.800    |     0.0013     |                     |                 |
|     Fipronil |    9    |        0.00214        | Insecticide |      41.500 |     2.20      |    0.110    |     0.0110     |         140         |      100.0      |

# Results

  - The MAXIMUM observed stormwater concentration of Imidacloprid
    exceeds the CHRONIC aquatic invertebrate benchmark. So does the
    detection limit….
  - The MAXIMUM observed stormwater concentration of Bifenthrin exceeds
    the CHRONIC aquatic invertebrate benchmark. So does the detection
    limit….

In both cases, since these are storm event samples, it is hard to know
whether these elevated concentrations are persistent or not. The
observed values are all below the realted ACUTE benchmarks (by about a
factor of 3).
