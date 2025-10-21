import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df1 = pd.read_csv("../modern/sectors/grenville/connectivity_decimal.csv", header=0, index_col=['LOC_NAME_S'])
df2 = pd.read_csv("../winds_modern/sectors/grenville/connectivity_decimal.csv", header=0, index_col=['LOC_NAME_S'])
df3 = pd.read_csv("../wind_and_ties/sectors/grenville/connectivity_decimal.csv", header=0, index_col=['LOC_NAME_S'])

names = ['Tides','Wind','Wind & Tides']
#df5k = np.arange(16).reshape(4,4)
#df4k = np.arange(16).reshape(4,4)
#df6k = np.arange(16).reshape(4,4)


list_df = [df1, df2, df3]
matrix = list()
getdiagonals = list()
getoffdiagonals = list()

# Convert the DataFrame to a NumPy array #matrix5 = df5k.values
def makematrix(x):
     x = x.values
     return x

for df in list_df:
    matrix.append(makematrix(df))


# Extract the diagonal elements using NumPy #diagonal_elements5 = np.diag(matrix5)
def getdiagonal(d):
    diag = np.diag(d)
    return diag

for df in matrix:
    getdiagonals.append(getdiagonal(df))

diagonals = pd.DataFrame(dict(zip(names, getdiagonals)), columns = names)
diagonals.to_csv('particle_diagonals_grenville.csv')


#### Extract the off diagonal elements using Numpy
def getoffdiagonal(o):
    off_u = o[np.triu_indices_from(o, k=1)]
    off_l = o[np.tril_indices_from(o, k=-1)]
    off_diagonal = np.concatenate((off_u,off_l), axis =0)
    return off_diagonal

#u_5 = a[np.triu_indices_from(a, k=1)]
#l_5 = a[np.tril_indices_from(a, k=-1)]
#offdiagonal_5 = np.concatenate((u_5,l_5), axis =0)

for df in matrix:
    getoffdiagonals.append(getoffdiagonal(df))

#print(getoffdiagonals)

offdiagonals = pd.DataFrame(dict(zip(names, getoffdiagonals)), columns = names)
offdiagonals.to_csv('particle_offdiagonals_grenville.csv') # not sure if this is working right


# density plot
#colour palettes
#colour = sns.color_palette("crest") # seaborn ocean coloured palette
#reef_palette = ["#385a7c","#e06565", "#faa7a7","#60958e", "#a0d6cf"] # came from https://www.color-hex.com/color-palette/71855
#ocean_reef_palette = ["#160F29", "#2C808C","#5CC1BC", "#A56DEE", "#FF695C"]
#coral_palette = ["#ea7070", "#fdc4b6", "#e59572", "#2694ab", "#4dbedf"]
#ocean_palette = ["#3b3667","#3d558d", "#3184ab", "#37aabd", "#46eaee"] # came from https://www.color-hex.com/color-palette/99118
ocean_palette_2 = ["#625E85", "#217154","#5A9CBB", "#9B88DB","#46eaee","#ea7070", "#e59572"] # came from https://www.color-hex.com/color-palette/99118
#ocean_palette_3 = ["#172B94","#6137B7", "#785ECE","#4890C3","#3FD2D6","#ea7070", "#DD7547"]
#palette_3 = ["#DAD6CA", "#1BB0CE", "#4F8699", "#6A5E72", "#563444"]

sns.set_palette(ocean_palette_2, n_colors=100)
sns.set_style("darkgrid")
#sns.set_context("paper")
fig, ax = plt.subplots()
ax.set_xlim(0.0,0.5)
df = ax.set(xlabel = "Self Connectivity", ylabel = "Density", title = "Diagonal Elements")

for df in diagonals:
    sns.kdeplot(diagonals, label = 'Resolution')

plt.savefig("particle_densityplot_grenville.png")
plt.show()

#df = ax.set(xlabel = "Self Connectivity", ylabel = "Density", title = "Off Diagonal Elements")
#for df in offdiagonals:
#    sns.kdeplot(offdiagonals, label = 'Resolution')

#plt.savefig("offdiagonals_densityplot.png")
#plt.show()

################

#df = sns.kdeplot(np.array(diagonal_elements5), ax=ax, label = "5000 m", color = '#385a7c', style("white"))
#df = sns.kdeplot(np.array(diagonal_elements4), ax=ax, label = "4000 m", color = '#e06565')



