import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import colors
from scipy.interpolate import Rbf
import Predictor
import Printer


class Interpolator(object):

    def __init__(self, resolution_scale=1):
        """
        Constructor method for the interpolator class
        :param resolution_scale: number, representing the fraction of interpolation resolution:
        1 = 1600x950,
        0.5 = 800x475,
        etc.
        """
        self.imshape_scaled = (int(1600*resolution_scale), int(950*resolution_scale))
        self.imshape_original = (1600, 950)

        self.xs = (pd.read_csv('Data/behavior_zones.csv')['interp_X'].values*resolution_scale).astype('int')
        self.ys = (pd.read_csv('Data/behavior_zones.csv')['interp_Y'].values*resolution_scale).astype('int')

        self.max = 2500

        self.overlay = Image.open("Data/overlay.png").resize(self.imshape_original, Image.ANTIALIAS)

        colours = [
            (180/255, 180/255, 180/255),
            (80/255, 80/255, 180/255),
            (80/255, 180/255, 80/255),
            (180/255, 180/255, 80/255),
            (180/255, 50/255, 50/255),
            (150/255, 0/255, 180/255)
        ]

        self.colour_map = colors.LinearSegmentedColormap.from_list('pedestrians', colours, N=11)

    def interpolate_predict(self, datetime, filename='interpolation'):
        """
        Predicts counts for the given date and time and interpolates the predictions onto a map.
        Saves the interpolated image to Images/Interpolation.png
        :param filename: name of the image file to be saved
        :param datetime: String defining the date for the prediction
        """
        predictions = Predictor.Predictor().predict_timeframe(datetime, datetime)
        ids = Predictor.get_prediction_ids(predictions)

        zs = predictions.values[:, ids[1]].flatten().astype('int')

        self.interpolate_data(zs, filename)

    def interpolate_data(self, data, filename='interpolation'):
        """
        Interpolates the given location counts onto a map.
        Saves the interpolated image to Images/Interpolation.png
        :param filename: name of the image file to be saved
        :param data: array with length 42, which represents the counts for each location (from the location dataframe).
        For more info on the locations, call the Predictor.dump_names() method.
        """

        zs = data.flatten()

        rbf = Rbf(self.xs, self.ys, zs, epsilon=3, smooth=5)

        data_map = np.ndarray((self.imshape_scaled[1], self.imshape_scaled[0]))
        total_count = data_map.shape[0] * data_map.shape[1]
        current_count = 0
        print("Building the interpolated map...")
        for x in range(data_map.shape[0]):
            for y in range(data_map.shape[1]):
                data_map[x, y] = rbf(x, y)
                current_count += 1

            Printer.loading_bar(int((current_count + 1) / (total_count / 100)))

        data_map -= np.min(data_map) - 1
        data_map_im = data_map / self.max
        data_image = Image.fromarray(np.uint8(self.colour_map(data_map_im) * 255))
        data_image = data_image.resize(self.imshape_original, Image.ANTIALIAS)
        data_image = Image.alpha_composite(data_image, self.overlay)

        data_image.save('Images/'+str(filename)+'.png', "PNG")
