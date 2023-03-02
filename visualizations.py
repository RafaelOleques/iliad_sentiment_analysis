import matplotlib.pyplot as plt

def compare_boxplot(dict_metrics, labels, width=22, height=10):
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
        number_type_trainers = len(result[title])

        firts_key = list(result[title].keys())[0]
        number_metrics = len(result[title][firts_key])

        print(number_type_trainers, number_metrics)
        
        fig, ax = plt.subplots(number_type_trainers, number_metrics, figsize=(width, height))
        print(ax.shape)
        fig.suptitle(title)
        print(title)

        scenarios = result[title]

        for idx_scenario, scenario in enumerate(scenarios):
            metrics = scenarios[scenario]
            for idx_metric, metric in enumerate(metrics):
                results=[]

                for values in metrics[metric]:
                    results.append(values)

                #ax[idx_scenario][idx_metric].set_ylim(bottom=0, top=100)
                print(idx_scenario, idx_metric, results)
                ax[idx_scenario][idx_metric].boxplot(results, labels=labels, showmeans=True)
        
                ax[idx_scenario][idx_metric].set_title(metric)
