# https://github.com/gerrymandr/georgia/blob/master/competitiveness.ipynb
import numpy as np
import pickle
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from gerrychain import Graph, Partition, Election
from gerrychain.updaters import Tally, cut_edges
import pandas as pd

# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

# load results from gerrychain 
sen_05 = np.load("/Users/hopecj/projects/gerryspam/MO/res/MO_state_senate_100000_0.05.p")
sen_03 = np.load("/Users/hopecj/projects/gerryspam/MO/res/MO_state_senate_100000_0.03.p")
sen_01 = np.load("/Users/hopecj/projects/gerryspam/MO/res/MO_state_senate_100000_0.01.p")
sen_05.keys() # shows "columns" available
print(sen_05["mean_median_ussen16"]) # results from chain

# get enacted map open
graph = Graph.from_file("/Users/hopecj/projects/gerryspam/MO/dat/final_prec/prec_labeled.shp")
elections = [Election("USSEN16", {"Dem": "G16USSDKAN", "Rep": "G16USSRBLU"}),
             Election("PRES16", {"Dem": "G16PREDCLI", "Rep": "G16PRERTRU"})]

mo_updaters = {"population" : Tally("POP10", alias="population"),
               "cut_edges": cut_edges,
            }
election_updaters = {election.name: election for election in elections}
mo_updaters.update(election_updaters)

sen_part = Partition(graph, assignment="SLDUST", updaters=mo_updaters)
cong_part = Partition(graph, assignment="SLDLST", updaters=mo_updaters)

# D voteshare - ensemble vs enacted
#PRES16
plt.figure(figsize=(12,6))
plt.title("PRES16 - 1% population deviation")
plt.xlabel("Indexed District")
plt.ylabel("Democratic vote % (PRES16)")
plt.boxplot(sen_01["results_pres16"], whis=(1,99), showfliers=False)
plt.scatter(y=sorted(sen_part["PRES16"].percents("Dem")), x=range(1,35), 
            marker="o", label="Enacted Plan", c="r")
plt.axhspan(0.45, 0.55, color="limegreen", alpha=0.15, zorder=0)
plt.axhline(y=0.5, color="limegreen", zorder=0)
plt.legend()
plt.savefig("/Users/hopecj/projects/gerryspam/MO/plots/stsen_dem_voteshare_pres16_01.png", bbox_inches="tight", dpi=200)
plt.show()

#USSENATE16
plt.figure(figsize=(12,6))
plt.title("SEN16 - 5% population deviation")
plt.xlabel("Indexed District")
plt.ylabel("Democratic vote % (SEN16)")
plt.boxplot(sen_05["results_ussen16"], whis=(1,99), showfliers=False)
plt.scatter(y=sorted(sen_part["USSEN16"].percents("Dem")), x=range(1,35), 
            marker="o", label="Enacted Plan", c="r")
plt.axhspan(0.45, 0.55, color="limegreen", alpha=0.15, zorder=0)
plt.axhline(y=0.5, color="limegreen", zorder=0)
plt.legend()
plt.savefig("/Users/hopecj/projects/gerryspam/MO/plots/stsen_dem_voteshare_ussen16_05.png", bbox_inches="tight", dpi=200)
plt.show()

# D seats - ensemble vs enacted
# PRES16
plt.title("Seat Share - Enacted versus Ensemble (PRES16 1% pop. deviation)")
plt.xlabel("Democratic Seats in State Senate")
plt.hist(sen_01["seats_pres16"], histtype="stepfilled", bins=np.arange(0,17)-0.5, alpha=0.5)
plt.axvline(x=np.mean(sen_01["seats_pres16"]), label="Ensemble Mean")
plt.axvline(x=sen_part["PRES16"].seats("Dem"), label="Enacted Plan", c="k")
plt.legend()
plt.savefig("/Users/hopecj/projects/gerryspam/MO/plots/stsen_dem_seats_pres16_01.png", bbox_inches="tight", dpi=200)
plt.show()

# USSEN16
plt.title("Seat Share - Enacted versus Ensemble (USSEN16 01% pop. deviation)")
plt.xlabel("Democratic Seats in State Senate")
plt.hist(sen_01["seats_ussen16"], histtype="stepfilled", bins=np.arange(0,17)-0.5, alpha=0.5)
plt.axvline(x=np.mean(sen_01["seats_ussen16"]), label="Ensemble Mean")
plt.axvline(x=sen_part["USSEN16"].seats("Dem"), label="Enacted Plan", c="k")
plt.legend()
plt.savefig("/Users/hopecj/projects/gerryspam/MO/plots/stsen_dem_seats_sen16_01.png", bbox_inches="tight", dpi=200)
plt.show()

# Partisanship
def extend_data_frame(df, data, key_prefix, col, districts, epsilon, 
                      elections=["PRES16", "SEN16"], iters=100000):
    for elect in elections:
        key = key_prefix.format(elect.lower())
        df = pd.concat([df, pd.DataFrame(np.array([data[key], [elect]*iters, [districts]*iters, [epsilon]*iters]).T,
                                         columns=[col, "Election", "Districts", "Epsilon"])], ignore_index=True)
    return df
elections = ["PRES16", "USSEN16"]

