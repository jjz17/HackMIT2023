import pandas as pd
import numpy as np
# np.random.seed(555)
import matplotlib.pyplot as plt
import bocd

def bocd_analysis(arr, constant_hazard=7):
    # Initialize object
    bc = bocd.BayesianOnlineChangePointDetection(bocd.ConstantHazard(constant_hazard), bocd.StudentT(mu=0, kappa=1, alpha=1, beta=1))

    # Online estimation and get the maximum likelihood r_t at each time point
    rt_mle = np.empty(arr.shape)
    for i, d in enumerate(arr):
        bc.update(d)
        rt_mle[i] = bc.rt 
    # Plot data with estimated change points
    index_changes = np.where(np.diff(rt_mle)<0)[0]
    return {
        "arr": arr,
        "index_changes": index_changes,
    }

    # plt.plot(arr, alpha=0.5, label="observation")
    # plt.scatter(index_changes, arr[index_changes], c='green', label="change point")