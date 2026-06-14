"""
Week 10: Gradient Descent 시각화
"""

import numpy as np
import matplotlib.pyplot as plt


# =====================================================
# 1D Gradient Descent
# =====================================================

def gradient_descent_1d(f, df, x0, lr=0.1, n_iters=50, tol=1e-6):
    """
    1차원 함수의 gradient descent.
    
    Parameters
    ----------
    f  : callable, f(x) -> scalar
    df : callable, df(x) -> scalar (derivative)
    x0 : float, 시작점
    lr : float, 학습률
    n_iters : int, 최대 반복
    tol : float, 수렴 판정 기준
    
    Returns
    -------
    trajectory : list of (x, f(x))
    """
    x = float(x0)
    trajectory = [(x, f(x))]
    
    for _ in range(n_iters):
        grad = df(x)
        x_new = x - lr * grad
        trajectory.append((x_new, f(x_new)))
        
        if abs(x_new - x) < tol:
            break
        x = x_new
    
    return trajectory


def plot_trajectory_1d(f, trajectory, x_range=None, title="", ax=None):
    """1D gradient descent 경로를 시각화."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))
    
    xs_path = [p[0] for p in trajectory]
    ys_path = [p[1] for p in trajectory]
    
    # 함수 그래프
    if x_range is None:
        x_min, x_max = min(xs_path) - 1, max(xs_path) + 1
    else:
        x_min, x_max = x_range
    
    xs = np.linspace(x_min, x_max, 300)
    ax.plot(xs, [f(x) for x in xs], "b-", alpha=0.5, label="f(x)")
    
    # 경로
    ax.plot(xs_path, ys_path, "ro-", markersize=4, alpha=0.6, label="GD path")
    ax.plot(xs_path[0], ys_path[0], "g^", markersize=12, label="start")
    ax.plot(xs_path[-1], ys_path[-1], "k*", markersize=15, label="end")
    
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(title + f" ({len(trajectory)} iters)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return ax


# =====================================================
# 2D Gradient Descent
# =====================================================

def gradient_descent_2d(f, grad_f, x0, lr=0.1, n_iters=50, tol=1e-6):
    """
    2차원 함수의 gradient descent.
    
    Parameters
    ----------
    f      : callable, f(x, y) -> scalar
    grad_f : callable, grad_f(x, y) -> np.array of shape (2,)
    x0     : (x, y) 시작점
    """
    pos = np.array(x0, dtype=float)
    trajectory = [pos.copy()]
    
    for _ in range(n_iters):
        grad = grad_f(pos[0], pos[1])
        pos_new = pos - lr * grad
        trajectory.append(pos_new.copy())
        
        if np.linalg.norm(pos_new - pos) < tol:
            break
        pos = pos_new
    
    return np.array(trajectory)


def plot_contour_trajectory(f, trajectory, x_range=(-6, 6), y_range=(-6, 6),
                             title="", ax=None):
    """2D gradient descent 경로를 등고선 위에 시각화."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 6))
    
    # 등고선
    xs = np.linspace(x_range[0], x_range[1], 100)
    ys = np.linspace(y_range[0], y_range[1], 100)
    X, Y = np.meshgrid(xs, ys)
    Z = f(X, Y)
    
    ax.contour(X, Y, Z, levels=20, cmap="viridis", alpha=0.6)
    
    # 경로
    ax.plot(trajectory[:, 0], trajectory[:, 1], "ro-", markersize=4, alpha=0.7)
    ax.plot(trajectory[0, 0], trajectory[0, 1], "g^", markersize=15, label="start")
    ax.plot(trajectory[-1, 0], trajectory[-1, 1], "k*", markersize=18, label="end")
    
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title + f" ({len(trajectory)} iters)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")
    return ax