# efficiency gap
eg = pd.DataFrame()
eg = extend_data_frame(eg, sen_05, "efficiency_gap_{}", "EG", 34, 0.05, elections=elections)
eg = extend_data_frame(eg, sen_03, "efficiency_gap_{}", "EG", 34, 0.03, elections=elections)
eg = extend_data_frame(eg, sen_01, "efficiency_gap_{}", "EG", 34, 0.01, elections=elections)

eg["EG"] = eg["EG"].apply(float)
eg["Districts"] = eg["Districts"].apply(int)
eg["Epsilon"] = eg["Epsilon"].apply(float)
# check that we got the right number of rows
eg.groupby(['Election', 'Epsilon'])['EG'].count()

# make a plot
sns.set(style="whitegrid", palette="Set3")
es = ["PRES16", "USSEN16"]
plt.figure(figsize=(12,6))
plt.title("Efficiency Gap Scores")
sns.violinplot(x="Epsilon", y="EG", hue="Election", hue_order=es, 
               data=eg, inner="quartile")
plt.axhspan(-0.08, 0.08, color="limegreen", alpha=0.15, zorder=0)

for i in [-1,1]:
    plt.plot([0 + i*0.2],sen_part[es[int(i == 1)]].efficiency_gap(), marker="o", color="red")
    plt.plot([1 + i*0.2],sen_part[es[int(i == 1)]].efficiency_gap(), marker="o", color="red")
#     plt.plot([3 + i*0.270],house[es[i+1]].efficiency_gap(), marker="o", color="red")
plt.savefig("/Users/hopecj/projects/gerryspam/MO/plots/stsen_EG.png", bbox_inches="tight", dpi=200)
plt.show()

#mean-median difference
mm = pd.DataFrame()
mm = extend_data_frame(mm, sen_05, "mean_median_{}", "MM", 34, 0.05, elections=elections)
mm = extend_data_frame(mm, sen_03, "mean_median_{}", "MM", 34, 0.03, elections=elections)
mm = extend_data_frame(mm, sen_01, "mean_median_{}", "MM", 34, 0.01, elections=elections)

mm["MM"] = mm["MM"].apply(float)
mm["Districts"] = mm["Districts"].apply(int)

mm["MM"] = mm["MM"].apply(float)
mm["Districts"] = mm["Districts"].apply(int)
mm["Epsilon"] = mm["Epsilon"].apply(float)
# check that we got the right number of rows
mm.groupby(['Election', 'Epsilon'])["MM"].count()

# make a plot
sns.set(style="whitegrid", palette="Set3")
es = ["PRES16", "USSEN16"]
plt.figure(figsize=(12,6))
plt.title("Mean Median Scores")
sns.violinplot(x="Epsilon", y="MM", hue="Election", hue_order=es, 
               data=mm, inner="quartile")

for i in [-1,1]:
    plt.plot([0 + i*0.2],sen_part[es[int(i == 1)]].mean_median(), marker="o", color="red")
    plt.plot([1 + i*0.2],sen_part[es[int(i == 1)]].mean_median(), marker="o", color="red")

plt.savefig("/Users/hopecj/projects/gerryspam/MO/plots/stsen_MM.png", bbox_inches="tight", dpi=200)
plt.show()

# create a data frame with columns for vote by district, eg, and D-seats
def extend_data_frame(df, data, key_prefix_metric, key_prefix_res, key_prefix_seats,
                      col, districts, epsilon, 
                      elections=["PRES16", "SEN16"], iters=100000):
    df_res = pd.DataFrame([])
    df_seats = pd.DataFrame([])
    for elect in elections:
        # eg DF
        key_metric = key_prefix_metric.format(elect.lower())
        df = pd.concat([df, pd.DataFrame(np.array([data[key_metric], [elect]*iters, [districts]*iters, [epsilon]*iters]).T,
                                         columns=["eg", "election", "total_districts", "epsilon"])], ignore_index=True)
        # results DF
        key_res = key_prefix_res.format(elect.lower())
        res_intermediate = pd.DataFrame(data[key_res])
        df_res = df_res.append(res_intermediate, ignore_index=True)
        # seats DF
        key_seats = key_prefix_seats.format(elect.lower())
        seats_intermediate = pd.DataFrame(data[key_seats])
        df_seats = df_seats.append(seats_intermediate, ignore_index=True)
    df_res.rename(columns=lambda x: x+1, inplace=True) 
    df_seats = df_seats.rename(columns={0:'D_seats'})
    return df, df_res, df_seats
elections = ["PRES16", "USSEN16"]

eg = pd.DataFrame()
eg_05 = extend_data_frame(eg, sen_05, "efficiency_gap_{}", "results_{}", "seats_{}", "EG", 34, 0.05, elections=elections)
eg_03 = extend_data_frame(eg, sen_03, "efficiency_gap_{}", "results_{}", "seats_{}", "EG", 34, 0.03, elections=elections)
eg_01 = extend_data_frame(eg, sen_01, "efficiency_gap_{}", "results_{}", "seats_{}", "EG", 34, 0.01, elections=elections)

# merge together the tuple returned from the function
# nb: this is all 5% population deviation!
out = eg_05[0].join(eg_05[1])
out = out.join(eg_05[2])

# sample rows for viz
out_sample = out.sample(n=8000, replace=False, random_state=1)
out_sample['hash'] = out_sample.index

out_sample.to_csv("/Users/hopecj/projects/gerryspam/MO/res/stsen_05_data_sampled.csv")