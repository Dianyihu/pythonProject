import numpy as np

'''
Kalman Filter
x_k+1 = A_k * x_k + B_k*u_k + R_k
z_k = H_k * x_k + Q_k

A_k: state transition matrix
B_k: control matrix
H_k: observation matrix
u_k: input matrix
R_k: process noise
Q_k: observation noise 
'''


def kf_predict(x0, p0, A, B, u, R):
    x10 = np.dot(A, x0) + np.dot(B, u)
    p10 = np.dot(np.dot(A, p0), A.T) + R
    return x10, p10


def kf_update(x10, p10, H, z, Q):
    K = np.dot(np.dot(p10, H.T), np.linalg.pinv(np.dot(np.dot(H, p10), H.T) + Q))
    x1 = x10 + np.dot(K, z - np.dot(H, x10))
    p1 = np.dot(np.eye(K.shape[0]) - np.dot(K, H), p10)
    return x1, p1


def kalman_filter(x0, p0, A, B, u, R, H, z, Q):
    x10, p10 = kf_predict(x0, p0, A, B, u, R)
    x1, p1 = kf_update(x10, p10, H, z, Q)
    return x1, p1


