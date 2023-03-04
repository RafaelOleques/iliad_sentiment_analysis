def list_mean(lst):
    mean = 0
    for i in range(len(lst)):
        mean += lst[i]
    
    mean /= len(lst)
    
    return mean

def accuracy(confusion_matrix):
    total = 0
    true_values = 0
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            total += confusion_matrix[i][j]
            if i == j:
                true_values += confusion_matrix[i][j]

    accuracy = true_values / total
    
    return accuracy

def error_rate(confusion_matrix):
    err = 1 - accuracy(confusion_matrix)
    
    return err

def individual_precision_list(confusion_matrix):
    cols = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix)):
            cols[j] += confusion_matrix[i][j]
    
    individual_precision = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        if cols[i] > 0:
            individual_precision[i] = confusion_matrix[i][i] / cols[i]
        
    return individual_precision

def macro_precision(confusion_matrix):
    precision = list_mean(individual_precision_list(confusion_matrix))
    
    return precision

def individual_recall_list(confusion_matrix):
    lines = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            lines[i] += confusion_matrix[i][j]

    individual_recall = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        individual_recall[i] = confusion_matrix[i][i] / lines[i]    
    
    return individual_recall

def macro_recall(confusion_matrix):
    recall = list_mean(individual_recall_list(confusion_matrix))
    
    return recall

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
    
    return individual_specificity

def macro_specificity(confusion_matrix):
    specificity = list_mean(individual_specificity_list(confusion_matrix))
    
    return specificity

def f1_score(confusion_matrix):
    prec = macro_precision(confusion_matrix)
    recall = macro_recall(confusion_matrix)
    score = (2 * prec * recall) / (prec + recall)

    return score

def print_metrics(acc, err, prec_macro, prec_ind, rev_macro, rev_ind, spec_macro, spec_ind, f_score):
    print("Acurácia: ", acc)
    print("Taxa de erro: ", err, '\n')

    print("Precisão(macro): ", prec_macro)
    for i in range(len(prec_ind)):
        print("  Precisão(" + ohe.categories_[0][i] + "): ", prec_ind[i])

    print('\n', "Recall(macro): ", rev_macro)
    for i in range(len(rev_ind)):
        print("  Recall(" + ohe.categories_[0][i] + "): ", rev_ind[i])

    print('\n', "Especificidade(macro): ", spec_macro)
    for i in range(len(spec_ind)):
        print("  Especificidade(" + ohe.categories_[0][i] + "): ", spec_ind[i])
    
    print('\n', "F1-score: ", f_score)