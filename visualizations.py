import matplotlib.pyplot as plt

def compare_boxplot(metrics_names, trainers, trainer_name, labels, width=22, height=10):
    number_metrics = len(metrics_names)
    number_type_trainers = len(trainers)

    fig, ax = plt.subplots(number_type_trainers, number_metrics, figsize=(width, height))
    fig.suptitle(trainer_name)

    for idx_trainer, trainers in enumerate(trainers):
        for idx_metric, metric in enumerate(metrics_names):
            results=[]
            for trainer in trainers:
                results.append(trainer.get_metric(metric))

            ax[idx_trainer][idx_metric].boxplot(results, labels=labels, showmeans=True)
    
            ax[idx_trainer][idx_metric].set_title(metric)
