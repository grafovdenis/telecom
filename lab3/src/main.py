import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.signal import lfilter


# x(t) = A * sin(2 * pi * w * t)
def filtered_sine_wave(amplitude=1, freq=20, show=False, save=False):
    fs = 1000  # sampling rate
    ts = 1 / fs  # sampling interval
    n = 2 ** 13  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector
    sig = amplitude * np.sin(2 * np.pi * freq * t)  # signal
    noise = np.random.normal(0, 0.5, n)
    sig_noised = sig + noise

    # Nyquist frequency
    nyq = fs / 2
    order = 4
    normal_cutoff = freq / nyq

    fnum, fdenom = signal.butter(order, normal_cutoff)
    sig_filtered = signal.filtfilt(fnum, fdenom, sig_noised)
    # sig_filtered = lfilter(fnum, fdenom, sig_noised)

    sig_noised_fft = np.fft.fft(sig_noised) / n * 2
    sig_filtered_fft = np.fft.fft(sig_filtered) / n * 2  # /N to scale due to python DFT equation,
    # *2 to make single sided
    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    print_time(t, sig_noised, sig_filtered, show, save)
    print_freq(fft_freq[:fs], abs(sig_noised_fft)[:fs], abs(sig_filtered_fft)[:fs], show, save)


def print_time(t, sig_noised, sig_filtered, show=False, save=False):
    plt.figure()
    plt.plot(t[:250], sig_noised[:250], label='Noised signal')
    plt.plot(t[:250], sig_filtered[:250], label='Filtered signal')
    plt.xlabel('time (S)')
    plt.ylabel('amplitude (V)')
    plt.legend()
    plt.grid(True)
    if save:
        plt.savefig('../out/sine_time.png')
    if show:
        plt.show()


def print_freq(fft_freq, sig_noised_fft, sig_filtered_fft, show=False, save=False):
    plt.figure()
    plt.plot(fft_freq, sig_noised_fft, label='Noised signal')
    plt.plot(fft_freq, sig_filtered_fft, label='Filtered signal')
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (V)')
    plt.legend()
    plt.grid(True)
    if save:
        plt.savefig('../out/sine_freq.png')
    if show:
        plt.show()


if __name__ == '__main__':
    filtered_sine_wave(show=True)
