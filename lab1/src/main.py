import matplotlib.pyplot as plt
import numpy as np


# x(t) = A * sin(w*t + fi_0)
def sine_wave(freq=20, show=False, save=False):
    fs = 1000  # sampling rate
    ts = 1 / fs  # sampling interval
    n = 8192  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector
    sig = np.cos(2 * np.pi * freq * t)  # signal
    sig_fft = np.fft.fft(sig) / n * 2  # /N to scale due to python DFT equation,
    # *2 to make single sided
    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    plt.figure()
    plt.plot(t[0:250], sig[0:250])
    plt.xlabel('time (S)')
    plt.ylabel('amplitude (V)')
    plt.grid(True)
    if save:
        plt.savefig('../out/sine_time.png')
    if show:
        plt.show()

    plt.figure()
    plt.plot(fft_freq[:fs], abs(sig_fft)[:fs])
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (V)')
    # plt.plot(fft_freq[:n // 2], 20 * np.log10(abs((sig_fft[:n // 2]))))
    # plt.ylabel('amplitude (dB20(V))')
    plt.grid(True)
    if save:
        plt.savefig('../out/sine_freq.png')
    if show:
        plt.show()


# x(t) = sign(sin(t))
def square_wave(freq=20, show=False, save=False):
    fs = 1000  # sampling rate
    ts = 1 / fs  # sampling interval
    n = 8192  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector
    sig = np.sign(np.cos(2 * np.pi * freq * t))  # signal
    sig_fft = np.fft.fft(sig) / n * 2  # /N to scale due to python DFT equation,
    # *2 to make single sided
    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    plt.figure()
    plt.plot(t[0:250], sig[0:250])
    plt.xlabel('time (S)')
    plt.ylabel('amplitude (V)')
    plt.grid(True)
    if save:
        plt.savefig('../out/square_time.png')
    if show:
        plt.show()

    plt.figure()
    plt.plot(fft_freq[:fs], abs(sig_fft)[:fs])
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (V)')
    # plt.plot(fft_freq[:n // 2], 20 * np.log10(abs((sig_fft[:n // 2]))))
    # plt.ylabel('amplitude (dB20(V))')
    plt.grid(True)
    if save:
        plt.savefig('../out/square_freq.png')
    if show:
        plt.show()


if __name__ == '__main__':
    sine_wave(show=True, save=True)
    square_wave(show=True, save=True)
