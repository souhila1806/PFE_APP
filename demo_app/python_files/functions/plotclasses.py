from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QGridLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout,QSizePolicy
from sklearn.metrics import roc_curve
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pchs
import matplotlib.colors as mcolors
import matplotlib.patheffects as path_effects
from python_files.utils import cross_val
from PyQt5.QtCore import QThread, pyqtSignal
from ..loading import LoadingScreen
import threading

class PlotWidget(QFrame):
    def __init__(self,data, parent=None):
        super(PlotWidget, self).__init__(parent)

        # Create a Figure object and a FigureCanvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


    def plot(self, data):
        print(f"distribution {data}")
        half = int(data.shape[0] / 2)
        bins = np.linspace(-1, 1, 120)
        self.figure.clear()  # Clear the previous plot

        # Create the subplots within the figure
        ax = self.figure.add_subplot(111)

        # Extract the data for plotting
        x = data.iloc[0:half, 0]
        y = data.iloc[half:, 0]
        colors = ['mediumpurple', 'mediumaquamarine']

        # Plot the histograms
        ax.hist([x, y], bins, alpha=1, color=colors, label=['matched', 'mismatched'])
        ax.set_xlim(-0.3, 1)
        ax.set_xticks(np.arange(-1, 1, step=0.1))
        ax.legend(loc='upper right')

        self.canvas.draw()


class RocCurvePlotWidget(QFrame):
    def __init__(self, data, model, parent=None):
        super(RocCurvePlotWidget, self).__init__(parent)

        # Create a Figure object and a FigureCanvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)


    def plot(self, data,model):
        half = int(data.shape[0] / 2)
        y_pred = np.concatenate((np.zeros(half), np.ones(half)))
        fpr, tpr, thresholds = roc_curve(y_pred, data, pos_label=1)

        self.figure.clear()  # Clear the previous plot

        # Create the subplots within the figure
        ax = self.figure.add_subplot(111)

        # Plot the ROC curve
        ax.plot(tpr, fpr, color='mediumpurple', label=model)
        ax.plot([0, 1], ls="--", color='mediumaquamarine', label="random classifier")
        ax.set_title('Receiver Operating Characteristic')
        ax.set_ylabel('Correct acceptance')
        ax.set_xlabel('False acceptance')

        ax.legend()

        # Draw the plot on the canvas
        self.canvas.draw()

class MagnitudePlotWidget(QFrame):
    def __init__(self,rest, parent=None):
        super(MagnitudePlotWidget, self).__init__(parent)
        self.setFixedSize(1500, 400)
        # Create a Figure object and a FigureCanvas
        self.figure = Figure(figsize=(35, 5))
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, model):
        print(model)
        data = pd.read_csv(r"data\files\magnitude_file.csv")

        self.figure.clear()
        # Create the subplots within the figure
        axs = self.figure.subplots(1, 4)

        y_max = 550
        box_colors = ['skyblue', 'lightgreen', 'mediumpurple', 'mediumaquamarine']

        models = ['xqlfw', 'gfpgan', 'gpen', 'sgpn']  # List of available models

        for i, model_name in enumerate(models):
            magnitude_values = data[f'mag_{model_name}'].values
            color = box_colors[i]

            axs[i].hist(magnitude_values, bins=50, color=color, edgecolor='black')
            axs[i].set_xlabel('Magnitude')
            if i==0:
                axs[i].set_ylabel('Frequency')
            axs[i].set_ylim(0, y_max)

            if model == model_name:
                title=axs[i].set_title(model_name.upper(), color='black', fontweight='bold')
                #title.set_path_effects([path_effects.withStroke(linewidth=2, foreground='yellow')])
            else:
                axs[i].set_title(model_name.upper())

            # Highlight the selected model's plot with a rectangle
            if model == model_name:
                print(f"modellllllll {model} ")
                xmin, xmax = axs[i].get_xlim()
                ymin, ymax = axs[i].get_ylim()
                rect = pchs.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=4, edgecolor='yellow',
                                         facecolor='none')
                axs[i].add_patch(rect)
                pastel_yellow = mcolors.hsv_to_rgb((0.16, 0.3, 1.0))  # Adjust HSV values for pastel yellow
                axs[i].set_facecolor(pastel_yellow)

        # Adjust the spacing between subplots
        self.figure.subplots_adjust(wspace=0.1)

        # Draw the plot on the canvas
        self.canvas.draw()


