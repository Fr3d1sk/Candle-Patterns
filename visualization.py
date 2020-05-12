import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Candlestick_patterns import Doji, Hammer, ShootingStar, GravestoneDoji, HangingMan
import math


def plot_multiple_data(x_values, y_values, titles, n_rows, n_cols, save=False,
                       filename="image", save_path="data/pictures/"):
    number_of_plots = len(x_values)
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(10.0, 10.0))
    plt.subplots_adjust(hspace=0.3, bottom=0.3)
    pointer_row = 0
    pointer_col = 0
    pointer_data = 0

    while pointer_col < n_cols:
        pointer_row = 0

        while pointer_row < n_rows:
            axs[pointer_row, pointer_col].plot(x_values[pointer_data], y_values[pointer_data])
            axs[pointer_row, pointer_col].set_title(titles[pointer_data])
            pointer_row += 1
            pointer_data += 1

        pointer_col += 1
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    if save:
        plt.savefig(save_path + filename + ".png", transparent=True)

    plt.show()

def check_data(timeframes, patterns, forward_length=5, trend_length=10, min_price_change=0.01,
               candle_type="all", image_name="image"):

    success_rate_over_time = []
    titles = []
    occurrences = []

    for time in timeframes:
        for pattern in patterns:

            candles_trend = []
            df = pd.read_csv(f"data/raw_history/crypto/BTCUSDT-{time}-data.csv")

            for index, row in df.iterrows():

                # checking if the candle is green or red for the trend
                if row["open"] >= row["close"]:
                    candles_trend.append(1)
                else:
                    candles_trend.append(0)

                # deleting last entry of the trend-history
                if len(candles_trend) >= trend_length:
                    candles_trend.pop(0)

                # checking if candlepattern should be called
                if index >= 1 and index + forward_length + 1 <= len(df):
                    if last_high != last_low:
                        trend = np.mean(candles_trend)
                        pattern.append(last_open, last_high, last_low, last_close, trend, df.iloc[index + forward_length]["close"],
                                       0.01)

                # writing current prices for the next iteration
                last_open = row["open"]
                last_high = row["high"]
                last_close = row["close"]
                last_low = row["low"]
                trend = 0

                # just to see that it still does something :p
                # if index % 100:
                #     print(f"{pattern.name}: {index}/{len(df)}")

            # calculating average of accuracy (of 3% of the data)
            avg_acc = []
            len_avg = math.ceil(len(pattern.acc_over_time_all) / 33)

            for a in range(len(pattern.acc_over_time_all)):

                if candle_type == "all":
                    avg_acc.append(np.mean(pattern.acc_over_time_all[max(a - len_avg, 0):a + 1]))
                elif candle_type == "red":
                    avg_acc.append(np.mean(pattern.acc_over_time_red[max(a - len_avg, 0):a + 1]))
                else:
                    avg_acc.append(np.mean(pattern.acc_over_time_green[max(a - len_avg, 0):a + 1]))

            # now append the success over time to a list which will be fed into a graph at the end
            if candle_type == "all":
                titles.append(f"{time}-{pattern.name}-{round(pattern.acc_all * 100, 1)}%")
            elif candle_type == "red":
                titles.append(f"{time}-{pattern.name}-{round(pattern.acc_red * 100, 1)}%")
            else:
                titles.append(f"{time}-{pattern.name}-{round(pattern.acc_green * 100, 1)}%")

            success_rate_over_time.append(avg_acc)
            occurrences.append(np.arange(1, len(avg_acc) + 1))

            # resetting the object for the next timeframe
            pattern.reset()

    plot_multiple_data(occurrences, success_rate_over_time, titles, 5, 3, filename=image_name, save=True)

if __name__ == "__main__":

    timeframes = [
        "1h",
        "4h"
    ]

    patterns = [
        ShootingStar(),
        Hammer(),
        Doji(),
        GravestoneDoji(),
        HangingMan()
    ]


    success_rate_over_time = []
    titles = []
    occurrences = []

    for time in timeframes:
        for pattern in patterns:

            candles_trend = []
            df = pd.read_csv(f"data/raw_history/crypto/BTCUSDT-{time}-data.csv")

            for index, row in df.iterrows():

                # checking if the candle is green or red for the trend
                if row["open"] >= row["close"]:
                    candles_trend.append(1)
                else:
                    candles_trend.append(0)

                # deleting last entry of the trend-history
                if len(candles_trend) >= 10:
                    candles_trend.pop(0)

                # checking if candlepattern should be called
                if index >= 1 and index + 6 <= len(df):
                    if last_high != last_low:

                        trend = np.mean(candles_trend)
                        pattern.append(last_open, last_high, last_low, last_close, trend, df.iloc[index + 5]["close"], 0.01)

                # writing current prices for the next iteration
                last_open = row["open"]
                last_high = row["high"]
                last_close = row["close"]
                last_low = row["low"]
                trend = 0

                # just to see that it still does something :p
                if index % 100:
                    print(f"{pattern.name}: {index}/{len(df)}")


            # calculating average of accuracy (of 3% of the data)
            avg_acc = []
            len_avg = math.ceil(len(pattern.acc_over_time_all) / 33)

            for a in range(len(pattern.acc_over_time_all)):
                avg_acc.append(np.mean(pattern.acc_over_time_all[max(a-len_avg, 0):a+1]))

            # now append the success over time to a list which will be fed into a graph at the end
            titles.append(f"{time}-{pattern.name}-{round(pattern.acc_all * 100, 1)}%")
            success_rate_over_time.append(avg_acc)
            occurrences.append(np.arange(1, len(avg_acc)+1))

            # resetting the object for the next timeframe
            pattern.reset()

    plot_multiple_data(occurrences, success_rate_over_time, titles, 5, 2, save=True)








