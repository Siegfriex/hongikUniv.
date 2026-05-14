"""
Week 11: Backpropagation의 Scratch 구현
========================================

이 파일이 강의 전체에서 가장 중요한 코드입니다.
2-2-1 네트워크의 9개 편미분을 수식 그대로 구현합니다.

네트워크 구조:
    
    x_0 ─┐
          ├─ [Dense 2→2] ─ [sigmoid] ─ [Dense 2→1] ─ ŷ
    x_1 ─┘                                           │
                                                     L = (1/2)(y - ŷ)²

수식 (강의록 Week 11 슬라이드 4, 16과 일치):

    Forward:
        z^(1)_i = W^(1)_{ij} x_j + b^(1)_i        (i=0,1)
        a^(1)_i = sigmoid(z^(1)_i)
        z^(2)   = W^(2)_i a^(1)_i + b^(2)
        a^(2)   = z^(2)                             (출력층 활성화 없음)
        L       = (1/2)(y - a^(2))²
    
    Backward (9개 편미분):
        ∂L/∂W^(2)_i = (a^(2) - y) · a^(1)_i
        ∂L/∂b^(2)   = (a^(2) - y)
        
        δ^(1)_i     = (a^(2) - y) · W^(2)_i · a^(1)_i · (1 - a^(1)_i)
        ∂L/∂W^(1)_ij = δ^(1)_i · x_j
        ∂L/∂b^(1)_i  = δ^(1)_i

설계 원칙:
- 수식과 코드가 1:1 대응 (주석으로 수식 명시)
- 학생이 검증할 수 있도록 중간값을 명시적으로 반환
- dict 스타일(net["w0"])을 쓰지 않음 — 행렬 기반
"""

import numpy as np


def sigmoid(z):
    """σ(z) = 1 / (1 + e^(-z))"""
    # 수치 안정성을 위한 clipping
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime_from_output(a):
    """
    σ'(z) = σ(z)(1 - σ(z)) = a(1 - a)
    
    forward에서 이미 계산된 a를 받으면 효율적.
    (Week 10 슬라이드 19에서 유도한 수식)
    """
    return a * (1.0 - a)


