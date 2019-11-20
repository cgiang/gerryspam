import geopandas as gpd
import pandas as pd
import numpy as np
import re

shp_path = '/Users/hopecj/projects/AR/Shapefiles/AR Precincts 10_11_2019/ELECTION_PRECINCTS.shp'
elec_path = '/Users/hopecj/projects/AR/elections/AR_G18.csv'

elec_df = pd.read_csv(elec_path)

shp_df = gpd.read_file(shp_path)
shp_df = shp_df[['county_nam', 'precinct','geometry']]
shp_df.groupby(['county_nam']).ngroups #sigh.....75 counties

# function to clean
def ar_prec_transform(dat, county, custom_transformation = None, upper = True, chop_five_digs = True):
       dat_out = dat.loc[dat['county_nam'] == county]
       dat_out['prec_new'] = dat_out['precinct']
       if chop_five_digs:
              dat_out['prec_new'] = dat_out['prec_new'].str.slice(start = 5)
       dat_out = dat_out.replace(
              custom_transformation
       )
       if upper:
              dat_out['prec_new'] = dat_out['prec_new'].str.upper()
       return dat_out

# arkansas cnty
c1 = ar_prec_transform(shp_df, 'Arkansas', 
       {'DEWITT 1': 'DEWITT WARD 1', 
       'DEWITT 2': 'DEWITT WARD 2',
       'DEWITT 3': 'DEWITT WARD 3',
       'STUTTGART 1': 'STUTTGART WARD 1',
       'STUTTGART 2': 'STUTTGART WARD 2', 
       'STUTTGART 3': 'STUTTGART WARD 3'}
       )

# ashley cnty
c2 = ar_prec_transform(shp_df, 'Ashley',
       {'CROSSETT WARD 1': 'CW 1',
       'CROSSETT WARD 2': 'CW 2',
       'CROSSETT WARD 3': 'CW 3',
       'FOUNTAIN HILL CITY': 'FH CITY',
       'FOUNTAIN HILL CITY': 'FH RURAL',
       'HAMBURG WARD 1': 'HW1',
       'HAMBURG WARD 2': 'HW2',
       'HAMBURG WARD 3': 'HW3',
       'MT. ZION': 'MT ZION',
       'NORTH CROSSETT EAST': 'NCE',
       'NORTH CROSSETT WEST': 'NCW',
       'SNYDER / TRAFALGAR': 'SNY/TRA',
       'VO - TECH': 'VOTECH',
       'WEST CROSSETT RURAL': 'WCR'}
       )

# baxter cnty
c3 = ar_prec_transform(shp_df, 'Baxter', upper=False, chop_five_digs=False)

# benton cnty
c4 = ar_prec_transform(shp_df, 'Benton', {
       'Precinct 01': 'Precinct 1',
       'Precinct 02': 'Precinct 2',
       'Precinct 03': 'Precinct 3',
       'Precinct 04': 'Precinct 4',
       'Precinct 05': 'Precinct 5',
       'Precinct 06': 'Precinct 6',
       'Precinct 07': 'Precinct 7',
       'Precinct 08': 'Precinct 8',
       'Precinct 09': 'Precinct 9'}, upper=False, chop_five_digs=False, 
)

# boone cnty
# COME BACK after contacting county
# big mismatch in number of precincts (more in election results)
c5 = ar_prec_transform(shp_df, 'Boone', )

# bradley cnty
c6 = ar_prec_transform(shp_df, 'Bradley', {
       'Warren Ward 1': 'Ward 1',
       'Warren Ward 2': 'Ward 2',
       'Warren Ward 3': 'Ward 3'},  
       upper=False
)

# calhoun cnty 
# COME BACK & figure out the deal with watson addition in election results
c7 = ar_prec_transform(shp_df, 'Calhoun', upper=False, chop_five_digs=False)

# carroll cnty
c8 = ar_prec_transform(shp_df, 'Carroll', {
       'Berryville Ward 1': 'BV Ward 1',
       'Berryville Ward 2': 'BV Ward 2',
       'Eureka Springs Ward 1': 'ES Ward 1',
       'Eureka Springs Ward 2': 'ES Ward 2',
       'Eureka Springs Ward 3': 'ES Ward 3',
       'Green Forest Ward 1': 'GF Ward 1',
       'Green Forest Ward 2': 'GF Ward 2',
       'North East Hickory': 'NE Hickory',
       'Northwest Hickory': 'NW Hickory',
       'Long Creek': 'Lng Crk',
       'SW & SE HICKORY': 'SW/SE HICKORY'}, 
       chop_five_digs=False)

# chicot cnty
# might need to chop another digit
c9 = ar_prec_transform(shp_df, 'Chicot', {
       'Carlton': 'Carlton 1'},
       upper=False)

# clark cnty
c10 = ar_prec_transform(shp_df, 'Clark', {
       'Central 1': 'Central',
       'Curtis 1': 'Curtis',
       'East County 1': 'East County',
       'Gum Springs Outside 1': 'Gum Springs Outside',
       'Gum Springs 1': 'Gum Springs Inside',
       'Gurdon Gen 1': 'Gurdon General',
       'North East County': 'Northeast County',
       'Okolona City 1': 'Okolona City',
       'South County 1': 'South County',
       'West County 1': 'West County',
       'Whelen Springs 1': 'Whelen Springs'},
       chop_five_digs=False)

