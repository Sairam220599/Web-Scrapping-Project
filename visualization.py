import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv("college_file.csv")

print(df)

fig1 ,ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

Region = df.groupby('Region').count()['College Name']

ax1.pie(Region, labels=Region.index , autopct='%1.1f%%')
ax1.set_title('No. of Colleges Region wise.')

Auto_By_Region = df.groupby(['Region','Autonomous Status']).count()['College Name']

auto = []
non_auto = []
print(type(Auto_By_Region))
for i in range(len(Auto_By_Region)):
    if(i%2==0):
        auto.append(Auto_By_Region[i])
    else:
        non_auto.append(Auto_By_Region[i])

print(auto, non_auto)

x = np.arange(len(Region.index))
width = 0.35

rect1 = ax2.bar(x - width/2, auto, width, label='Auto')
rect2 = ax2.bar(x + width/2, non_auto, width, label='Non Autonomous')
ax2.legend()
ax2.set_xticks(x)
ax2.set_xticklabels(Region.index)
ax2.set_ylabel('No. of Colleges')
ax2.set_title('No. of Autonmous and non-Autonomous per Region')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax2.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rect1)
autolabel(rect2)

fig2.tight_layout()
plt.show()








