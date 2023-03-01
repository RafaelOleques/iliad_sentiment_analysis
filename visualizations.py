import matplotlib.pyplot as plt

def compare_boxplot(metrics_names, trainers, trainer_name, labels, width=22, height=5):
    number_metrics = len(metrics_names)

    fig, ax = plt.subplots(1, number_metrics, figsize=(width, height))
    fig.suptitle(trainer_name)

    for idx, metric in enumerate(metrics_names):
        results=[]
        for trainer in trainers:
            results.append(trainer.get_metric(metric))

        ax[idx].boxplot(results, labels=labels, showmeans=True)
    
    ax[idx].set_title(metric)