class SimilarityPlotWidget(QFrame):
    def __init__(self,model,rest, parent=None):
        super(SimilarityPlotWidget, self).__init__(parent)
        self.setFixedSize(1100, 400)
        # Create a Figure objct and a FigureCanvas
        self.figure = Figure(figsize=(35, 5))
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)



    def plot(self,model,rest):
        data=pd.read_csv(r"data\files\simIndex_file.csv")
        self.figure.clear()
        # Set the width of the entire figure
        axs = self.figure.subplots(1, 3)  # Adjust the width as desired

        y_max = 700
        col=model.lower()[:3]
        box_colors = ['lightgreen', 'mediumpurple', 'mediumaquamarine']
        models = ['gfpgan', 'gpen', 'sgpn']  # List of available models

        for i, model_name in enumerate(models):
            # Plotting the first histogram
            color=box_colors[i]
            magnitude_values = data[f"{col}_{model_name}"].values
            axs[i].hist(magnitude_values, bins=50, color=color, edgecolor='black')
            axs[i].set_xlabel('Similarity')
            if i==0:
                axs[i].set_ylabel('Frequency')

            if rest == model_name:
                axs[i].set_title(model_name.upper(), color='black', fontweight='bold')
                #title.set_path_effects([path_effects.withStroke(linewidth=2, foreground='yellow')])
            else:
                axs[i].set_title(model_name.upper())

            axs[i].set_ylim(0, y_max)
            if rest == model_name:
                print(f"modellllllll {rest} ")
                xmin, xmax = axs[i].get_xlim()
                ymin, ymax = axs[i].get_ylim()
                rect = pchs.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=4, edgecolor='yellow',
                                         facecolor='none')
                axs[i].add_patch(rect)
                pastel_yellow = mcolors.hsv_to_rgb((0.16, 0.3, 1.0))  # Adjust HSV values for pastel yellow
                axs[i].set_facecolor(pastel_yellow)


        # Adjust the spacing between subplots
        self.figure.subplots_adjust(wspace=0.2)

        # Draw the plot on the canvas
        self.canvas.draw()

class RegressionPlotWidget(QFrame):
    def __init__(self,fusiontype,rec_model,rest_model, parent=None):
        super(RegressionPlotWidget, self).__init__(parent)
        self.setFixedSize(750,1500)
        # Create a Figure objct and a FigureCanvas
        self.figure = Figure(figsize=(20, 105))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow figure to expand

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.fusiontype=fusiontype
        self.rec_model=rec_model
        self.rest_model=rest_model

    def plot(self, fusiontype, rec_model, rest_model):
        try:
            self.thread = ProcessThread(fusiontype, rec_model, rest_model)
            self.thread.finished.connect(self.handle_finished)

            # Start the thread

            print("Current Thread Name 1:",threading.current_thread().name)

            self.thread.start()
            self.thread.wait()
            print("Current Thread Name2:",threading.current_thread().name)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def handle_finished(self, result):
        print("name 3",threading.current_thread().name)
        coeff, data, loading_screen = result
        self.figure.clear()
        # Set the width of the entire figure
        axs = self.figure.subplots(5, 2)
        self.figure.subplots_adjust(top=0.92, bottom=0.08, hspace=0.4)
        half = 300
        column_values = np.concatenate((np.ones(half), np.zeros(half)))
        colors = ['#0F9DE8' if label == 1 else '#660099' for label in column_values]

        for i, ax in enumerate(axs.flatten()):
            _, test = cross_val(data, i)
            test['label'] = column_values
            columns = test.columns
            x_col = columns[0]  # Assuming the first column is for the x-axis
            y_col = columns[1]
            test.plot.scatter(x=x_col, y=y_col, c=colors, ax=ax, label=None)
            ax.set_xlabel(f"{self.rest_model[0]} scores")
            if i%2 == 0:
                ax.set_ylabel(f"{self.rest_model[1]} scores")
            else:
                ax.set_ylabel("")
            ax.set_title(f'fold {i}')

            a = coeff.iloc[i, 0]
            b = coeff.iloc[i, 1]
            c = coeff.iloc[i, 2]

            s1_range = np.linspace(test[x_col].min(), test[y_col].max(), 100)

            # Calculate corresponding s2 values based on the line equation
            s2_range = (-c - a * s1_range) / b

            ax.plot(s1_range, s2_range, 'r', label='f(s1, s2)' if i == 0 else None)
            if i == 0:
                ax.legend()

            # Draw the plot on the canvas
            self.canvas.draw()
            loading_screen.stopLoading()



