import matplotlib.pyplot as plt

def compare_boxplot(dict_metrics, labels, width=20, height=5):
    plots = []
    result = {}
    
    for model in dict_metrics:
        result[model] = {}
    
    #plot
    for model in dict_metrics:
        #line
        for scenario in dict_metrics[model]:
            if scenario not in result[model]:
                result[model][scenario] = {}
            #Values
            for data_operation in dict_metrics[model][scenario]:
                for metric in dict_metrics[model][scenario][data_operation]:
                    if metric not in result[model][scenario]:
                        result[model][scenario][metric] = []
                        result[model][scenario][metric].append(dict_metrics[model][scenario][data_operation][metric])
                    else:
                        result[model][scenario][metric].append(dict_metrics[model][scenario][data_operation][metric])
    
    for title in result:
        #number_type_trainers = len(result[title])

        firts_key = list(result[title].keys())[0]
        number_metrics = len(result[title][firts_key])

        #print(number_type_trainers, number_metrics)

        scenarios = result[title]

        for idx_scenario, scenario in enumerate(scenarios):
            print("===>", number_metrics//2, 2)
            fig, ax = plt.subplots(number_metrics//2, 2, figsize=(width, height))
            fig.suptitle(f"{title} utilizando {scenario}")
        
            metrics = scenarios[scenario]

            line = 0
            collum = 0
            for idx_metric, metric in enumerate(metrics):
                results=[]

                if idx_metric %2 == 0 and idx_metric != 0:
                    line += 1
                    collum = 0


                print(line, idx_metric)

                for values in metrics[metric]:
                    results.append(values)

                ax[line][collum].set_ylim(bottom=0, top=100)
                print(idx_scenario, idx_metric, results)
                ax[line][collum].boxplot(results, labels=labels, showmeans=True)
        
                ax[line][collum].set_title(metric)

                collum += 1