class MLP:
    """
    2-입력, 2-은닉, 1-출력 MLP.
    구조는 고정. Week 12에서 임의 구조로 일반화할 예정.
    
    파라미터:
        W1 : (2, 2)  # W1[i, j] = j번째 입력 → i번째 은닉 뉴런
        b1 : (2,)
        W2 : (1, 2)
        b2 : (1,)
    """
    
    def __init__(self, n_input=2, n_hidden=2, n_output=1, random_seed=None):
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # 작은 랜덤값으로 초기화
        self.W1 = np.random.randn(n_hidden, n_input) * 0.5
        self.b1 = np.zeros(n_hidden)
        self.W2 = np.random.randn(n_output, n_hidden) * 0.5
        self.b2 = np.zeros(n_output)
        
        self.history = {"loss": []}
    
    # -------- Forward --------
    def forward(self, x):
        """
        단일 샘플 예측. x: shape (n_input,)
        """
        z1 = self.W1 @ x + self.b1      # shape (n_hidden,)
        a1 = sigmoid(z1)                 # shape (n_hidden,)
        z2 = self.W2 @ a1 + self.b2      # shape (n_output,)
        a2 = z2                          # 출력 활성화 없음
        return a2
    
    def forward_with_cache(self, x):
        """
        Backward에 필요한 중간값을 함께 반환.
        
        Returns
        -------
        cache : dict with keys x, z1, a1, z2, a2
        """
        z1 = self.W1 @ x + self.b1
        a1 = sigmoid(z1)
        z2 = self.W2 @ a1 + self.b2
        a2 = z2
        
        return {"x": x, "z1": z1, "a1": a1, "z2": z2, "a2": a2}
    
    # -------- Backward --------
    def backward(self, cache, y):
        """
        단일 샘플에 대한 9개 편미분 계산.
        
        cache : forward_with_cache의 출력
        y     : 타겟 값 (shape (n_output,))
        
        Returns
        -------
        grads : dict with keys dW1, db1, dW2, db2
        """
        x, a1, a2 = cache["x"], cache["a1"], cache["a2"]
        
        # 1. 출력층 오차
        #    ∂L/∂a2 = a2 - y
        dL_da2 = a2 - y                                 # shape (n_output,)
        
        # 2. 출력층 파라미터 gradient
        #    ∂L/∂W2[i,j] = dL_da2[i] · a1[j]
        #    ∂L/∂b2[i]   = dL_da2[i]
        dW2 = np.outer(dL_da2, a1)                      # shape (n_output, n_hidden)
        db2 = dL_da2                                    # shape (n_output,)
        
        # 3. 은닉층으로 에러 역전파
        #    ∂L/∂a1 = W2^T · dL_da2    (다음 층으로 gradient 전파)
        dL_da1 = self.W2.T @ dL_da2                     # shape (n_hidden,)
        
        # 4. Sigmoid 미분 통과
        #    δ^(1) = ∂L/∂z1 = ∂L/∂a1 · σ'(z1) = ∂L/∂a1 · a1(1-a1)
        delta1 = dL_da1 * sigmoid_prime_from_output(a1) # shape (n_hidden,)
        
        # 5. 은닉층 파라미터 gradient
        #    ∂L/∂W1[i,j] = δ^(1)[i] · x[j]
        #    ∂L/∂b1[i]   = δ^(1)[i]
        dW1 = np.outer(delta1, x)                       # shape (n_hidden, n_input)
        db1 = delta1                                    # shape (n_hidden,)
        
        return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}
    
    # -------- Training --------
    def train(self, X, Y, epochs=10000, lr=0.1, verbose=False, log_every=1000):
        """
        전체 데이터셋에 대한 학습.
        
        X : (N, n_input)
        Y : (N, n_output)
        """
        X = np.atleast_2d(X)
        Y = np.atleast_2d(Y)
        if Y.ndim == 1:
            Y = Y.reshape(-1, 1)
        
        N = len(X)
        
        for epoch in range(epochs):
            # 배치 전체에 대한 gradient 누적
            total_dW1 = np.zeros_like(self.W1)
            total_db1 = np.zeros_like(self.b1)
            total_dW2 = np.zeros_like(self.W2)
            total_db2 = np.zeros_like(self.b2)
            total_loss = 0.0
            
            for x, y in zip(X, Y):
                cache = self.forward_with_cache(x)
                grads = self.backward(cache, y)
                
                total_dW1 += grads["dW1"]
                total_db1 += grads["db1"]
                total_dW2 += grads["dW2"]
                total_db2 += grads["db2"]
                
                total_loss += 0.5 * np.sum((y - cache["a2"]) ** 2)
            
            # 평균 gradient로 업데이트
            self.W1 -= lr * total_dW1 / N
            self.b1 -= lr * total_db1 / N
            self.W2 -= lr * total_dW2 / N
            self.b2 -= lr * total_db2 / N
            
            avg_loss = total_loss / N
            self.history["loss"].append(avg_loss)
            
            if verbose and (epoch % log_every == 0):
                print(f"Epoch {epoch:5d}: loss = {avg_loss:.6f}")
        
        return self.history["loss"]
    
    def predict(self, X):
        """배치 예측."""
        X = np.atleast_2d(X)
        return np.array([self.forward(x) for x in X])


# =====================================================
# 검증: 손계산과의 비교
# =====================================================

