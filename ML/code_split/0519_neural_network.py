"""
Week 12: Layer 추상화 — 임의의 신경망 구조 지원
=================================================

Week 11의 `mlp_scratch.py`를 일반화합니다.

핵심 변화:
    Week 11: class MLP  (2-2-1 구조에 하드코딩, 샘플 1개씩 처리)
    Week 12: class Network + Layer 계층 (임의 구조, 미니배치 일괄 처리)

조립 예시:
    net = Network()
    net.add(Dense(784, 128))
    net.add(ReLU())
    net.add(Dense(128, 64))
    net.add(ReLU())
    net.add(Dense(64, 10))      # 분류는 logit까지만
    loss_fn = SoftmaxCE()       # Softmax + CrossEntropy 결합

이 구조는 Keras의 Sequential API와 동일한 설계 철학을 따릅니다.
Week 13 이후 framework로 전환할 때 자연스럽게 연결됩니다.

배치 컨벤션:
    모든 forward/backward는 (N, ...) 형태의 배치를 입력으로 받는다.
    N=1인 경우도 (1, n_in) shape로 넣으면 동일하게 동작한다.

Layer 공통 인터페이스:
    forward(x)          : (N, n_in)   → (N, n_out)
    backward(grad_out)  : (N, n_out)  → (N, n_in)
                         파라미터가 있는 층은 dW, db도 계산해 저장
    update(lr)          : 파라미터 업데이트 (없는 층은 no-op)
"""

import numpy as np


# =====================================================
# Base Layer
# =====================================================

class Layer:
    """모든 층의 공통 인터페이스."""

    def forward(self, x):
        raise NotImplementedError

    def backward(self, grad_output):
        raise NotImplementedError

    def update(self, lr):
        pass  # 파라미터 없는 층은 기본적으로 no-op


# =====================================================
# Dense (Fully Connected) Layer
# =====================================================

class Dense(Layer):
    """
    Z = X · W^T + b   (배치 형태)

    수식 (배치 크기 N):
        forward:   Z = X · W^T + b      X:(N, n_in)  → Z:(N, n_out)
        backward:
            ∂L/∂W = grad_out^T · X      shape (n_out, n_in)
            ∂L/∂b = sum(grad_out, axis=0)
            ∂L/∂X = grad_out · W        이전 층으로 전파, shape (N, n_in)
    """

    def __init__(self, n_in, n_out, seed=None):
        if seed is not None:
            np.random.seed(seed)

        # He 초기화 (ReLU에 적합).
        scale = np.sqrt(2.0 / n_in)
        self.W = np.random.randn(n_out, n_in) * scale  # (n_out, n_in)
        self.b = np.zeros(n_out)                       # (n_out,)

        self.dW = np.zeros_like(self.W)
        self.db = np.zeros_like(self.b)

    def forward(self, x):
        # x: (N, n_in) → (N, n_out)
        self.x = x
        return x @ self.W.T + self.b

    def backward(self, grad_output):
        # grad_output: (N, n_out)
        # 배치 평균은 loss에서 이미 처리되므로 여기서는 합산만 한다.
        self.dW = grad_output.T @ self.x         # (n_out, n_in)
        self.db = grad_output.sum(axis=0)        # (n_out,)
        return grad_output @ self.W              # (N, n_in)

    def update(self, lr):
        self.W -= lr * self.dW
        self.b -= lr * self.db


# =====================================================
# Activation Layers (모두 element-wise → 자동으로 배치 지원)
# =====================================================

class Sigmoid(Layer):
    """σ(z) = 1/(1+e^(-z)),  σ'(z) = σ(z)(1 - σ(z))"""

    def forward(self, x):
        x = np.clip(x, -500, 500)  # overflow 방지
        self.out = 1.0 / (1.0 + np.exp(-x))
        return self.out

    def backward(self, grad_output):
        return grad_output * self.out * (1.0 - self.out)


class ReLU(Layer):
    """ReLU(z) = max(0, z),  미분: 1 if z > 0 else 0"""

    def forward(self, x):
        self.mask = (x > 0).astype(x.dtype)
        return x * self.mask

    def backward(self, grad_output):
        return grad_output * self.mask


