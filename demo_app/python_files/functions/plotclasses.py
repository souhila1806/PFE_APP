from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout
from sklearn.metrics import roc_curve
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from python_files.utils import cross_val
import sys

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

        # Create your plot using the figure object
        self.plot(data)

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
        colors = ['red', 'blue']

        # Plot the histograms
        ax.hist([x, y], bins, alpha=0.5, color=colors, label=['matched', 'mismatched'])
        ax.set_xlim(-0.3, 1)
        ax.set_xticks(np.arange(-1, 1, step=0.1))
        ax.legend(loc='upper right')

        self.canvas.draw()


class RocCurvePlotWidget(QFrame):
    def __init__(self, data, parent=None):
        super(RocCurvePlotWidget, self).__init__(parent)

        # Create a Figure object and a FigureCanvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Create your plot using the figure object
        self.plot(data)

    def plot(self, data):
        half = int(data.shape[0] / 2)
        y_pred = np.concatenate((np.zeros(half), np.ones(half)))
        fpr, tpr, thresholds = roc_curve(y_pred, data, pos_label=1)

        self.figure.clear()  # Clear the previous plot

        # Create the subplots within the figure
        ax = self.figure.add_subplot(111)

        # Plot the ROC curve
        ax.plot(tpr, fpr)
        ax.plot([0, 1], ls="--")
        ax.set_title('Receiver Operating Characteristic')
        ax.set_ylabel('Correct acceptance')
        ax.set_xlabel('False acceptance')

        # Draw the plot on the canvas
        self.canvas.draw()

class MagnitudePlotWidget(QFrame):
    def __init__(self, parent=None):
        super(MagnitudePlotWidget, self).__init__(parent)

        # Create a Figure objct and a FigureCanvas
        self.figure = Figure(figsize=(35, 5))
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Create your plot using the figure object
        self.plot()

    def plot(self):
        data= pd.read_csv(r"demo_app\data\files\magnitude_file.csv")

        self.figure.clear()
        # Create the subplots within the figure
        axs = self.figure.subplots(1, 4)
        y_max = 550
        box_colors = ['skyblue', 'lightgreen', 'mediumpurple', 'mediumaquamarine']

        # Plotting the first histogram
        magnitude_values = data['mag_xqlfw'].values
        axs[0].hist(magnitude_values, bins=50, color='skyblue', edgecolor='black')
        axs[0].set_xlabel('Magnitude')
        axs[0].set_ylabel('Frequency')
        axs[0].set_title('XQLFW')
        axs[0].set_ylim(0, y_max)

        # Plotting the second histogram
        magnitude_values = data['mag_gfpgan'].values
        axs[1].hist(magnitude_values, bins=50, color='lightgreen', edgecolor='black')
        axs[1].set_xlabel('Magnitude')
        axs[1].set_ylabel('Frequency')
        axs[1].set_title('GFP-GAN')
        axs[1].set_ylim(0, y_max)

        # Plotting the first histogram
        magnitude_values = data['mag_gpen'].values
        axs[2].hist(magnitude_values, bins=50, color='mediumpurple', edgecolor='black')
        axs[2].set_xlabel('Magnitude')
        axs[2].set_ylabel('Frequency')
        axs[2].set_title('GPEN')
        axs[2].set_ylim(0, y_max)

        # Plotting the first histogram
        magnitude_values = data['mag_sgpn'].values
        axs[3].hist(magnitude_values, bins=50, color='mediumaquamarine', edgecolor='black')
        axs[3].set_xlabel('Magnitude')
        axs[3].set_ylabel('Frequency')
        axs[3].set_title('SGPN')
        axs[3].set_ylim(0, y_max)


        # Adjust the spacing between subplots
        self.figure.subplots_adjust(wspace=0.2)

        # Draw the plot on the canvas
        self.canvas.draw()

class SimilarityPlotWidget(QFrame):
    def __init__(self,model, parent=None):
        super(SimilarityPlotWidget, self).__init__(parent)

        # Create a Figure objct and a FigureCanvas
        self.figure = Figure(figsize=(35, 5))
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Create your plot using the figure object
        self.plot(model)

    def plot(self,model):
        data=pd.read_csv(r"demo_app\data\files\simIndex_file.csv")
        self.figure.clear()
        # Set the width of the entire figure
        axs = self.figure.subplots(1, 3)  # Adjust the width as desired

        y_max = 700
        col=model.lower()[:3]

        # Plotting the first histogram
        magnitude_values = data[f"{col}_gfpgan"].values
        axs[0].hist(magnitude_values, bins=50, color='lightgreen', edgecolor='black')
        axs[0].set_xlabel('Similarity')
        axs[0].set_ylabel('Frequency')
        axs[0].set_title('GFP-GAN')
        axs[0].set_ylim(0, y_max)

        # Plotting the second histogram
        magnitude_values = data[f"{col}_gpen"].values
        axs[1].hist(magnitude_values, bins=50, color='mediumpurple', edgecolor='black')
        axs[1].set_xlabel('Similarity')
        axs[1].set_ylabel('Frequency')
        axs[1].set_title('GPEN')
        axs[1].set_ylim(0, y_max)

        magnitude_values = data[f"{col}_sgpn"].values
        axs[2].hist(magnitude_values, bins=50, color='mediumaquamarine', edgecolor='black')
        axs[2].set_xlabel('Similarity')
        axs[2].set_ylabel('Frequency')
        axs[2].set_title('SGPN')
        axs[2].set_ylim(0, y_max)

        # Adjust the spacing between subplots
        self.figure.subplots_adjust(wspace=0.2)

        # Draw the plot on the canvas
        self.canvas.draw()

