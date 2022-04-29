import math
from typing import List, Union, Any
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.gridspec as gridspec


# This function finds the center of mass of r-theta pairs
def com(theta_data, r_data):

    one_over_n = 1.0/theta_data.shape[0]
    x_avg = one_over_n * np.dot(r_data, np.cos(theta_data))
    y_avg = one_over_n * np.dot(r_data, np.sin(theta_data))

    return ([math.atan2(y_avg, x_avg)], [math.sqrt(x_avg**2 + y_avg**2)])

    
class FourierAnalyzer:
    SCALAR_ARRAY_1D = Union[
        List[float],
        np.ndarray[Any, np.dtype[+np.ScalarType]]
        ]
    def __init__(self,
            x_data: SCALAR_ARRAY_1D =None,
            y_data: SCALAR_ARRAY_1D =None,
            min_winding=0.0,
            max_winding=1.0):

        # validate inputs
        if not isinstance(y_data, np.ndarray):
            y_data = np.array(y_data)
        if x_data is None:
            x_data = np.arange(y_data.shape[0])
        self.y_data = y_data
        self.x_data = x_data
        # Define initial winding number
        w_init = 0.5*(min_winding + max_winding)

        # Domain of winding numbers to be considered
        w = np.linspace(min_winding, max_winding, 5000)
        # The domain after having the winding number applied
        wound_x = w_init*x_data
        # The range for the frequency transform
        fourier_data = np.array([com(wn*x_data, y_data)[1][0] for wn in w])

        # Create the figure
        self.fig = plt.figure()
        gspecs = gridspec.GridSpec(3, 1, height_ratios=[1, 3, 1], hspace=0.4)
        ax_inputs = plt.subplot(gspecs[0])
        ax_winding = plt.subplot(gspecs[1], projection='polar')
        self.ax_freq_transform = plt.subplot(gspecs[2])

        # Plot of the function being analyzed
        ax_inputs.plot(x_data, y_data)
        # Plot the wound-up function and the center of mass
        self.plt_winding, = ax_winding.plot(wound_x, y_data)
        c_o_m = com(wound_x, y_data)
        self.plt_com, = ax_winding.plot(c_o_m[0], c_o_m[1], marker="o",
            markersize=10, markeredgecolor="red", markerfacecolor="red")
        # Plot frequency transform and current winding number line
        self.ax_freq_transform.plot(w, fourier_data)
        self.vline = self.ax_freq_transform.axvline(x=w_init, color='r')

        # Some cosmetic changes
        ax_winding.grid(True)
        ax_inputs.set_title('Original Function')
        ax_winding.set_title('Wound-up Function')
        self.ax_freq_transform.set_title('Frequency Transform')
        ax_inputs.set_yticks([])
        ax_winding.set_rticks([])
        self.ax_freq_transform.set_yticks([])
        self.fig.canvas.manager.window.geometry('+0+0')
        self.fig.set_size_inches(11, 8)
        self.fig.canvas.manager.set_window_title('Wind up a Function!')

        # adjust the main plot to make room for the slider
        plt.subplots_adjust(bottom=.08, top=.97, left=0.01, right=.99)

        # Slider to control the winding number
        ax_sld_wind = plt.axes([0.13, 0.01, 0.74, 0.03])
        self.sld_wind = Slider(
            ax=ax_sld_wind,
            label='Winding Number',
            valmin=min_winding,
            valmax=max_winding,
            valinit=w_init,
        )

        # register the update function with the slider
        self.sld_wind.on_changed(self.update())

        # Create a button to reset the sliders to initial values.
        axBtnReset = plt.axes([0.93, 0.01, 0.06, 0.04])
        btnReset = Button(axBtnReset, 'Reset', hovercolor='0.975')

        # Register button callback
        btnReset.on_clicked(lambda event: self.sld_wind.reset())

        plt.show()

    # The function to be called anytime a slider's value changes
    def update(self):
        def _update(winding_num):
            wound_x = winding_num*self.x_data
            self.plt_winding.set_xdata(wound_x)
            c_o_m = com(wound_x, self.y_data)
            self.plt_com.set_xdata(c_o_m[0])
            self.plt_com.set_ydata(c_o_m[1])
            self.vline.remove()
            self.vline = self.ax_freq_transform.axvline(
                x=winding_num, color='r')
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        return _update


def demo_data():
    x = np.linspace(0, 50, 10000)
    return (
        x,
        (
            (np.sin(5.0*x) + 1) +
            (np.sin(6.8*x) + 1) +
            (np.sin(9.0*x) + 1) +
            (np.sin(10.0*x) + 1)  # +
            # (2.0*np.random.rand(x.shape[0]))
        )
    )


if __name__ == '__main__':
    x,y = demo_data()
    FourierAnalyzer(
        x_data=x,
        y_data=y,
        min_winding=4.0,
        max_winding=11.0,
    )
