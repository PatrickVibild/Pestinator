# Installation guide

To install and run the Pestinator simulation you shall follow the next steps. 

## Downloading the simulator
There are two options available: The first is to download the zip file containing the whole project found at https://github.com/PatrickVibild/Pestinator and unzip the content in the machine. Alternatively, git can be used to clone the repository with the command (Open the terminal with windows button + R or crtl + alt T if in linux distribution): 

```
git clone https://github.com/PatrickVibild/Pestinator
```

## Installing the dependencies

To run the simulation successfully, there are some packages that need to be installed. Since it is based on the pygame engine, a python version shall be installed:

Python version: python3.8.3 or later

The releases and versions can be found and installed following the instructions in https://www.python.org/downloads/

After the python version is installed, the rest of the dependencies can be installed with pip.

If pip is not installed yet on a Windows machine, first download the script https://bootstrap.pypa.io/get-pip.py , move to the file location and then run:

```
python get-pip.py
```

If the machine is running Ubuntu, then in a terminal window run:

```
sudo apt-get install python3-pip

pip install --upgrade pip
```

Make sure that the correct version of python is being used and then proceed to install the rest of the dependencies:

```
pip3 install pygame
pip3 install numpy
pip3 install matplotlib
```

All the required software is now installed in the machine.

## Configuring the simulation 

In the file ``` parameters.py``` there are defined a set of parameters of the simulation. By editing this file the number of drones, thresholds, capacities and strategies of different agents may be changed. The scanning routines possibilities are: "random", "brute_force" and "fast_brute_force". Remember to save the changes before running the simulation. 

## Usage 

To start the simulation run the ```main.py``` script(on the file location):

```
python3 main.py
```
A window will pop up in black for a few seconds, where the field is being generated and all modules are being initialized. Then it will be displayed the field with the selected drones starting the routine. Click inside the window and press "1" to speed up the simulation time and "2" to slow it down. The margins of the field indicate the time of the day, where white margins mean day, black means night and blue means that the wind is higher than the threshold.

Leave the simulation running as much as desired and then kill the process with ``` ctrl + C``` or kill all python threads. If the simulation has lasted for more than two weeks, there will be 5 new images in the folder corresponding to the graphs of the simulation as can be seen in the report.

### Disclaimer

For the data plots to work it may be necessary to run the simulator on a Linux (Ubuntu) distribution. Otherwise, if the simulation is not working properly it may be required to comment the lines 26 and 27 in the ```main.py``` file:

```
data = Data_visualizer(interval)
data.run()
```
Then, the plots wont be generated.

For more insights of what is happening in the simulation, look at the terminal prompt where the file was launched.