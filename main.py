import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = None  # Initialize the DataFrame variable

def create_window():
    win = Tk()
    win.geometry("900x600")
    win.title('School Performace Assessment System')
    return win

def upload_file():
    global df
    win = create_window()
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        print("Selected File:", file_path)
        create_and_display_charts(win)

def create_and_display_charts(win):
    if df is not None:
        # First Matplotlib figure - Pie Chart
        plt.figure(figsize=(5, 5))
        labels = ['Female', 'Male']
        plt.pie(df['gender'].value_counts(), labels=labels, explode=[0.1, 0.1],
                autopct='%1.2f%%', colors=['#E37383', '#FFC0CB'], startangle=90)
        plt.title('Gender')

        # Embed the first figure in the Tkinter window
        canvas1 = FigureCanvasTkAgg(plt.gcf(), master=win)
        canvas1.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)

        # Second Matplotlib figure - Grouped Bar Chart
        plt.figure(figsize=(5, 5))
        grouped_data = df.groupby(['year', 'gender'])['performance'].mean().unstack()
        grouped_data.plot(kind='bar', color=['blue', 'pink'])
        plt.title('Performance by Year and Gender')
        plt.xlabel('Year')
        plt.ylabel('Average Performance')

        # Embed the second figure in the Tkinter window
        canvas2 = FigureCanvasTkAgg(plt.gcf(), master=win)
        canvas2.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)

        # Third Matplotlib figure - Bar Chart
        plt.figure(figsize=(5, 5))
        grouped_data = df.groupby(['year'])['performance'].mean()
        grouped_data.plot(kind='bar', color='skyblue')
        plt.title('Performance by Year')
        plt.xlabel('Year')
        plt.ylabel('Average Performance')

        # Embed the third figure in the Tkinter window
        canvas3 = FigureCanvasTkAgg(plt.gcf(), master=win)
        canvas3.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)

# Create the initial Tkinter window
main_win = create_window()

upload_button = Button(main_win, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

# Create a frame for the Matplotlib figures
frame = Frame(main_win)
frame.pack(side=TOP, fill=BOTH, expand=1)

# Start the Tkinter main loop
main_win.mainloop()
