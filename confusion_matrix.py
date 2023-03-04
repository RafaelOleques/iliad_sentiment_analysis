import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # para visualização de informações
import seaborn as sns

def build_matrix(y_true, y_pred):
    # Build matrix
    matrix = [[]] * len(y_true[0])
    for i in range(len(y_true[0])):
        matrix[i] = [0] * len(y_true[0])

    # Calculate matirx
    for i in range(len(y_true)):
        tr = y_true[i] 
        pred = y_pred[i]
        j = np.where(tr == 1)[0][0]
        k = np.where(pred == 1)[0]
        if len(k) == 0:
            if (j + 1) < len(y_true[0]):
                k = j + 1
            else:
                k = j - 1
        else:
            k = k[0]
        matrix[j][k] += 1

    return matrix

def plot_confusion_matrix(confusion_matrix, categories):
    df_cm = pd.DataFrame(confusion_matrix, index = [i for i in categories], columns = [i for i in categories])
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True)
