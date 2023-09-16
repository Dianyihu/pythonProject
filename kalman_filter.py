import numpy as np

'''
Kalman Filter
x(k+1,k) = A(k)*x(k)+B(k+1)*u(k+1)+w
z(k+1) = H(k+1)*x(k+1)+v

Predict:
State Extrapolation, x(k+1,k) = A(k)*x(k)+B(k+1)*u(k+1)
Covariance Extrapolation, P(k+1,k) = A(k)*P(k,k)*A(k).T+Q

Update:
Kalman Gain, K(k) = P(k,k-1)*H.T*(H*P(k,k-1)*H.T+R(k))^(-1)
State Update, x(k,k) = x(k,k-1)+K(k)*(z(k)-H*x(k,k-1))
Covariance Update, P(k,k) = (I-K(k)*H)*P(k,k-1)*(I-K(k)*H).T+K(k)*R(k)*K(k).T

temp_matrix = np.eye(K.shape[0]) - np.dot(K, self.H)
phat_1 = np.dot(np.dot(temp_matrix, phat_10), temp_matrix.T)+ np.dot(np.dot(K, R), K.T)

x: state vector, (nx, 1)
u: input variable, (nu, 1)
z: measure vector, (nz, 1)
A: state transition matrix, (nx, nx)
B: control matrix (nx, nu)
H: observation matrix, (nz, nx)

w: process noise vector, (nx, 1)
v: observation noise vector, (nz, 1)
P: estimate covariance, (nx, nx)
Q: process noise covariance, (nx, nx)
R: measurement covariance, (nz, nz)

K: Kalman gain, (nx, nz)
'''


class Kalman_filter:
    def __init__(self, A: np.ndarray, Q: np.ndarray, H: np.ndarray, R: np.ndarray, x0: np.ndarray,
                 p0: np.ndarray, B=None):
        self.A, self.Q, self.H, self.R = A, Q, H, R
        self.B = np.eye(1) if B is None else B
        self.xhat, self.phat = x0, np.expand_dims(p0, axis=0)

    def predict(self, xhat_0: np.ndarray, phat_0: np.ndarray, u_1: np.ndarray):
        xhat_10 = np.dot(self.A, xhat_0) + np.dot(self.B, u_1)
        phat_10 = np.dot(np.dot(self.A, phat_0), self.A.T) + self.Q
        return xhat_10, phat_10

    def update(self, xhat_10: np.ndarray, phat_10: np.ndarray, z_1: np.ndarray):
        K = np.dot(np.dot(phat_10, self.H.T), np.linalg.pinv(np.dot(np.dot(self.H, phat_10), self.H.T) + self.R))
        xhat_1 = xhat_10 + np.dot(K, z_1 - np.dot(self.H, xhat_10))
        # phat_1 = np.dot(np.eye(K.shape[0]) - np.dot(K, self.H), phat_10)
        temp_matrix = np.eye(K.shape[0]) - np.dot(K, self.H)
        phat_1 = np.dot(np.dot(temp_matrix, phat_10), temp_matrix.T)+ np.dot(np.dot(K, self.R), K.T)

        return xhat_1, phat_1

    def filter(self, z_list: np.ndarray, u_list=None):
        if u_list is None:
            u_list = np.zeros(z_list.shape[0]).reshape(-1, 1)

        for u_1, z_1 in zip(u_list, z_list):
            xhat_10, phat_10 = self.predict(self.xhat[:, [-1]], self.phat[-1], u_1)
            xhat_1, phat_1 = self.update(xhat_10, phat_10, z_1.reshape(-1, 1))

            self.xhat = np.append(self.xhat, xhat_1, axis=1)
            self.phat = np.append(self.phat, np.expand_dims(phat_1, axis=0), axis=0)

    def update_matrix(self, A=None, B=None, H=None, Q=None, R=None):
        if A is not None:
            self.A = A
        if B is not None:
            self.B = B
        if H is not None:
            self.H = H
        if Q is not None:
            self.Q = Q
        if R is not None:
            self.R = R

