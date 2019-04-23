import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, hilbert


def sine_wave(amplitude=1, freq=10, show=False, save=False):
    fs = 2000  # sampling rate
    ts = 1 / fs  # sampling interval
    n = 2 ** 13  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector

    carrier_freq = 100
    carrier_amplitude = 1
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    sig = np.sin(2 * np.pi * freq * t)
    m = amplitude / carrier_amplitude
    singleton_modulated = (1 + m * amplitude * sig) * carrier_amplitude * carrier
    suppressed_carried_mod = amplitude * carrier_amplitude * sig * carrier
    single_sideband_mod = hilbert(sig) * np.cos(2 * np.pi * carrier_freq * t) - hilbert(sig) * carrier

    order = 5
    normal_cutoff = freq / carrier_freq

    fnum, fdenom = butter(order, normal_cutoff)
    singleton_demodulated = filtfilt(fnum, fdenom, abs(singleton_modulated))
    suppressed_carried_demod = suppressed_carried_mod * carrier_amplitude * carrier

    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    singleton_modulated_fft = \
        abs(np.fft.fft(singleton_modulated)) / n * 2  # discrete Fourier Transform ( / n * 2 - normalization)
    singleton_demodulated_fft = abs(np.fft.fft(singleton_demodulated)) / n * 2

    suppressed_carried_mod_fft = abs(np.fft.fft(suppressed_carried_mod)) / n * 2
    suppressed_carried_demod_fft = abs(np.fft.fft(suppressed_carried_demod)) / n * 2

    single_sideband_mod_fft = abs(np.fft.fft(single_sideband_mod)) / n * 2

    draw_plot(t, (singleton_modulated, singleton_demodulated),
              ('Singleton Modulated sine wave', 'Singleton Demodulated sine wave'),
              'time (s)', 'amplitude (V)', show, save)
    draw_plot(fft_freq[1:], (singleton_modulated_fft[1:], singleton_demodulated_fft[1:]),
              ('Singleton Modulated sine wave', 'Singleton Demodulated sine wave'),
              'frequency (hz)', 'amplitude (V)', show, save)

    draw_plot(t, (suppressed_carried_mod, suppressed_carried_demod),
              ('Suppressed carrier Modulated sine wave', 'Suppressed carrier Demodulated sine wave'),
              'time (s)', 'amplitude (V)', show, save)
    draw_plot(fft_freq, (suppressed_carried_mod_fft, suppressed_carried_demod_fft),
              ('Suppressed carrier Modulated sine wave', 'Suppressed carrier Demodulated sine wave'),
              'frequency (hz)', 'amplitude (V)', show, save)

    draw_plot(t, (single_sideband_mod,),
              ('Single sideband Modulated sine wave',),
              'time (s)', 'amplitude (V)', show, save)
    draw_plot(fft_freq, (single_sideband_mod_fft,),
              ('Single sideband carrier Modulated sine wave',),
              'frequency (hz)', 'amplitude (V)', show, save)


def draw_plot(x, y, labels, xlabel, ylabel, show=False, save=False):
    size = 500
    plt.figure()
    for i in range(0, len(y)):
        plt.plot(x[:size], y[i][:size], label=labels[i])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    if save:
        plt.savefig('../out/' + labels[0].split(' ')[0] + '_' + xlabel.split(' ')[0] + '.png')
    if show:
        plt.show()


if __name__ == '__main__':
    pic = 0
    sine_wave(show=True, save=True)