def verification_example():
    """
    학생이 손으로 계산할 수 있는 간단한 예제.
    가중치를 명시적으로 설정하고 한 샘플의 forward + backward를 출력.
    이 값을 종이에 손으로 계산한 것과 비교 가능.
    """
    print("=" * 60)
    print("검증 예제: 손계산 vs 코드")
    print("=" * 60)
    
    mlp = MLP()
    # 명시적 가중치 설정 (학생이 손계산하기 쉽도록 간단한 값)
    mlp.W1 = np.array([[0.1, 0.2],
                       [0.3, 0.4]])
    mlp.b1 = np.array([0.0, 0.0])
    mlp.W2 = np.array([[0.5, 0.6]])
    mlp.b2 = np.array([0.0])
    
    x = np.array([1.0, 1.0])
    y = np.array([0.0])
    
    print(f"\n입력 x = {x}")
    print(f"타겟 y = {y}")
    print(f"\nW1 =\n{mlp.W1}")
    print(f"b1 = {mlp.b1}")
    print(f"W2 = {mlp.W2}")
    print(f"b2 = {mlp.b2}")
    
    # Forward
    cache = mlp.forward_with_cache(x)
    print("\n--- Forward ---")
    print(f"z1 = W1·x + b1 = {cache['z1']}")
    print(f"a1 = sigmoid(z1) = {cache['a1']}")
    print(f"z2 = W2·a1 + b2 = {cache['z2']}")
    print(f"a2 = z2 = {cache['a2']}")
    
    loss = 0.5 * np.sum((y - cache["a2"]) ** 2)
    print(f"L = (1/2)(y - a2)^2 = {loss}")
    
    # Backward
    grads = mlp.backward(cache, y)
    print("\n--- Backward (9개 편미분) ---")
    print(f"∂L/∂W2 = {grads['dW2']}")
    print(f"∂L/∂b2 = {grads['db2']}")
    print(f"∂L/∂W1 =\n{grads['dW1']}")
    print(f"∂L/∂b1 = {grads['db1']}")
    
    print("\n※ 위 값들을 종이에 손으로 계산한 것과 일치해야 합니다.")


def gradient_check(mlp, x, y, epsilon=1e-5):
    """
    모든 파라미터(W1, b1, W2, b2)에 대해 분석 미분과 수치 미분을 비교.
    최대 상대 오차를 반환.
    """
    # 1. 분석 미분 (backward로 한 번에 계산)
    cache = mlp.forward_with_cache(x)
    analytical = mlp.backward(cache, y)
    
    def loss_fn():
        a2 = mlp.forward(x)
        return 0.5 * np.sum((y - a2) ** 2)
    
    max_rel_err = 0.0
    
    # 2. 모든 파라미터를 순회하며 수치 미분과 비교
    params = [
        ('W1', mlp.W1, analytical['dW1']),
        ('b1', mlp.b1, analytical['db1']),
        ('W2', mlp.W2, analytical['dW2']),
        ('b2', mlp.b2, analytical['db2']),
    ]
    
    for name, param, grad_analytical in params:
        # 다차원 배열을 1차원으로 보고 모든 원소 검사
        it = np.nditer(param, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            idx = it.multi_index
            orig = param[idx]
            
            param[idx] = orig + epsilon
            loss_plus = loss_fn()
            param[idx] = orig - epsilon
            loss_minus = loss_fn()
            param[idx] = orig  # 복원
            
            numerical = (loss_plus - loss_minus) / (2 * epsilon)
            ana = grad_analytical[idx]
            
            # 상대 오차 = |수치 - 분석| / max(|수치|, |분석|, eps)
            abs_err = abs(numerical - ana)
            denom = max(abs(numerical), abs(ana), 1e-12)
            rel_err = abs_err / denom
            
            if rel_err > max_rel_err:
                max_rel_err = rel_err
            
            it.iternext()
    
    return max_rel_err


# =====================================================
# XOR 학습 데모
# =====================================================

def train_xor():
    """Week 11의 성과: XOR를 backprop으로 학습."""
    print("\n" + "=" * 60)
    print("XOR 학습 (2-2-1 MLP + Backpropagation)")
    print("=" * 60)
    
    X = np.array([[0.0, 0.0],
                  [0.0, 1.0],
                  [1.0, 0.0],
                  [1.0, 1.0]])
    Y = np.array([[0.0], [1.0], [1.0], [0.0]])
    
    # 출력층에 활성화가 없으므로 타겟을 약간 조정해도 되지만,
    # 여기서는 [0, 1] 타겟 그대로 회귀 학습
    mlp = MLP(random_seed=42)
    mlp.train(X, Y, epochs=10000, lr=0.5, verbose=True, log_every=2000)
    
    print("\n--- 학습 완료 후 예측 ---")
    for x, y in zip(X, Y):
        pred = mlp.forward(x)[0]
        print(f"  입력 {x} → 예측 {pred:+.4f} (타겟 {y[0]})")



