import statsmodels.tsa.seasonal as stats
import numpy as np


def remove_trend(series, period=365):
    decomposition = stats.seasonal_decompose(series, period=period)
    stationary_series = decomposition.observed - decomposition.trend

    return stationary_series


def noise(series, period=365):
    decomposition = stats.seasonal_decompose(series, period=period)
    noise = decomposition.observed - decomposition.trend - \
            decomposition.seasonal

    return noise


def no_noise(series, period=365):
    decomposition = stats.seasonal_decompose(series, period=period)
    no_noise = decomposition.observed - noise(series, period=period)

    return no_noise


def autocorrelation_pd(series):
    rho = []
    for k in range(len(series)):
        rho.append(series.autocorr(k))

    return np.array(rho)


def autocorrelation(series):
    # Source: https://iopscience.iop.org/article/10.1088/0026-1394/47/5/012/pdf
    mu = np.nanmean(series)
    norm = np.var(series) * len(series)
    aux = np.array(series.values - mu)
    rho = [aux.dot(aux)]
    for k in range(1, len(series)):
        conv = np.array(aux[k:].dot(aux[:-k]))
        rho.append(conv)

    return np.array(rho / norm)


def corrected_mean(series, rho):
    N = len(series)
    var = np.var(series)
    aux = np.array(list(range(1, N)))
    var_corrected = var / N * (1 + 2 * np.sum((N - aux) * rho[aux]) / N)

    return np.mean(series), np.sqrt(var_corrected)
