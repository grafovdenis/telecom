import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import scipy.integrate as integrate


def sine_wave(amplitude=1, freq=10, show=False, save=False):
    fs = 2000  # sampling rate
    ts = 1 / fs  # sampling interval
    n = 2 ** 13  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector

    carrier_freq = 50
    carrier_amplitude = 1
    sig = np.sin(2 * np.pi * freq * t)
    phase_modulated = carrier_amplitude * np.sin(2 * np.pi * carrier_freq * t + amplitude * sig)

    sig_integrated = np.zeros_like(sig)
    for i, dt in enumerate(t):
        sig_integrated[i] = integrate.simps(sig, dx=t[i])

    freq_modulated = carrier_amplitude * np.sin(2 * np.pi * carrier_freq * t
                                                + amplitude * sig_integrated)

    analytic_signal = hilbert(phase_modulated)
    phase_function = np.unwrap(np.angle(analytic_signal) + np.pi / 2)

    phase_demodulated = phase_function - 2 * np.pi * carrier_freq * t

    freq_demodulated = phase_function - 2 * np.pi * carrier_freq * t

    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    phase_modulated_fft = \
        abs(np.fft.fft(phase_modulated)) / n * 2  # discrete Fourier Transform ( / n * 2 - normalization)
    phase_demodulated_fft = abs(np.fft.fft(phase_demodulated)) / n * 2

    freq_modulated_fft = \
        abs(np.fft.fft(freq_modulated)) / n * 2  # discrete Fourier Transform ( / n * 2 - normalization)
    freq_demodulated_fft = abs(np.fft.fft(freq_demodulated)) / n * 2

    draw_plot(t, (phase_modulated, phase_demodulated),
              ('PM modulated sine wave', 'PM demodulated sine wave'),
              'time (s)', 'amplitude (V)', show, save)
    draw_plot(fft_freq, (phase_modulated_fft, phase_demodulated_fft),
              ('PM modulated sine wave', 'PM demodulated sine wave'),
              'frequency (hz)', 'amplitude (V)', show, save)

    draw_plot(t[1:], (freq_modulated[1:], freq_demodulated[1:]),
              ('FM modulated sine wave', 'FM demodulated sine wave'),
              'time (s)', 'amplitude (V)', show, save)
    draw_plot(fft_freq[1:], (freq_modulated_fft[1:], freq_demodulated_fft[1:]),
              ('FM modulated sine wave', 'FM demodulated sine wave',),
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
