import pandas as pd
import matplotlib.pyplot as plt # para visualização de informações
import seaborn as sns

def confusion_matrix(y_true, y_pred, categories):
    # Build matrix
    categories = list(categories[0])
    matrix = [[]] * len(categories)
    for i in range(len(categories)):
        matrix[i] = [0] * len(categories)
    
    # Calculate matirx
    for i in range(len(y_true)):
        matrix[categories.index(y_true[i])][categories.index(y_pred[i])] += 1

    return matrix
    
def plot_confusion_matrix(confusion_matrix, categories):
    df_cm = pd.DataFrame(confusion_matrix, index = [i for i in categories], columns = [i for i in categories])
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True)