class Softmax(Layer):
    """
    행 단위(axis=1) softmax. 분류 출력층 전용.

    CrossEntropyLoss와 함께 쓰는 것을 가정하고 backward를 단순화:
        ∂L/∂z = y_pred - y_true   (이 값을 loss.backward()가 전달)

    분류 학습에는 보통 SoftmaxCE를 쓰는 것을 권장.
    이 클래스는 단독으로 확률을 얻고 싶을 때(예: 추론) 사용.
    """

    def forward(self, x):
        # 수치 안정성: 행별 최댓값을 뺌
        x_shifted = x - np.max(x, axis=1, keepdims=True)
        exp_x = np.exp(x_shifted)
        self.out = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return self.out

    def backward(self, grad_output):
        # CrossEntropy + Softmax 결합 gradient를 그대로 통과
        return grad_output


# =====================================================
# Loss Functions
# =====================================================

class MSELoss:
    """
    Mean Squared Error: L = (1/2N) Σ ||y_pred - y_true||²
    배치 평균을 취해 batch_size에 무관한 학습률 사용 가능.
    """

    def forward(self, y_pred, y_true):
        N = y_pred.shape[0]
        self.diff = y_pred - y_true
        self.N = N
        return 0.5 * np.sum(self.diff ** 2) / N

    def backward(self):
        return self.diff / self.N


class SoftmaxCE:
    """
    Softmax + Cross-Entropy를 하나로 묶은 loss.
    분류 학습에 권장.

    네트워크는 마지막 Dense까지만 두고(즉, logit 출력),
    이 loss가 내부에서 softmax를 적용한 뒤 CE를 계산한다.

        L = -(1/N) Σ y_true · log(softmax(logits))
        ∂L/∂logits = (softmax(logits) - y_true) / N

    이렇게 결합하면:
      1) log-sum-exp 트릭으로 수치 안정성이 좋아진다.
      2) backward gradient가 매우 단순해진다.
    """

    def forward(self, logits, y_true):
        N = logits.shape[0]
        # log-sum-exp로 안정적인 log_softmax
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        log_sum_exp = np.log(np.sum(np.exp(shifted), axis=1, keepdims=True))
        log_probs = shifted - log_sum_exp           # log(softmax)
        self.probs = np.exp(log_probs)              # 확률 (backward에서 사용)
        self.y_true = y_true
        self.N = N
        return -np.sum(y_true * log_probs) / N

    def backward(self):
        return (self.probs - self.y_true) / self.N

    # 추론용 helper
    def predict_proba(self, logits):
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        exp_x = np.exp(shifted)
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)


# =====================================================
# Network
# =====================================================

class Network:
    """
    Layer들을 순차적으로 쌓는 컨테이너. Keras의 Sequential과 동일한 역할.
    """

    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)
        return self  # chaining 지원

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad):
        for layer in reversed(self.layers):  # ← "역"전파
            grad = layer.backward(grad)

    def update(self, lr):
        for layer in self.layers:
            layer.update(lr)

    def predict(self, X):
        return self.forward(X)

    def evaluate_classification(self, X, Y):
        """One-hot encoded Y에 대한 분류 정확도."""
        preds = self.forward(X)
        return np.mean(preds.argmax(axis=1) == Y.argmax(axis=1))


# =====================================================
# 학습 루프
# =====================================================

def fit(net, X, Y, loss_fn, epochs=100, batch_size=32, lr=0.01, verbose=True):
    """
    Mini-batch 학습.
        X : (N, n_input)
        Y : (N, n_output)
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

            # 미니배치를 통째로 forward/backward
            pred = net.forward(X_batch)
            loss = loss_fn.forward(pred, Y_batch)
            grad = loss_fn.backward()
            net.backward(grad)
            net.update(lr)

            epoch_loss += loss
            n_batches += 1

        avg_loss = epoch_loss / n_batches
        history["loss"].append(avg_loss)

        if verbose and (epoch % max(1, epochs // 10) == 0):
            print(f"Epoch {epoch:4d}: loss = {avg_loss:.6f}")

    return history
