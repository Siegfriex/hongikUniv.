"""
Week 12-13: Layer + Optimizer 추상화
=====================================

Week 11의 단일 MLP 코드를 두 단계로 일반화한 라이브러리.

    Week 11 : class MLP   (2-2-1 하드코딩, 샘플 1개씩)
    Week 12 : Layer + Network + Optimizer  (임의 구조, 미니배치, SGD)
    Week 13 : + Momentum / RMSProp / Adam  (optimizer 만 갈아끼우면 끝)

설계 철학 (PyTorch / Keras 와 동일):
    - Layer     : forward / backward 만 책임 (dW, db 만 보관)
    - Optimizer : 파라미터 갱신 규칙을 책임
    두 책임이 분리되어 있으므로 optimizer 만 바꿔도
    네트워크 코드는 한 줄도 손댈 필요가 없다.

조립 예시:
    net = Network()
    net.add(Dense(784, 128))
    net.add(ReLU())
    net.add(Dense(128, 10))
    loss_fn = SoftmaxCE()

    # ▼ 이 한 줄만 바꾸면 학습 방식이 달라진다
    optimizer = SGD(lr=0.01)
    # optimizer = Momentum(lr=0.01, mu=0.9)
    # optimizer = RMSProp(lr=0.001)
    # optimizer = Adam(lr=0.001)

    fit(net, X, Y, loss_fn, optimizer, epochs=10, batch_size=64)
"""

import numpy as np


# =====================================================
# Base Layer
# =====================================================

class Layer:
    """모든 층의 공통 인터페이스 (forward + backward)."""

    def forward(self, x):
        raise NotImplementedError

    def backward(self, grad_output):
        raise NotImplementedError

    def params_and_grads(self):
        """파라미터를 가진 층은 (param, grad) 튜플 목록을 돌려준다.
        Optimizer 가 이 목록을 받아 in-place 로 갱신한다.
        활성화 함수처럼 파라미터가 없는 층은 기본 빈 리스트."""
        return []


# =====================================================
# Dense (Fully Connected) Layer
# =====================================================

class Dense(Layer):
    """
    Z = X · W^T + b   (미니배치 형태)

    forward:   X:(N, n_in) → Z:(N, n_out)
    backward:
        dW = grad_out^T · X         shape (n_out, n_in)
        db = sum(grad_out, axis=0)  shape (n_out,)
        return grad_out · W         shape (N, n_in)   ← 앞 층으로 전파
    """

    def __init__(self, n_in, n_out, seed=None):
        if seed is not None:
            np.random.seed(seed)

        scale = np.sqrt(2.0 / n_in)   # He 초기화 (ReLU 에 적합)
        self.W = np.random.randn(n_out, n_in) * scale
        self.b = np.zeros(n_out)

        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

    def forward(self, x):
        self.x = x
        return x @ self.W.T + self.b

    def backward(self, grad_output):
        self.dW = grad_output.T @ self.x
        self.db = grad_output.sum(axis=0)
        return grad_output @ self.W

    def params_and_grads(self):
        # Optimizer 는 이 튜플들에 in-place 갱신을 적용한다.
        return [(self.W, self.dW), (self.b, self.db)]


# =====================================================
# Activation Layers (element-wise → 배치 자동 지원)
# =====================================================

class Sigmoid(Layer):
    """σ(z) = 1/(1+e^(-z)),  σ'(z) = σ(z)(1 - σ(z))"""

    def forward(self, x):
        x = np.clip(x, -500, 500)
        self.out = 1.0 / (1.0 + np.exp(-x))
        return self.out

    def backward(self, grad_output):
        return grad_output * self.out * (1.0 - self.out)


class ReLU(Layer):
    """ReLU(z) = max(0, z),  미분: 1 if z>0 else 0"""

    def forward(self, x):
        self.mask = (x > 0).astype(x.dtype)
        return x * self.mask

    def backward(self, grad_output):
        return grad_output * self.mask


class Softmax(Layer):
    """행 단위 softmax. CrossEntropy 와 함께 쓰는 게 보통이므로
    이 backward 는 'grad_output 이 이미 (p - y) 형태로 전달된다' 는 가정으로
    통과만 시킨다. 분류 학습에는 SoftmaxCE 권장."""

    def forward(self, x):
        x_shifted = x - np.max(x, axis=1, keepdims=True)
        exp_x = np.exp(x_shifted)
        self.out = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return self.out

    def backward(self, grad_output):
        return grad_output


# =====================================================
# Loss Functions
# =====================================================

class MSELoss:
    """L = (1/2N) Σ ||y_pred - y_true||²"""

    def forward(self, y_pred, y_true):
        N = y_pred.shape[0]
        self.diff = y_pred - y_true
        self.N = N
        return 0.5 * np.sum(self.diff ** 2) / N

    def backward(self):
        return self.diff / self.N


class SoftmaxCE:
    """Softmax + Cross-Entropy 결합.
        ∂L/∂logits = (softmax(logits) - y_true) / N
    log-sum-exp 트릭으로 수치 안정.
    """

    def forward(self, logits, y_true):
        N = logits.shape[0]
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        log_sum_exp = np.log(np.sum(np.exp(shifted), axis=1, keepdims=True))
        log_probs = shifted - log_sum_exp
        self.probs = np.exp(log_probs)
        self.y_true = y_true
        self.N = N
        return -np.sum(y_true * log_probs) / N

    def backward(self):
        return (self.probs - self.y_true) / self.N

    def predict_proba(self, logits):
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        exp_x = np.exp(shifted)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)


