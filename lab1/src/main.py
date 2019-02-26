import matplotlib.pyplot as plt
import numpy as np


# x(t) = A * sin(w*t + fi_0)
def sine_wave(show=False):
    freq = 20  # frequency of the signal
    ts = 1 / 250  # sampling interval
    # freq & Ts are selected for coherent sampling
    n = 8192  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector
    sig = np.cos(2 * np.pi * freq * t)  # signal
    sig_fft = np.fft.fft(sig) / n * 2  # /N to scale due to python DFT equation,
    # *2 to make single sided
    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    plt.figure()
    plt.plot(t[0:100], sig[0:100])
    plt.xlabel('time (S)')
    plt.ylabel('amplitude (V)')
    plt.grid(True)
    if show:
        plt.show()

    plt.figure()
    plt.plot(fft_freq[:n // 2], 20 * np.log10(abs((sig_fft[:n // 2]))))
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (dB20(V))')
    plt.grid(True)
    if show:
        plt.show()


# x(t) = sign(sin(t))
def square_wave(show=False):
    freq = 20  # frequency of the signal
    ts = 1 / 250  # sampling interval
    # freq & Ts are selected for coherent sampling
    n = 8192  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector
    sig = np.sign(np.cos(2 * np.pi * freq * t))  # signal
    sig_fft = np.fft.fft(sig) / n * 2  # /N to scale due to python DFT equation,
    # *2 to make single sided
    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    plt.figure()
    plt.plot(t[0:100], sig[0:100])
    plt.xlabel('time (S)')
    plt.ylabel('amplitude (V)')
    plt.grid(True)
    if show:
        plt.show()

    plt.figure()
    plt.plot(fft_freq[:n // 2], 20 * np.log10(abs((sig_fft[:n // 2]))))
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (dB20(V))')
    plt.grid(True)
    if show:
        plt.show()


if __name__ == '__main__':
    sine_wave(show=True)
    square_wave(show=True)