# clay county
c11 = ar_prec_transform(shp_df, 'Clay', {
       'Bennett & Lemmons': 'Bennett and Lemmons',
       'E Oak Bluff & Blue Cane': 'East Oak Bluff & Blue Cane',
       'Liddell & chalk Bluff': 'Liddell & Chalk Bluff',
       'Cleveland & N Kilgore': 'N Kilgore & Cleveland',
       'North St Francis': 'North St. Francis',
       'Gleghorn & S Kilgore': 'S Kilgore & Gleghorn',
       'South St Francis': 'South St. Francis'},
       upper=False)

# cleburne county
# also transformed the elections data to remove last three numbers
c12 = ar_prec_transform(shp_df, 'Cleburne')

# cleveland county
c13 = ar_prec_transform(shp_df, 'Cleveland', upper=False)

# columbia county
c14 = ar_prec_transform(shp_df, 'Columbia', {
       'Taylor City': 'Taylor',
       'Waldo City': 'Waldo'},
       chop_five_digs=False)

# conway county
c15 = ar_prec_transform(shp_df, 'Conway', {
       'St Vincent': 'St. Vincent',
       'Lick Mountain': 'Lick Mtn.'})

# craighead
# took the "precinct" out of elections data
c16 = ar_prec_transform(shp_df, 'Craighead',
       chop_five_digs=False,
       upper=False)

# crawford 
c17 = ar_prec_transform(shp_df, 'Crawford', {
       'Alma 01': 'Alma 1', 
       'Alma 02': 'Alma 2', 
       'Alma 03': 'Alma 3', 
       'Alma 04': 'Alma 4', 
       'Cove City': 'Cove City CSD',
       'Lee Creek': 'Lee Creek CSD',
       'Mulberry 01': 'Mulberry 1',
       'Mulberry 02': 'Mulberry 2',
       'Mulberry 03': 'Mulberry 3'},
       chop_five_digs=False,
       upper=False)

# crittenden
# need to revisit. none of these names match up
c18 = ar_prec_transform(shp_df, 'Crittenden')

# cross
c19 = ar_prec_transform(shp_df, 'Cross', {
       'Bay Village / Birdeye': 'Bay Village, Birdeye',
       'Cherry Valley': 'Cherry Valley City',
       'Tyronza / Twist': 'Tyronza, Twist',
       'Wynne Ward 1': 'WYNNE WARD 1',
       'Wynne Ward 2': 'WYNNE WARD 2',
       'Wynne Ward 3': 'WYNNE WARD 3',
       'Wynne Ward 4': 'WYNNE WARD 4',
       'Wynne Ward 5': 'WYNNE WARD 5'},
       chop_five_digs=False,
       upper=False)

# dallas
c20 = ar_prec_transform(shp_df, 'Dallas', upper=False)






elec_df = pd.read_csv(elec_path)
elec_df['NAME'] = elec_df['NAME'].str.strip()
elec_df = elec_df[['NAME', 'precinct', 'G18DGOV', 'G18RGOV', 'G18LGOV',
       'G18DHOR', 'G18RHOR', 'G18DStSEN', 'G18RStSEN', 'G18DStHou',
       'G18RStHou', 'G18LStHou', 'G16DPRS', 'G16RPRS', 'G16LPRS', 'G16GPRS',
       'G16CPRS', 'G16NPPRS', 'G16NAPRS', 'G16DSEN', 'G16RSEN', 'G16LSEN',
       'G16NASEN', 'G16NPSEN', 'G16DHOR', 'G16RHOR', 'G16LHOR', 'G16NAHOR',
       'G16NPHOR', 'G16DStHou', 'G16RStHou', 'G16CStHou', 'G16IStHou',
       'G16NAStHou', 'G16NPStHou', 'G14RGOV', 'G14CGOV', 'G14LGOV', 'G14NAGOV',
       'G14NPGOV', 'G14DSEN', 'G14RSEN', 'G14LSEN', 'G14NASEN', 'G14NPSEN',
       'G14DHOR', 'G14RHOR', 'G14LHOR', 'G14NPHOR', 'G14DStSEN', 'G14RStSEN',
       'G14NAStSEN', 'G14NPStSEN', 'G14DStHou', 'G14RStHou', 'G14CStHou',
       'G14LStHou', 'G14NAStHou', 'G14NPStHou']]

merged = pd.merge(shp_df, elec_df, on='NAME', how = 'outer')


merged.to_file('/Volumes/GoogleDrive/Shared drives/princeton_gerrymandering_project/OpenPrecincts/States for site/Alaska/Final/AK_Prec_G14_16_18.shp')
#merged.to_csv('/Volumes/GoogleDrive/Shared drives/princeton_gerrymandering_project/OpenPrecincts/States for site/Alaska/Final/AK_Prec_G14_16_18_test.csv')

for i in shp_df:
   geom = shp_df['geometry']
   if geom.geom_type=='MultiPolygon':
      print(geom)
