def print_metrics(acc, err, prec_macro, prec_ind, rev_macro, rev_ind, spec_macro, spec_ind):
    print("Acurácia: ", acc)
    print("Taxa de erro: ", err, '\n')

    print("Precisão(macro): ", prec_ind)
    for i in range(len(prec_ind)):
        print("  Precisão(" + ohe.categories_[0][i] + "): ", prec_ind[i])

    print('\n', "Recall(macro): ", rev_macro)
    for i in range(len(rev_ind)):
        print("  Recall(" + ohe.categories_[0][i] + "): ", rev_ind[i])

    print('\n', "Especificidade(macro): ", spec_macro)
    for i in range(len(spec_ind)):
        print("  Especificidade(" + ohe.categories_[0][i] + "): ", spec_ind[i])

def list_mean(lst):
    mean = 0
    for i in range(len(lst)):
        mean += lst[i]
    
    mean /= len(lst)
    
    return mean
    
def accuracy_score(confusion_matrix):
    total = 0
    true_values = 0
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            total += confusion_matrix[i][j]
            if i == j:
                true_values += confusion_matrix[i][j]

    accuracy = true_values / total
    
    return accuracy * 100

def error_rate(confusion_matrix):
    err = 1 - accuracy_score(confusion_matrix)
    
    return err * 100

def individual_precision_list(confusion_matrix):
    cols = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            cols[j] += confusion_matrix[i][j]
    
    individual_precision = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        if not cols[i] == 0:
            individual_precision[i] = confusion_matrix[i][i] / cols[i]
        
    return individual_precision * 100

def macro_precision(confusion_matrix):
    precision = list_mean(individual_precision_list(confusion_matrix))
    
    return precision * 100

def individual_recall_list(confusion_matrix):
    lines = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            lines[i] += confusion_matrix[i][j]

    individual_recall = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        if not lines[i] == 0:
            individual_recall[i] = confusion_matrix[i][i] / lines[i]    
    
    return individual_recall * 100

def macro_recall(confusion_matrix):
    recall = list_mean(individual_recall_list(confusion_matrix))
    
    return recall * 100
    
def individual_specificity_list(confusion_matrix):
    total = 0
    cols = [0] * len(confusion_matrix)
    vn = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            total += confusion_matrix[i][j]
            cols[j] += confusion_matrix[i][j]
            vn[i] -= confusion_matrix[i][j]
            vn[j] -= confusion_matrix[i][j]
            if i == j:
                vn[i] += confusion_matrix[i][j]
                
    for i in range(len(vn)):
        vn[i] += total

    individual_specificity = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        individual_specificity[i] = vn[i] / (cols[i] - confusion_matrix[i][i] + vn[i])
    
    return individual_specificity * 100

def macro_specificity(confusion_matrix):
    specificity = list_mean(individual_specificity_list(confusion_matrix))
    
    return specificity * 100

def f1_score(confusion_matrix):
    prec = macro_precision(confusion_matrix)
    recall = macro_recall(confusion_matrix)
    score = (2 * prec * recall) / (prec + recall)

    return score 