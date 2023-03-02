def metricas(confusion_matrix):
    total = 0
    verdadeiros = 0
    lines = [0] * len(confusion_matrix)
    cols = [0] * len(confusion_matrix)
    vn = [0] * len(confusion_matrix)
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix[i])):
            total += confusion_matrix[i][j]
            lines[i] += confusion_matrix[i][j]
            cols[j] += confusion_matrix[i][j]
            vn[i] -= confusion_matrix[i][j]
            vn[j] -= confusion_matrix[i][j]
            if i == j:
                vn[i] += confusion_matrix[i][j]
                verdadeiros += confusion_matrix[i][j]
    
    for i in range(len(vn)):
        vn[i] += total

    acuracia = verdadeiros / total
    taxa_de_erro = 1 - acuracia
    precisao_individual = [0] * len(confusion_matrix)
    recall_individual = [0] * len(confusion_matrix)
    especificidade_individual = [0] * len(confusion_matrix)
    
    for i in range(len(confusion_matrix)):
        recall_individual[i] = confusion_matrix[i][i] / lines[i]
        precisao_individual[i] = confusion_matrix[i][i] / cols[i]
        especificidade_individual[i] = vn[i] / (cols[i] - confusion_matrix[i][i] + vn[i])
    
    precisao_macro = 0
    recall_macro = 0
    especificidade_macro = 0
    for i in range(len(confusion_matrix)):
        precisao_macro += precisao_individual[i]
        recall_macro += recall_individual[i]
        especificidade_macro += especificidade_individual[i]
        
    precisao_macro /= len(confusion_matrix)
    recall_macro /= len(confusion_matrix)
    especificidade_macro /= len(confusion_matrix)
    
    return  acuracia, taxa_de_erro, precisao_macro, precisao_individual, recall_macro, recall_individual, especificidade_macro, especificidade_individual

def print_metricas(acc, err, prec_macro, prec_ind, rev_macro, rev_ind, spec_macro, spec_ind):
    print("Acurácia: ", acc)
    print("Taxa de erro: ", err, '\n')

    print("Precisão(macro): ", prec_macro)
    for i in range(len(cm_test)):
        print("  Precisão(" + ohe.categories_[0][i] + "): ", prec_ind[i])

    print('\n', "Recall(macro): ", rev_macro)
    for i in range(len(cm_test)):
        print("  Recall(" + ohe.categories_[0][i] + "): ", rev_ind[i])

    print('\n', "Especificidade(macro): ", spec_macro)
    for i in range(len(cm_test)):
        print("  Especificidade(" + ohe.categories_[0][i] + "): ", spec_ind[i])

