from saram import Population, Saram
import matplotlib.pyplot as plt
import pandas as pd

time = 0
n = 300
t = 300
p = Population(n)
populations = []

for i in range(t*365):
    p.day()
    populations.append(p.n)
    time += 1
    if time % 365 == 0:
        print("year", int(time/365), "n =", p.n)

print("v/peopleEver:")
print(p.virgins, p.peopleEver, sep="/")
print("suicides:", p.suicides)

ages = pd.Series(p.partnerAges)
attr = pd.Series(p.partnerAttr)
breakUpLen = pd.Series(p.breakupLengths)
breakups = pd.Series(p.breakups)
populations = pd.Series(populations)
children = pd.Series(p.children)
generations = pd.Series(p.generations)
prAges = pd.Series(p.pregnancyAges)
pAgeDiff = pd.Series(p.partnerAgeDiff)
lifeLengths = pd.Series(p.lifeLengths)

fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10) = plt.subplots(10)
ax1.hist(ages, bins=40)
ax2.hist(attr, bins=30)
ax3.hist(breakUpLen, bins=20)
ax4.bar(breakups.value_counts().keys(), breakups.value_counts())
ax5.plot(populations)
ax6.bar(children.value_counts().keys(), children.value_counts())
ax7.bar(generations.value_counts().keys(), generations.value_counts())
ax8.hist(prAges, bins=20)
ax9.hist(pAgeDiff, bins=10)
ax10.hist(lifeLengths)
plt.show()
