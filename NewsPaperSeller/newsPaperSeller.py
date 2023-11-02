import random
import pandas as pd
news_type = [("good", 1, 35), ("fair", 36, 80), ("poor", 81, 100)]
demand = {
"good" : [(40, 1, 3), (50, 4, 8), (60, 9, 23), (70, 24, 43), (80, 44, 78), (90, 79, 93), (100, 94, 100)],
"fair" : [(40, 1, 10), (50, 11, 28), (60, 29, 68), (70, 69, 88), (80, 89, 96), (90, 97, 100)],
"poor" : [(40, 1, 44), (50, 45, 66), (60, 67, 82), (70, 83, 94), (80, 95, 100)]
}
# number of days and items
N = 10
items = 70
# prices in cent
paper_cost = .33
selling_price = .50
scarp_price = .05
#cost of papers
NP_cost = items * paper_cost
# generate a list of random numbers
# RN_NT = [random.randint(1, 101) for i in range(N)]
# RN_D = [random.randint(1, 101) for i in range(N)]
RN_NT = [86, 32, 73, 24, 76, 38, 45, 18, 44, 12]
RN_D = [4, 39, 66, 89, 97, 24, 9, 55, 15, 17]
# calculate the news type and demand
def CalcNT(RN):
    for row in news_type:
        if RN >= row[1] and RN <= row[2]:
            return row[0]
def CalcD(RN, NT):
    for row in demand[NT]:
        if RN >= row[1] and RN <= row[2]:
            return row[0]

df = pd.DataFrame(columns=['Day', 'RN for NT','News Type', 'RN for demand','Demand', 'Sales Revenue', 'Cost of NPs', 'Lost Profit', 'Scrap Revenue','Daily Profit'])    
for i in range(N):
    NT = CalcNT(RN_NT[i])
    D = CalcD(RN_D[i], NT)
    # calculate the revenue
    sales_revenue = D * selling_price
    # lost profit and scarp revenue
    lost_profit = 0.0
    scarp_revenue = 0.0
    if D < items:
        scarp_revenue += (items - D) * scarp_price
    elif D > items:
        lost_profit += (D - items) * selling_price    
    # calculate the profit
    profit = sales_revenue - NP_cost + scarp_revenue - lost_profit
    df = pd.concat([df, pd.DataFrame([[i+1, RN_NT[i], NT, RN_D[i], D, sales_revenue, NP_cost, lost_profit, scarp_revenue, profit]], columns=['Day', 'RN for NT','News Type', 'RN for demand','Demand', 'Sales Revenue', 'Cost of NPs', 'Lost Profit', 'Scrap Revenue','Daily Profit'])])

print(df)
df.to_excel('newsPaperSeller.xlsx', index=False)        