# =====================================================
# Optimizers  (Week 13)
# =====================================================
#
# 공통 인터페이스:
#     opt = Optimizer(lr=...)
#     opt.step(net)        # net 의 모든 파라미터를 한 번에 업데이트
#
# 내부적으로 Layer.params_and_grads() 를 순회.
# Momentum / RMSProp / Adam 처럼 "이전 상태" 가 필요한 optimizer 는
# 파라미터의 id() 를 key 로 한 dict 에 상태를 저장한다.
# =====================================================


class Optimizer:
    """모든 optimizer 의 공통 인터페이스."""

    def step(self, net):
        """net 의 모든 (param, grad) 쌍에 대해 in-place 갱신."""
        for layer in net.layers:
            for param, grad in layer.params_and_grads():
                self._update(param, grad)

    def _update(self, param, grad):
        raise NotImplementedError


class SGD(Optimizer):
    """θ ← θ − η·∇L."""

    def __init__(self, lr=0.01):
        self.lr = lr

    def _update(self, param, grad):
        param -= self.lr * grad


class Momentum(Optimizer):
    """v ← μ·v − η·∇L
       θ ← θ + v
    이전 갱신 방향을 누적해 진동을 줄이고 골짜기를 빠르게 통과.
    """

    def __init__(self, lr=0.01, mu=0.9):
        self.lr = lr
        self.mu = mu
        self.v = {}   # id(param) → velocity

    def _update(self, param, grad):
        key = id(param)
        if key not in self.v:
            self.v[key] = np.zeros_like(param)
        self.v[key] = self.mu * self.v[key] - self.lr * grad
        param += self.v[key]


class RMSProp(Optimizer):
    """s ← ρ·s + (1−ρ)·g²
       θ ← θ − η · g / (√s + ε)
    차원마다 그래디언트 크기를 추적해 step 크기를 자동 조정.
    """

    def __init__(self, lr=0.001, rho=0.9, eps=1e-8):
        self.lr = lr
        self.rho = rho
        self.eps = eps
        self.s = {}

    def _update(self, param, grad):
        key = id(param)
        if key not in self.s:
            self.s[key] = np.zeros_like(param)
        self.s[key] = self.rho * self.s[key] + (1 - self.rho) * (grad ** 2)
        param -= self.lr * grad / (np.sqrt(self.s[key]) + self.eps)


class Adam(Optimizer):
    """Momentum (1차 모멘트) + RMSProp (2차 모멘트) 결합.
       m ← β₁·m + (1−β₁)·g
       v ← β₂·v + (1−β₂)·g²
       m̂ = m/(1−β₁ᵗ),  v̂ = v/(1−β₂ᵗ)         ← 편향 보정
       θ ← θ − η · m̂ / (√v̂ + ε)
    """

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = {}
        self.v = {}
        self.t = 0   # time step (전역)

    def step(self, net):
        self.t += 1   # step 호출 단위로 한 번 증가
        super().step(net)

    def _update(self, param, grad):
        key = id(param)
        if key not in self.m:
            self.m[key] = np.zeros_like(param)
            self.v[key] = np.zeros_like(param)
        self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grad
        self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * (grad ** 2)
        m_hat = self.m[key] / (1 - self.beta1 ** self.t)
        v_hat = self.v[key] / (1 - self.beta2 ** self.t)
        param -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


# =====================================================
# Network
# =====================================================

class Network:
    """Layer 들을 순차적으로 쌓는 컨테이너. Keras 의 Sequential 과 동일."""

    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)
        return self

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad):
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def predict(self, X):
        return self.forward(X)

    def evaluate_classification(self, X, Y):
        """One-hot encoded Y 에 대한 분류 정확도."""
        preds = self.forward(X)
        return np.mean(preds.argmax(axis=1) == Y.argmax(axis=1))


# =====================================================
# 학습 루프
# =====================================================

def fit(net, X, Y, loss_fn, optimizer,
        epochs=100, batch_size=32, verbose=True):
    """Mini-batch 학습.
        X : (N, n_input)
        Y : (N, n_output)
        optimizer : SGD / Momentum / RMSProp / Adam 중 하나
    """
    N = len(X)
    history = {"loss": []}

    for epoch in range(epochs):
        idx = np.random.permutation(N)
        epoch_loss = 0.0
        n_batches = 0

        for start in range(0, N, batch_size):
            batch_idx = idx[start:start + batch_size]
            X_batch = X[batch_idx]
            Y_batch = Y[batch_idx]

            pred = net.forward(X_batch)
            loss = loss_fn.forward(pred, Y_batch)
            grad = loss_fn.backward()
            net.backward(grad)
            optimizer.step(net)        # ← Week 12 의 net.update(lr) 대신

            epoch_loss += loss
            n_batches += 1

        avg_loss = epoch_loss / n_batches
        history["loss"].append(avg_loss)

        if verbose and (epoch % max(1, epochs // 10) == 0):
            print(f"Epoch {epoch:4d}: loss = {avg_loss:.6f}")

    return history
