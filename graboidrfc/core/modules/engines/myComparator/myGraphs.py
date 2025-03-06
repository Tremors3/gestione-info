
# Importazione standard
import matplotlib.pyplot as plt
import numpy as np
import os

# Importazione tipi per documentazione
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes

# Importazione di moduli del progetto
from graboidrfc.core.modules.utils.logger import logger as logging, bcolors
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path
from graboidrfc.core.modules.engines.myComparator.myComparator import MyComparator

class MyGraphs:
    
    # Graph options
    MARKERS = {
        'BM25':'o',
        'BM25_CUSTOM':'s',
        'TFIDF':'v',
        'TFIDF_CUSTOM':'d',
        'VSM':'v',
        'VSM_CUSTOM':'d',
    }

    MOSAIC = [
        ['whoosh','pylucene'],
        ['postgresql','.']
    ]

    GRAPH_COLORS = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    
    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))

    # SETTINGS FILE PATHS
    SETTINGS_FILE_PATH = os.path.join(
        DYNAMIC_PACKAGE_PATH, "core", "config", "comparator.json"
    )

    # GRAPH FILE PATHS
    OUTPUT_GRAPH_FOLDER = os.path.join(
        DYNAMIC_PACKAGE_PATH, "core", "data", "graphs"
    )

    # ######################################################################## #
    
    @staticmethod
    def __get_comparator() -> MyComparator:
        comparator = MyComparator()
        return comparator

    @staticmethod
    def __get_query_index(r: dict) -> list[str]:
        """Restituisce una lista di indici estratta dai risultati passati"""

        queries = list(
            r[list(r.keys())[0]] \
            [list(r[list(r.keys())[0]].keys())[0]] \
            ["avg_prec_of_queries"].keys()
        )
        return queries

    @classmethod
    def __line_plot_engine(cls, ax: Axes, res:dict, e: str, 
                           y_label: str, num = None) -> None:
        """
        Fa il grafico sia per le singole query-engine sia per la 
        media della precisione degli engine
        """

        ax.clear()
        if num == None:
            # Grafico per la precisione media degli engine
            for ranking, values in res[e].items():
                recall = list(values["avg_prec_at_std_rec_lvls"].keys())
                precision = list(values["avg_prec_at_std_rec_lvls"].values())
                ax.plot(
                    recall, precision, 
                    marker=cls.MARKERS[ranking], label=ranking
                )
            
        else:
            # Grafico per query-engine
            for ranking, values in res[num][e].items():
                recall = list(values["recall_precision"].keys())
                precision = list(values["recall_precision"].values())
                ax.plot(
                    recall, precision, 
                    marker=cls.MARKERS[ranking], label=ranking
                )
 
        ax.set_xticks(recall)
        ax.set_yticks(recall)
        ax.grid(True)
        ax.set_ylabel(y_label) 
        ax.set_xlabel('Recall')
        ax.set_title(e.capitalize())
        ax.legend()

    @classmethod
    def __plot_map(cls, ax: Axes, e: str, lab: str, vals: list[float], 
                   y_tick: list[float]) -> None:
        """Fa il grafico per la Mean Average Precision"""
        
        ax[e].bar(lab, vals, zorder=2, color=cls.GRAPH_COLORS)
        ax[e].set_title(e.capitalize())
        ax[e].set_ylim(0.0, 1.0)
        ax[e].set_xlabel('Ranking models') 
        ax[e].set_ylabel('MAP (Mean Average Precision)') 
        ax[e].set_yticks(y_tick)
        ax[e].grid(True, zorder=0)

    @staticmethod
    def __bar_plot_queries(ax: Axes, res: dict, e: str, width: float, x, 
                           queries: list[str], y_tick: list[float], 
                           field: str, lab_x: str, lab_y: str) -> None:
        """Fa l'istogramma per le query eseguite in ogni search engine"""
        
        ax.clear()
        offset = 0
        multiplier = 0  

        for ranking, values in res[e].items():
            ranking_results = list(values[field].values())

            offset = width * multiplier
            ax.bar(x + offset, ranking_results, width, label=ranking, zorder=2)
            multiplier+=1

        ax.set_title(e.capitalize())
        ax.set_ylim(0.0, 1.0)
        ax.set_xlabel(lab_x) 
        ax.set_ylabel(lab_y) 
        ax.set_xticks(x + width, queries)
        ax.set_yticks(y_tick)
        ax.legend(ncols=2)
        ax.grid(True, zorder=0)

    @classmethod
    def __save_plot_to_file(cls, figure: Figure, subdir: str, filename: str) -> None:
        """Salva il grafico su file"""

        # Controllo presenza directory
        dir_path = os.path.join(cls.OUTPUT_GRAPH_FOLDER, subdir)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        
        # Check del nome del file inserito
        if not filename:
            logging.warning(f"Il nome del file \'{filename}\' non è valido.")
            return
        file_path = os.path.join(dir_path, filename)
        
        # Scrittura del grafico su file
        figure.savefig(file_path)

    @staticmethod
    def __get_values(res: dict, e: str, field: str) -> list[float]:
        """
        Restituisce una lista con i valori del field richiesto
        per ogni funzione di ranking del search engine passato
        """

        vals = []
        for r in res[e].keys():
            vals.append(res[e][r][field])
        return vals

    @staticmethod
    def __get_ticks(n: int) -> list[float]:
        """Genera i 'tick' per l'asse delle ordinate 0/n ... n/n"""

        if not n: return 0
        return [i/n for i in range(n+1)]
    
    # ######################################################################## #
    
    @classmethod
    def graph_by_query(cls):
        comparator = cls.__get_comparator()
        
        # Prende i risultati per recall e precision per ogni singola query
        results = comparator.calc_all_recall_precision_by_query()
        
        for number in results.keys():
            fig = plt.figure(layout="constrained", figsize=[10.0, 10.0])
            ax_array = fig.subplot_mosaic(cls.MOSAIC)
            
            for engine in results[number].keys():
                engine = engine.lower()

                # Disegna il grafico per la precision per ogni modello di 
                # ranking della singola query
                cls.__line_plot_engine(
                    ax=ax_array[engine],
                    res=results,
                    e=engine,
                    num=number,
                    y_label="Precision"
                )
            cls.__save_plot_to_file(fig, "prec_rec", f"{number}.svg")

            for engine in results[number].keys():

                # Disegna il grafico per l'F Measure (Harmonic mean)
                cls.__bar_plot_queries(
                    ax=ax_array[engine],
                    res=results[number],
                    e=engine,
                    width=0.1,
                    x=np.arange(len(cls.__get_ticks(10))),
                    queries=cls.__get_ticks(10),
                    y_tick=cls.__get_ticks(10),
                    field="f_measure",
                    lab_x="Recall",
                    lab_y="F Measure"
                )
            
            # Salva il grafico su file
            cls.__save_plot_to_file(fig, "f_measure", f"fm_query_{number}.svg")

    @classmethod
    def graph_by_engine(cls):
        comparator = cls.__get_comparator()

        # Prende i risultati per la recall e la precision per ogni modello 
        # di ranking per ogni engine
        results = comparator.calc_all_recall_precision_by_engine()
        
        # Impostazioni per il grafico a linee
        fig = plt.figure(layout="constrained", figsize=[10.0, 10.0])
        ax = fig.subplots()

        # Prende gli indici delle query
        queries = cls.__get_query_index(results)

        # Impostazioni per l'istogramma
        fig2, ax2 = plt.subplots(layout='constrained', figsize=[10.0, 5.0])
        y_tick = cls.__get_ticks(10)
        x = np.arange(len(queries))
        width = 0.2
        
        for engine in results.keys():
            engine = engine.lower()
            
            # Disegna il grafico per l'Average precision per recall level
            cls.__line_plot_engine(
                ax=ax,
                res=results,
                e=engine,
                y_label='Average Precision (recall level)'
            )

            # Salva il grafico su file
            cls.__save_plot_to_file(fig, "avg_prec_level", f"engine_{engine}.svg")

            for _ in queries:

                # Disegna il grafico per l'Average Precision delle query 
                cls.__bar_plot_queries(
                    ax2,
                    results,
                    engine,
                    width,
                    x,
                    queries,
                    y_tick,
                    field = "avg_prec_of_queries",
                    lab_x="Queries",
                    lab_y="Average Precision (query)"
                )

                # Salva il grafico su file
                cls.__save_plot_to_file(fig2, "avg_prec_query", f"queries_{engine}.svg")

                # Disegna il grafico per la NDCG
                cls.__bar_plot_queries(
                    ax2,
                    results,
                    engine,
                    width,
                    x,
                    queries,
                    y_tick,
                    field="ndcg",
                    lab_x="Queries",
                    lab_y="NDGC"
                )

                # Salva il grafico su file
                cls.__save_plot_to_file(fig2, "ndgc", f"ndgc_{engine}.svg")

    @classmethod
    def graph_map(cls):
        comparator = cls.__get_comparator()
        
        # Prende recall e precision
        results = comparator.calc_all_recall_precision_by_engine()

        # Impostazioni per il grafico
        fig = plt.figure(layout="constrained", figsize=[10.0, 10.0])
        ax_array = fig.subplot_mosaic(cls.MOSAIC)
        
        # Tick per l'asse delle ordinate
        y_tick = cls.__get_ticks(10)

        for engine in results.keys():
            values = []

            # Pulisce i label
            labels = [i.replace("_"," ") for i in results[engine].keys()]

            # Prende i valori per la Mean Average Precision
            values = cls.__get_values(results, engine, field='map')
            
            # Disegna il grafico
            cls.__plot_map(
                ax_array,
                engine,
                labels,
                values,
                y_tick
            )
        
        # Salva i lgrafico
        cls.__save_plot_to_file(fig, "map", "map.svg")

    # ######################################################################## #
    
    def start():
        """ Graphs Entry Point """
        MyGraphs.graph_by_query()
        MyGraphs.graph_by_engine()
        MyGraphs.graph_map()
        logging.debug(f"Grafici salvati al seguente percorso: \'{__class__.OUTPUT_GRAPH_FOLDER}\'")

if __name__ == "__main__":
    MyGraphs.start()