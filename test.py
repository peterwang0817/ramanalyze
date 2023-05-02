import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_path = ["data/20230424(mos2)/L20bulkangle30expos15.asc", "data/20230424(mos2)/L20bulkangle34expos15.asc"]
bkgd_path = "data/20230424(mos2)/L20_background_angle10expos15.asc"

df = []
#df['background'] = np.loadtxt
for file in file_path:
    df.append(np.loadtxt(file, max_rows=2000))
#df = pd.read_table(bkgd_path, header=None, nrows=2000, index_col=0)
for file in df:
    plt.plot(file[:,0], file[:,1])
plt.show()