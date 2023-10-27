import prettytable
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
IAT_table = [(1, 0, 24), (2, 25, 64), (3, 65, 84), (4, 85, 100)]
AbleST_table = [(2, 0, 29), (3, 30, 57), (4, 58, 82), (5, 83, 100)]
BakerST_table = [(2, 0, 34), (3, 35, 59), (4, 60, 79), (5, 80, 100)]
# AbleST_table = [(3, 0, 34), (4, 35, 59), (5, 60, 79), (6, 80, 100)]
# BakerST_table = [(2, 0, 29), (3, 30, 57), (4, 58, 82), (5, 83, 100)]
table = []

def CalcIAT(RN):
    for row in IAT_table:
        if RN >= row[1] and RN <= row[2]:
            return row[0]


def CalcAbleST(RN):
    for row in AbleST_table:
        if RN >= row[1] and RN <= row[2]:
            return row[0]


def CalcBakerST(RN):
    for row in BakerST_table:
        if RN >= row[1] and RN <= row[2]:
            return row[0]


""" 
call id : i+1
RN_IAT : random.randint(1,100)
IAT : fn to convert RN_IAT based on IAT_table
clock: clock+IAT
RN-ST: random.randint(1,100)
AbleSTbegins: clock if AbleAvailable and not BakerAvailable else NULL
AbleST: fn to convert RN_ST based on AbleST_table if AbleAvailable and not BakerAvailable else NULL
AbleSTends: AbleSTbegins+AbleST if AbleAvailable and not BakerAvailable else NULL
bakerSTbegins: clock if bakerAvailable else NULL
bakerST: fn to convert RN_ST based on bakerST_table if bakerAvailable else NULL
bakerSTends: bakerSTbegins+bakerST if bakerAvailable else NULL
QueuingTime: if (BakerAvailable == false and AbleAlailable == false) then min(AbleSTends,bakerSTends)-clock else NULL
TimeInSystem: QueuingTime + AbleTrun ? AbleST : BakerST
AbleIdleTime: if AbleTurn then AbleSTends[i-1]-AbleSTbegins[i] else NULL
BakerIdleTime: if BakerTurn then BakerSTends[i-1]-BakerSTbegins[i] else NULL
"""
# generate a list of random numbers
RN_IAT = [random.randint(0, 100) for i in range(100)]
RN_ST = [random.randint(0, 100) for i in range(100)]
# RN_IAT = [0, 26, 98, 90, 26,42, 74, 80, 68, 22, 48, 34, 45, 24, 34, 63, 38, 80, 42, 56, 89, 18, 51, 71, 16, 92]
# RN_ST = [95, 21, 51, 92, 89, 38, 13, 61, 50, 49, 39, 53, 88, 1, 81, 53, 81, 64, 1, 67, 1, 47, 75, 57, 87, 47]

BakerAvailable = True
AbleAvailable = True
Baker_turn = True
Able_turn = False
clock = 0
BakerSTbegins = 0
AbleSTbegins = 0
BakerSTEnds = 0
AbleSTEnds = 0
AbleIdleTime = 0
BakerIdleTime = 0
for i, (RN_IAT, RN_ST) in enumerate(zip(RN_IAT, RN_ST)):
    QueuingTime = 0
    AbleST = 0
    BakerST = 0
    id = i+1  # call id should be deleted later
    if i != 0:
        IAT =  CalcIAT(RN_IAT)
    else: IAT = 0
    clock = clock + IAT
    if (clock < BakerSTEnds and clock < AbleSTEnds):
        if (BakerSTEnds <= AbleSTEnds):
            Baker_turn = True
            Able_turn = False
            BakerSTbegins = BakerSTEnds
            QueuingTime = BakerSTEnds - clock
            BakerST = CalcBakerST(RN_ST)
            BakerSTEnds = BakerSTbegins + BakerST
            BakerIdleTime = 0

        else:
            Baker_turn = False
            Able_turn = True
            AbleSTbegins = AbleSTEnds
            QueuingTime = AbleSTEnds - clock
            AbleST = CalcAbleST(RN_ST)
            AbleSTEnds = AbleSTbegins + AbleST
            AbleIdleTime = 0
    elif (clock < BakerSTEnds and clock >= AbleSTEnds):
        Able_turn = True
        Baker_turn = False
        AbleSTbegins = clock
        AbleIdleTime = clock - AbleSTEnds if AbleSTEnds else 0
        AbleST = CalcAbleST(RN_ST)
        AbleSTEnds = AbleSTbegins + AbleST
        QueuingTime = 0
    else:
        Baker_turn = True
        Able_turn = False
        BakerSTbegins = clock
        BakerIdleTime = clock - BakerSTEnds if BakerSTEnds else 0
        BakerST = CalcBakerST(RN_ST)
        BakerSTEnds = BakerSTbegins + BakerST
        QueuingTime = 0
    TimeInSystem = QueuingTime + AbleST if Able_turn else BakerST
    call = {
        "call ID": id,
        "RN_IAT": RN_IAT,
        "IAT": IAT,
        "clock": clock,
        "RN_ST": RN_ST,
        "AbleSTbegins": AbleSTbegins if Able_turn else "",
        "AbleST": AbleST if Able_turn else "",
        "AbleSTEnds": AbleSTEnds if Able_turn else "",
        "BakerSTbegins": BakerSTbegins if Baker_turn else "",
        "BakerST": BakerST if Baker_turn else "",
        "BakerSTEnds": BakerSTEnds if Baker_turn else "",
        "QueuingTime": QueuingTime,
        "TimeInSystem": TimeInSystem,
        "AbleIdleTime": AbleIdleTime if Able_turn else "",
        "BakerIdleTime": BakerIdleTime if Baker_turn else ""
    }
    table.append(call)

# export to xlsx
df = pd.DataFrame(table)
df.to_excel("twoServers.xlsx", index=False)
# print the table
prtytble = prettytable.PrettyTable()
prtytble.field_names = list(table[0].keys())
for row in table:
    prtytble.add_row(list(row.values()))
print(prtytble)

# percentage backer was busy

ptc_baker_busy = sum([row["BakerST"] for row in table if row["BakerST"] != ""]) / table[-1]["clock"]

print("percentage backer was busy: {:.2%}".format(ptc_baker_busy))

# percentage able was busy  
ptc_able_busy = sum([row["AbleST"] for row in table if row["AbleST"] != ""]) / table[-1]["clock"]
print("\n\npercentage able was busy: {:.2%}".format(ptc_able_busy))

# average waiting time
avg_waiting_time = sum([row["QueuingTime"] for row in table]) / sum([row["QueuingTime"] != 0 for row in table])
print("\n\naverage waiting time: {:.2f} minutes".format(avg_waiting_time))
#histogram to show callers delay
# waiting_time = [row["QueuingTime"] for row in table if row["QueuingTime"] != 0]
# max_waiting_time = max(waiting_time)
# plt.hist(waiting_time, edgecolor = 'black')
# plt.xticks(range(1,max_waiting_time+1))
# plt.show()
# count plot to show callers delay
waiting_time_df = pd.DataFrame([row["QueuingTime"] for row in table if row["QueuingTime"] != 0])
# type_count = waiting_time_df[0].value_counts()
# order = type_count.index
sns.countplot(x=0, data=waiting_time_df)
# # for i in range(1, type_count.shape[0]+1):
# #     cnt = type_count[i]
# #     pct_text = '{:0.1f}%'.format(100*cnt/waiting_time_df.shape[0])
# #     plt.text(cnt+1, i-1, pct_text, va='center')
plt.show()