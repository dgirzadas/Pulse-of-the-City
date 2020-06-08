# Pulse of the City
A pedestrian traffic prediction and spatial interpolation project for the City Council of Nijmegen.

This project is the result of a Bachelor's thesis project.

Made by: __Domantas Giržadas__

## Description

This project contains two modules - pedestrian traffic prediction and spatial interpolation (+ visualisation) modules:

### 1. **Pedestrian traffic prediction module**
This module is capable of predicting the number of pedestrians for a certain date and time in any of the 42 available locations around the downtown area of Nijmegen, Netherlands.

*(image with the locations shown on a map)*

The predictions are based on an averaging approach - a prediction for a certain date-time is an average count for that day of the week and hour (e.g. Wednesday, 14:00). This value is then scaled, based on an estimated yearly trend and expanded by a confidence interval. This approach has been found to perform better than machine learning-based models (i.e. Support Vector Regression, Multi-Layer Perceptron or Gaussian Process Regression) with the following performance scores:

- **Mean Absolute Error** (Predictions only) = 45.086
- **Mean Absolute Error** (True value within confidence interval -> Zero error) = 25.02
- **R<sup>2</sup>** = 0.726

This module can be used for any application, related to pedestrian count forecasting or comparison. An example graph of the predictions can be seen below.

*(image with the example prediction graphs)*

### 2. Spatial interpolation (+ visualisation) module

This module is capable of generating interpolated estimations between the 42 locations. By using this module, predictions and observations are not limited to the 42 locations, but are interpolated within a large part of the downtown area of Nijmegen.

An example interpolated prediction map can be seen below.

*(image with the interpolated map)*

# Installation

In order to run this project, clone this repository into your local machine:

```
git clone https://github.com/dgirzadas/Pulse-of-the-City.git
```

And you are basically good to go!

To see examples of how to use this system, check out [the demo Jupyter notebook](Demo.ipynb).

# License
This project is published under the [MIT license](LICENSE).

# Acknowledgements
I would like to thank my supervisors, who guided me through the development of this system:

**Internal supervisor** (Radboud University, Department of Artificial Intelligence):

*Pim Haselager, PhD*

**External supervisors** (Municipality of Nijmegen):

*Mariska Baartman*

*Sjoerd Dikkerboom, MSc*

*Paul Geurts, B*

*Jasper Meekes, MSc*

*Arjen Verhulst, BA*
