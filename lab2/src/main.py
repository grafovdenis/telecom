import numpy as np
from scipy import signal
import time
import matplotlib.pyplot as plt


def position(correlations, sinc_package):
    for i in range(0, len(correlations) - 3):
        if sum(correlations[i:i + 3]) == sum(sinc_package):
            return i + 1


# x(t) = convolve(sign(sin(t)), sign(sin(t)))
def triangle_wave(freq=20, show=False, save=False):
    fs = 1000  # sampling rate
    ts = 1 / fs  # sampling interval
    n = 8192  # number of fft points, pick power of 2
    t = np.arange(0, n * ts, ts)  # time vector
    sig = np.convolve(np.sign(np.sin(2 * np.pi * freq * t)), np.sign(np.sin(2 * np.pi * freq * t)), 'same')  # signal
    sig_fft = np.fft.fft(sig) / n * 2  # /N to scale due to python DFT equation,
    # *2 to make single sided
    fft_freq = np.fft.fftfreq(n, ts)  # python function to get Hz frequency axis

    plt.figure()
    plt.plot(t[0:250], sig[0:250])
    plt.xlabel('time (S)')
    plt.ylabel('amplitude (V)')
    plt.grid(True)
    if save:
        plt.savefig('../out/triangle_time.png')
    if show:
        plt.show()

    plt.figure()
    plt.plot(fft_freq[:fs], abs(sig_fft)[:fs])
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (V)')
    plt.grid(True)
    if save:
        plt.savefig('../out/triangle_freq.png')
    if show:
        plt.show()


def package():
    sinc_package = np.array([1, 0, 1], dtype=int)
    sig = np.array([0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0], dtype=int)

    start_time = time.time()
    correlations_direct = signal.correlate(sig, sinc_package, mode='valid', method='direct')  # прямой метод
    print("Direct method:\n--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    correlations_fft = signal.correlate(sig, sinc_package, mode='valid', method='fft')  # быстрая корреляция
    print("FFT method:\n--- %s seconds ---" % (time.time() - start_time))

    print("Correlations using direct method:", correlations_direct)
    print("Correlations using FFT method   :", correlations_fft)
    pos = position(correlations_direct, sinc_package)
    print("Position with direct correlation:", pos)
    print("Position with FFT correlation   :", position(correlations_fft, sinc_package))
    package = sig[pos + 3:][:8]
    print("Package: ", package)


if __name__ == '__main__':
    package()
    triangle_wave(show=True, save=True)
