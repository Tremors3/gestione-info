import matplotlib.pyplot as plt
import numpy as np
import os
from pprint import pprint

from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path
from graboidrfc.core.modules.engines.myComparator.myComparator import MyComparator

comparator = MyComparator()
markers = {
    'BM25':'o',
    'BM25_CUSTOM':'s',
    'TFIDF':'v',
    'TFIDF_CUSTOM':'d',
    'VSM':'v',
    'VSM_CUSTOM':'d',
}

# CURRENT WORKING DIRECTORY & FILE PATHS
DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))

# SETTINGS FILE PATHS
SETTINGS_FILE_PATH = os.path.join(
    DYNAMIC_PACKAGE_PATH, "core", "config", "comparator.json"
)

# RESULTS FILE PATHS
BENCHMARK_FOLDER = os.path.join(
    DYNAMIC_PACKAGE_PATH, "core", "data", "benchmark", "graphs"
)

def graph_by_query():
    results = comparator.calc_all_recall_precision_by_query()

    # fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    for number in results.keys():
        fig = plt.figure(layout="constrained", figsize=[10.0, 10.0])
        ax_array = fig.subplot_mosaic(
            [
                ['whoosh','pylucene'],
                ['postgresql','.']
            ]
            
        )

        for engine in results[number].keys():
            engine = engine.lower()
            for ranking, values in results[number][engine].items():
                recall = values.keys()
                precision = values.values()
                
                ax_array[engine].plot(
                    list(recall), list(precision), 
                    marker=markers[ranking], label=ranking
                )

                x = [i/10 for i in range(11)]

            ax_array[engine].set_xticks(list(recall))
            ax_array[engine].set_yticks(list(recall))
            ax_array[engine].grid(True)
            ax_array[engine].set_xlabel('Recall')
            ax_array[engine].set_ylabel('Precision') 
            ax_array[engine].set_title(engine.capitalize())
            ax_array[engine].legend()  
        
        fig.savefig(os.path.join(BENCHMARK_FOLDER, f"{number}.svg"))

def graph_by_engine():
    results = comparator.calc_all_recall_precision_by_engine()

    # Prende gli indici delle query
    queries = list(results[list(results.keys())[0]][list(results[list(results.keys())[0]].keys())[0]]["avg_prec_of_queries"].keys())
    x = np.arange(len(queries))
    
    fig = plt.figure(layout="constrained", figsize=[10.0, 10.0])
    ax = fig.subplots()

    fig2, ax2 = plt.subplots(layout='constrained', figsize=[10.0, 5.0])
    y_tick = [i/10 for i in range(11)]
    
    width = 0.2

    for engine in results.keys():
        engine = engine.lower()
        for ranking, values in results[engine].items():
            recall = values["avg_prec_at_std_rec_lvls"].keys()
            precision = values["avg_prec_at_std_rec_lvls"].values()
            ax.plot(
                list(recall), list(precision), 
                marker=markers[ranking], label=ranking
            )

        ax.set_xticks(list(recall))
        ax.set_yticks(list(recall))
        ax.grid(True)
        ax.set_xlabel('Recall')
        ax.set_ylabel('Average Precision (recall level)') 
        ax.set_title(engine.capitalize())
        ax.legend()  
        fig.savefig(os.path.join(BENCHMARK_FOLDER, f"{engine}.svg"))
        ax.clear()

        for query in queries:                    
            offset = 0
            multiplier = 0  

            for ranking in results[engine].keys():
                ranking_results = list(results[engine][ranking]["avg_prec_of_queries"].values())

                offset = width * multiplier
                rects = ax2.bar(x + offset, ranking_results, width, label=ranking, zorder=2)
                multiplier+=1

            ax2.set_title(engine.capitalize())
            ax2.set_ylim(0.0, 1.0)
            ax2.set_xlabel('Queries') 
            ax2.set_ylabel('Average Precision (query)') 
            ax2.set_xticks(x + width, queries)
            ax2.set_yticks(y_tick)
            ax2.legend(ncols=2)
            ax2.grid(True, zorder=0)
            fig2.savefig(os.path.join(BENCHMARK_FOLDER, f"queries_{engine}.svg"))
            ax2.clear()


def map_graph():
    results = comparator.calc_all_recall_precision_by_engine()
    x = np.arange(len(results))

    fig = plt.figure(layout="constrained", figsize=[10.0, 10.0])
    ax_array = fig.subplot_mosaic(
        [
            ['whoosh','pylucene'],
            ['postgresql','.']
        ]
        
    )
    y_tick = [i/10 for i in range(11)]

    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]

    for engine in results.keys():
        values = []
        offset = 0
        
        labels = [i.replace("_"," ") for i in results[engine].keys()]

        values = []
        for ranking in results[engine].keys():
            values.append(results[engine][ranking]['map'])
        # print(labels)
        # print(values)
        ax_array[engine].bar(labels, values, zorder=2, color=colors)
        ax_array[engine].set_title(engine.capitalize())
        ax_array[engine].set_ylim(0.0, 1.0)
        ax_array[engine].set_xlabel('Ranking models') 
        ax_array[engine].set_ylabel('MAP (Mean Average Precision)') 
        
        ax_array[engine].set_yticks(y_tick)
        # ax_array[engine].legend(ncols=3)
        ax_array[engine].grid(True, zorder=0)
    fig.savefig(os.path.join(BENCHMARK_FOLDER, "map.svg"))
    # plt.show()
    # print(results)

map_graph()
# graph_by_query()
# graph_by_engine()