class RegressionPlotWidget(QFrame):
    def __init__(self,fusiontype,rec_model,rest_model, parent=None):
        super(RegressionPlotWidget, self).__init__(parent)

        # Create a Figure objct and a FigureCanvas
        self.figure = Figure(figsize=(35, 5))
        self.canvas = FigureCanvas(self.figure)

        # Set the layout of the QFrame
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.fusiontype=fusiontype
        self.rec_model=rec_model
        self.rest_model=rest_model
        # Create your plot using the figure object

        self.plot(self.fusiontype,self.rec_model,self.rest_model)

    def init_elements(self,fusiontype,rec_model,rest_model):
        self.directory = pd.read_csv(
            rf"demo_app\data\files\{fusiontype}_coefficients.csv")
        #get column name in coefficient file
        col = f"{fusiontype[0]}f_{rest_model[0].lower()}_{rest_model[1].lower()}_{rec_model.lower()}"
        if not any(self.directory['name'].str.contains(col)):
            col = f"{fusiontype[0]}f_{rest_model[1].lower()}_{rest_model[0].lower()}_{rec_model.lower()}"
        #get the coefficients
        coeff = self.directory[self.directory['name'] == col].reset_index(drop=True)
        coeff = coeff.drop('name', axis=1)


        if fusiontype == "score":
            xqlfw = pd.read_csv(r"demo_app\data\files\xqlfw_scores.csv")
            col1 = f"{rec_model.lower()}_{rest_model[0].lower()}"
            col2 = f"{rec_model.lower()}_{rest_model[1].lower()}"
            # get the data
            data = pd.concat([xqlfw[col1], xqlfw[col2]], axis=1)
        else:
            print("hybrid fusion")
            xqlfw = pd.read_csv(r"demo_app\data\files\xqlfw_scores.csv")
            ff = pd.read_csv(r"demo_app\data\files\feature_fusion_scores.csv")
            if len(rest_model)==2:#if there are 2 models in feature level fusion
                col1 = f"ff_{rest_model[0].lower()}_{rest_model[1].lower()}_{rec_model.lower()}"
                if col1 not in ff.columns:
                    col1 = f"ff_{rest_model[1].lower()}_{rest_model[2].lower()}_{rec_model.lower()}"
                rest_l2= [element for element in ["GFPGAN", "SGPN", "GPEN"] if element not in rest_model]
                col2 = f"{rec_model.lower()}_{rest_l2[0].lower()}"
            else:#all
                col1=f"ff_all_{rec_model.lower()}"
                col2=f"{rec_model.lower()}_gfpgan"
            data = pd.concat([ff[col1], xqlfw[col2]], axis=1)
        return coeff,data
    def plot(self,fusiontype,rec_model,rest_model):
        self.figure.clear()
        # Set the width of the entire figure
        axs = self.figure.subplots(2, 5)
        coeff,data=self.init_elements(fusiontype,rec_model,rest_model)
        half=300
        column_values = np.concatenate((np.ones(half), np.zeros(half)))
        colors = ['#0F9DE8' if label == 1 else '#660099' for label in column_values]

        for i, ax in enumerate(axs.flatten()):
            _,test = cross_val(data,i)
            test['label'] = column_values
            columns = test.columns
            print(columns)
            x_col = columns[0]  # Assuming the first column is for the x-axis
            y_col = columns[1]
            print(x_col,y_col)
            test.plot.scatter(x=x_col, y=y_col, c=colors, ax=ax, label=None)
            ax.set_xlabel(f"{rest_model[0]} scores")
            ax.set_ylabel(f"{rest_model[1]} scores")
            ax.set_title(f'fold {i}')

            a = coeff.iloc[i, 0]
            b = coeff.iloc[i, 1]
            c = coeff.iloc[i, 2]

            s1_range = np.linspace(test[x_col].min(), test[y_col].max(), 100)

            # Calculate corresponding s2 values based on the line equation
            s2_range = (-c - a * s1_range) / b

            ax.plot(s1_range, s2_range, 'r', label='f(s1, s2)' if i == 0 else None)
            ax.legend()

            # Draw the plot on the canvas
            self.canvas.draw()
