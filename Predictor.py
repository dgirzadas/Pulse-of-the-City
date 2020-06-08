import numpy as np
import pandas as pd
import datetime as dt
import pickle
import re
import Printer


def get_prediction_ids(dataframe):
    """
    Gives the matrix of ids for columns that contain the predictions [<low_ids>, <mid_ids>, <high_ids>]
    :param dataframe: prediction dataframe from the predict_timeframe function.
    :return: numpy array of indices for specific prediction columns
    """
    return np.array([
            np.arange(1, dataframe.shape[1], 3),
            np.arange(2, dataframe.shape[1], 3),
            np.arange(3, dataframe.shape[1], 3),
        ])


def dump_names():
    """
    Prints the list of location names and their IDs for predictions.
    """
    print(pd.read_csv('Data/behavior_zones.csv')['Name'])


class Predictor(object):

    def __init__(self):
        """
        Constructor method for the predictor class.
        Initialises the prediction models, scaling factors and the location list
        """
        self.models = []

        self.avg_preds = np.load('Models/average_predictions.npy')

        self.daily_scales = pd.read_csv('Data/daily_scales.csv').set_index('Date')
        self.conf_stds = np.load('Data/conf_stds.npy')
        self.location_names = pd.read_csv('Data/behavior_zones.csv')['Name']

    def predict_timeframe(self, start_time, end_time, request_ids=None, ci=True):
        """
        Generates a dataframe of hourly predictions for the given location IDs within the requested timeframe.
        :param ci: Boolean parameter, defining if the user wants the confidence interval included in the prediction.
        :param request_ids: list of location IDs for prediction
        :param start_time: String of the starting date
        :param end_time: String of the ending date
        :return: dataframe with hourly predictions for each location
        """
        print("Generating predictions...")
        if request_ids is None:
            request_ids = range(self.avg_preds.shape[0])

        requests = self.__generate_pred_requests(start_time, end_time)
        data = pd.DataFrame()

        for i, request in enumerate(requests):
            Printer.loading_bar(int((i+1)/(len(requests)/100)))

            prediction = self.predict(request[0], request[1], request[2], request[3], locations=request_ids, ci=ci)
            data = data.append(prediction)

        return data

    def predict(self, year, month, day, hour, locations, ci):
        """
        Returns an estimated pedestrian count for a given date and hour
        :param ci: Boolean parameter, defining if the user wants the confidence interval included in the prediction.
        :param year: year for prediction
        :param locations: list of location indices, if not passsed, all locations are returned
        :param month: month for prediction
        :param day: day for prediction
        :param hour: hour for prediction. 0 means 00:00 - 01:00, etc.
        :return: dataframe of predicted pedestrian numbers for each location
        """
        try:
            predict_date = dt.date(year, month, day)

            scale_factor = self.daily_scales.loc[str(month) + '-' + str(day)]['Scale']

            predictions = pd.DataFrame()
            predictions['Datetime'] = [str(dt.datetime(year, month, day, hour))]
            for i, location_id in enumerate(locations):
                pred = int(self.avg_preds[location_id, predict_date.weekday(), hour])
                if ci:
                    predictions[str(self.location_names[location_id]) + '_low'] = int(
                        np.max([(pred - self.conf_stds[location_id, predict_date.weekday(), hour]) * scale_factor, 0]))
                    predictions[str(self.location_names[location_id]) + '_mid'] = int(np.max([pred * scale_factor, 0]))
                    predictions[str(self.location_names[location_id]) + '_high'] = int(
                        np.max([(pred + self.conf_stds[location_id, predict_date.weekday(), hour]) * scale_factor, 0]))
                else:
                    predictions[str(self.location_names[location_id])] = int(np.max([pred * scale_factor, 0]))

            return predictions
        except IndexError:
            raise IndexError("\nInvalid location index")
        except KeyError:
            raise IndexError("\nInvalid location index")


    def __generate_pred_requests(self, start_time, end_time):
        """
        Generates a list containing required information for the prediction model.
        :param start_time:
        :param end_time:
        :return:
        """
        requests = []
        year_start, month_start, day_start, hour_start = self.__parse_date(start_time)
        year_end, month_end, day_end, hour_end = self.__parse_date(end_time)

        start_date = dt.datetime(year_start, month_start, day_start, hour_start)
        self.startDate = dt.date(start_date.year, 1, 1)
        end_date = dt.datetime(year_end, month_end, day_end, hour_end)

        date = start_date
        if start_time == end_time:
            requests.append([date.year, date.month, date.day, date.hour])
            return requests
        else:
            while date < end_date:
                requests.append([date.year, date.month, date.day, date.hour])
                date += dt.timedelta(1 / 24)

            return requests

    @staticmethod
    def __parse_date(date):
        """
        Parses the date from the received string
        :param date: string, containing the date and time
        :return: integers, representing the year, month, day and hour of the string
        """
        try:
            m = re.match(r'(.*)-(.*)-(.*)T(.*):(.*):(.*)', date)
            return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        except Exception:
            raise Exception("\nDate parsing error: \nMake sure the date is in format '<year>-<month>-<day>T<hours>:<minutes>:<seconds>'")