class ProcessThread(QThread):
    finished = pyqtSignal(object)

    def __init__(self, fusiontype,rec_model,rest_model):
        super().__init__()
        self.loading_screen = LoadingScreen()
        self.loading_screen.startLoading()
        print("name4 ", threading.current_thread().name)
        self.fusiontype = fusiontype
        self.rec_model = rec_model
        self.rest_model = rest_model


    def run(self):
        print("name5 ", threading.current_thread().name)
        fusiontype = self.fusiontype
        rec_model = self.rec_model
        rest_model = self.rest_model
        self.directory = pd.read_csv(
            rf"data\files\{fusiontype}_coefficients.csv")
        # get column name in coefficient file
        col = f"{fusiontype[0]}f_{rest_model[0].lower()}_{rest_model[1].lower()}_{rec_model.lower()}"
        if not any(self.directory['name'].str.contains(col)):
            col = f"{fusiontype[0]}f_{rest_model[1].lower()}_{rest_model[0].lower()}_{rec_model.lower()}"
        # get the coefficients
        coeff = self.directory[self.directory['name'] == col].reset_index(drop=True)
        coeff = coeff.drop('name', axis=1)

        if fusiontype == "score":
            xqlfw = pd.read_csv(r"data\files\xqlfw_scores.csv")
            col1 = f"{rec_model.lower()}_{rest_model[0].lower()}"
            col2 = f"{rec_model.lower()}_{rest_model[1].lower()}"
            # get the data
            data = pd.concat([xqlfw[col1], xqlfw[col2]], axis=1)
        else:
            print("hybrid fusion")
            xqlfw = pd.read_csv(r"data\files\xqlfw_scores.csv")
            ff = pd.read_csv(r"data\files\feature_fusion_scores.csv")
            if len(rest_model) == 2:  # if there are 2 models in feature level fusion
                col1 = f"ff_{rest_model[0].lower()}_{rest_model[1].lower()}_{rec_model.lower()}"
                if col1 not in ff.columns:
                    col1 = f"ff_{rest_model[1].lower()}_{rest_model[2].lower()}_{rec_model.lower()}"
                rest_l2 = [element for element in ["GFPGAN", "SGPN", "GPEN"] if element not in rest_model]
                col2 = f"{rec_model.lower()}_{rest_l2[0].lower()}"
            else:  # all
                col1 = f"ff_all_{rec_model.lower()}"
                col2 = f"{rec_model.lower()}_gfpgan"
            data = pd.concat([ff[col1], xqlfw[col2]], axis=1)

        result = coeff,data,self.loading_screen
        self.finished.emit(result)

if __name__ == '__main__':
    try:
        fusiontype="score fusion"
        rec_model= "arcface"
        rest_model=["sgpn","gpen"]
        reg=RegressionPlotWidget(fusiontype,rec_model,rest_model)
        app = QApplication([])
        window = QWidget()
        layout = QGridLayout()
        layout.addWidget(reg)
        window.setLayout(layout)

        window.show()
        app.exec_()
    except Exception as e:
        import traceback
        traceback.print_exc()

