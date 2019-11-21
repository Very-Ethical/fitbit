# Fitbit Data Analysis

***Purpose:*** 

Find the correct labels, determine which is "extra," predict the missing two weeks, reproducibly tidy the data, and summarize the data.

  
***How to use:***
  First, download or clone this repository by clicking the "Clone or download" button in the top-right of your screen.

  If you have untidy fitbit data, delete all the .csvs currently in the fitbit directory.

  Then, place all the .csv files in that same fitbit directory inside of the downloaded repository.

  From the terminal while in the repository, type "python acquire.py"

  To see the results of the analysis, open the Jupyter Notebook titled "fitbit_project.ipynb."

  From there, click Kernel -> Restart & Run All.

  Please note this process has only been tested on MacOS and is highly unlikely to work as described on Windows computers.

  It is also highly unlikely to produce meaningful results given notably different datasets, since we hard-coded many elements of the model such as, but not limited to:

    - the duration of the data collection
    - what values would be considered outliers for this person
    - the weight columns assume the subject to be a male who is six-feet tall

***Dependencies:***

    - jupyter notebook
    - python 3
    - pandas
    - seaborn
    - matplotlib
    - fbprophet

***Deliverables:***

    - A Jupyter notebook containing analysis of fit bit data
    - A tidied dataset 
    - A summary of the data including insights drawn from the data as well as any conclusions that can be drawn about the wearer of the device
    - A two slide presentation of our findings (+ title slide)