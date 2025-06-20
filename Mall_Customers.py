from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

file_path = "Data/Mall_Customers.csv"
if os.path.isfile(file_path):
    print(f"File found: {file_path}")
    df1 = pd.read_csv(file_path)
else:
    print(f"File not found: {file_path}")
    df1 = None

def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]]
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) // nGraphPerRow
    plt.figure(num=None, figsize=(6 * nGraphPerRow, 8 * nGraphRow), dpi=80, facecolor='w', edgecolor='k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if not np.issubdtype(type(columnDf.iloc[0]), np.number):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation=90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad=1.0, w_pad=1.0, h_pad=1.0)
    plt.show()

def plotCorrelationMatrix(df, graphWidth):
    df = df.dropna(axis=1)
    df = df[[col for col in df if df[col].nunique() > 1]]
    df = pd.get_dummies(df, columns=['Gender'], drop_first=True)  # Corrected here
    print(f'Filtered DataFrame for correlation matrix:\n{df.head()}')
    print(f'Number of columns for correlation: {df.shape[1]}')
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum=1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title('Correlation Matrix', fontsize=15)
    plt.show()

def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include=[np.number])
    print(f'Numeric DataFrame for scatter matrix:\n{df.head()}')
    df = df.dropna(axis=1)
    df = df[[col for col in df if df[col].nunique() > 1]]
    print(f'Filtered DataFrame for scatter matrix:\n{df.head()}')
    print(f'Number of columns for scatter matrix: {df.shape[1]}')
    columnNames = list(df)
    if len(columnNames) > 10:
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*np.triu_indices_from(ax, k=1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()

if df1 is not None:
    nRow, nCol = df1.shape
    print(f'There are {nRow} rows and {nCol} columns')
    print(df1.dtypes)
    print(df1.head(5))

    plotPerColumnDistribution(df1, 10, 5)
    plotCorrelationMatrix(df1, 8)
    plotScatterMatrix(df1, 12, 10)
