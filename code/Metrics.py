import numpy as np
from tqdm import tqdm

class Metrics:
    """Class with functions to get all the different metrics we need
    """

    def __roundClosest(a, b):
        """Round a to the closest multiple of b
        """

        return b * round(a/b)

    def avg_speed(car_data: list):
        """Calculate average speed for each time step

        Args:
            carData: list with cars for each time step (generated by the simulation)

        Returns: list with average speed for each time step
        """

        avg_list = []
        for data_t in car_data:
            speed_array = np.array([car['v'] * 3.6 for car in data_t])
            avg_list.append(np.average(speed_array))
        return avg_list

    def median_speed(carData: list):
        """Calculate median speed for each time step

        Args:
            carData: list with cars for each time step (generated by the simulation)

        Returns: list with median speed for each time step
        """

        median_list = []
        for data_t in carData:
            speed_array = np.median([car['v'] * 3.6 for car in data_t])
            median_list.append(np.average(speed_array))
        return median_list


    def make_dots(car_data: list, road_length: int, time_div: float, delta_x: float, colors: list):

        """Make car dot plot

        Args:
            carData: list with cars for each time step (generated by the simulation)
            roadLength: length of the road in the simulation
            time_div: time resampling factor of the data points (use 1 every i-th datapoint)
            delta_x: minimum change in distance (how much distance a pixel represents)
        """

        black = (0, 0, 0)
        red = (0, 0, 0)
        white = (255, 255, 255)
        blue = (0, 0, 0)

        print("Generating graph...")
        pixel_plot = np.full((len(car_data[::time_div]), round(road_length/delta_x), 3), (255., 255., 255.))
        for i, data_t in enumerate(tqdm(car_data[::time_div])):
            for car in data_t:
                x = int(np.floor(car['pos'][0]/delta_x))
                if x >= pixel_plot.shape[1]:  continue
                pixel_plot[i][x] *= colors[int(car['pos'][1]/5)]
                pixel_plot[i][x] = pixel_plot[i][x] * (255 / max(0.00001, pixel_plot[i][x].max()))

        return pixel_plot

    def make_dots_bw(car_data: list, road_length: int, time_div: float, delta_x: float):

        """Make car dot plot

        Args:
            carData: list with cars for each time step (generated by the simulation)
            roadLength: length of the road in the simulation
            time_div: time resampling factor of the data points (use 1 every i-th datapoint)
            delta_x: minimum change in distance (how much distance a pixel represents)
        """

        print("Generating graph...")
        pixel_plot = np.full((len(car_data[::time_div]), round(road_length/delta_x)), (255.))
        for i, data_t in enumerate(tqdm(car_data[::time_div])):
            for car in data_t:
                x = int(np.floor(car['pos'][0]/delta_x))
                if x >= pixel_plot.shape[1]:  continue
                pixel_plot[i][x] -= 255./2
                pixel_plot[i][x] = max(pixel_plot[i][x], 0)

        return pixel_plot

    def plot_bins(bins, data, filename):
        import matplotlib.pyplot as plt
        plot_data = np.array(data)
        plot_data = np.resize(plot_data, int(np.floor(plot_data.size/bins) * bins))
        plot_data = plot_data.reshape(-1, int(plot_data.size/bins))
        plot_data = np.mean(plot_data, axis=1)
        plt.bar(range(bins), plot_data)
        plt.ylim(0, 160)
        plt.savefig(filename)
        plt.close()

    def plot_bar_groupped(data, filename, type_labels, xlabels=None, margin=0.2):
        import matplotlib.pyplot as plt

        width = (1 - margin) / data.shape[0]

        for i, d in enumerate(data):
            print(d)
            plt.bar([x + i*width for x in range(data.shape[1])], d, width=width, label=type_labels[i])

        plt.xticks([x + ((width * data.shape[0])/2) - width/2 for x in range(data.shape[1])], xlabels)
        plt.legend()
        plt.savefig(filename)
        plt.close()

    def show_dots(pixel_plot):
        import matplotlib.pyplot as plt
        plt.imshow(pixel_plot, cmap='gray')
        plt.show()
