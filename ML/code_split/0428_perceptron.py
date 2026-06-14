"""
Week 9: Perceptron과 MLP의 기초 구현
====================================

이 파일은 4주간 진화할 신경망 코드의 출발점입니다.

Week 9: perceptron.py       (현재) ─ Perceptron과 하드코딩 MLP
Week 10: gradient_descent.py       ─ Gradient descent 시각화 (별도 파일)
Week 11: mlp_scratch.py            ─ Backprop 수식을 코드로
Week 12: neural_network.py         ─ Layer 추상화와 임의 구조 지원

설계 원칙:
- 처음부터 클래스 기반 (전역 변수, dict 사용 금지)
- notation 통일: 소문자 x, W, b, y
- 이해를 최우선으로 (최적화보다 명확성)
"""

import numpy as np
import matplotlib.pyplot as plt


# =====================================================
# Perceptron: 단일 뉴런
# =====================================================

class Perceptron:
    """
    단일 퍼셉트론.
    
    수식:
        z = w^T x + b
        y_hat = step(z)   # step(z) = 1 if z > 0 else -1
    
    학습 규칙:
        w <- w + lr * (t - y_hat) * x
        b <- b + lr * (t - y_hat)
    """
    
    def __init__(self, n_inputs, learning_rate=0.1, random_seed=None):
        if random_seed is not None:
            np.random.seed(random_seed)
        
        self.w = np.zeros(n_inputs)  # 작은 초기값 대신 0으로 시작
        self.b = 0.0
        self.lr = learning_rate
        self.history = {"loss": [], "weights": []}
    
    def _activation(self, z):
        """Step function: 출력은 +1 또는 -1"""
        return np.where(z > 0, 1, -1)
    
    def predict(self, x):
        """단일 샘플 또는 배치 예측"""
        x = np.atleast_2d(x)
        z = x @ self.w + self.b
        return self._activation(z)
    
    def fit(self, X, y, epochs=10, verbose=False):
        """
        학습. X: (N, n_inputs), y: (N,) with values in {-1, +1}
        """
        X = np.atleast_2d(X)
        y = np.asarray(y)
        
        for epoch in range(epochs):
            n_errors = 0
            for i in range(len(X)):
                y_hat = self.predict(X[i])[0]
                error = y[i] - y_hat
                
                # 학습 규칙 적용
                self.w = self.w + self.lr * error * X[i]
                self.b = self.b + self.lr * error
                
                if error != 0:
                    n_errors += 1
            
            self.history["loss"].append(n_errors)
            self.history["weights"].append((self.w.copy(), self.b))
            
            if verbose:
                print(f"Epoch {epoch+1}: errors={n_errors}, w={self.w}, b={self.b:.3f}")
            
            if n_errors == 0:
                if verbose:
                    print(f"Converged at epoch {epoch+1}")
                break
    
    def plot_decision_boundary(self, X, y, title="Decision Boundary", ax=None):
        """2D 데이터의 결정 경계를 시각화 (n_inputs=2 전용)"""
        if self.w.shape[0] != 2:
            raise ValueError("plot_decision_boundary는 2D 입력에서만 동작")
        
        if ax is None:
            _, ax = plt.subplots(figsize=(6, 6))
        
        X = np.atleast_2d(X)
        y = np.asarray(y)
        
        # 데이터 점
        for class_val, color, marker in [(-1, "red", "o"), (1, "blue", "s")]:
            mask = (y == class_val)
            ax.scatter(X[mask, 0], X[mask, 1], c=color, marker=marker,
                       s=100, edgecolor="black", label=f"class={class_val}")
        
        # 결정 경계: w_0 x_0 + w_1 x_1 + b = 0
        # => x_1 = -(w_0 x_0 + b) / w_1
        if abs(self.w[1]) > 1e-10:
            x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
            xs = np.linspace(x_min, x_max, 100)
            ys = -(self.w[0] * xs + self.b) / self.w[1]
            ax.plot(xs, ys, "k--", label="decision boundary")
        
        ax.set_xlabel("x_0")
        ax.set_ylabel("x_1")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_aspect("equal")
        return ax


# =====================================================
# MultiLayerPerceptron: 하드코딩 (Week 9 버전)
# =====================================================

class MultiLayerPerceptron:
    """
    Week 9에서는 학습을 아직 다루지 않습니다.
    여기서는 XOR를 풀기 위해 가중치를 '손으로' 설정한 네트워크를
    조립해 보여줍니다.
    
    Week 11에서 실제로 backpropagation으로 학습하는 MLP를 만들 것입니다.
    """
    
    def __init__(self):
        self.perceptrons = {}
    
    @classmethod
    def xor_hardcoded(cls):
        """
        XOR = AND(NAND(x_0, x_1), OR(x_0, x_1))
        
        각 gate는 단일 퍼셉트론으로 구현 가능:
        - OR:   w = [0.5, 0.5],  b =  0.7
        - NAND: w = [-0.5, -0.5], b =  0.7
        - AND:  w = [0.5, 0.5],  b = -0.7
        """
        mlp = cls()
        
        or_gate = Perceptron(n_inputs=2)
        or_gate.w = np.array([0.5, 0.5])
        or_gate.b = 0.7
        
        nand_gate = Perceptron(n_inputs=2)
        nand_gate.w = np.array([-0.5, -0.5])
        nand_gate.b = 0.7
        
        and_gate = Perceptron(n_inputs=2)
        and_gate.w = np.array([0.5, 0.5])
        and_gate.b = -0.7
        
        mlp.perceptrons["or"] = or_gate
        mlp.perceptrons["nand"] = nand_gate
        mlp.perceptrons["and"] = and_gate
        
        return mlp
    
    def predict(self, x):
        """XOR 계산: AND(NAND(x), OR(x))"""
        x = np.atleast_2d(x)
        h_or = self.perceptrons["or"].predict(x)
        h_nand = self.perceptrons["nand"].predict(x)
        
        hidden = np.column_stack([h_nand, h_or])
        output = self.perceptrons["and"].predict(hidden)
        return output


# =====================================================
# 데모 코드 (이 파일을 직접 실행할 때)
# =====================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9: Perceptron 실습 데모")
    print("=" * 60)
    
    # --- 1. AND 학습 ---
    print("\n[1] AND 게이트 학습")
    X_and = np.array([[-1, -1], [-1, 1], [1, -1], [1, 1]])
    y_and = np.array([-1, -1, -1, 1])
    
    p_and = Perceptron(n_inputs=2, learning_rate=0.1)
    p_and.fit(X_and, y_and, epochs=20, verbose=True)
    print(f"학습된 가중치: w={p_and.w}, b={p_and.b:.3f}")
    
    # --- 2. OR 학습 ---
    print("\n[2] OR 게이트 학습")
    y_or = np.array([-1, 1, 1, 1])
    p_or = Perceptron(n_inputs=2, learning_rate=0.1)
    p_or.fit(X_and, y_or, epochs=20)
    print(f"학습된 가중치: w={p_or.w}, b={p_or.b:.3f}")
    
    # --- 3. XOR 시도 (실패해야 함) ---
    print("\n[3] XOR 학습 시도 (실패 예상)")
    y_xor = np.array([-1, 1, 1, -1])
    p_xor = Perceptron(n_inputs=2, learning_rate=0.1)
    p_xor.fit(X_and, y_xor, epochs=100)
    print(f"최종 에러 수: {p_xor.history['loss'][-1]}/4 — 수렴 실패 확인")
    
    # --- 4. MLP로 XOR 해결 ---
    print("\n[4] 하드코딩 MLP로 XOR 해결")
    mlp = MultiLayerPerceptron.xor_hardcoded()
    for x in X_and:
        y_pred = mlp.predict(x)[0]
        print(f"  입력 {x} → 출력 {y_pred}")
    
    # --- 5. 시각화 ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    p_and.plot_decision_boundary(X_and, y_and, title="AND (learned)", ax=axes[0])
    p_or.plot_decision_boundary(X_and, y_or, title="OR (learned)", ax=axes[1])
    p_xor.plot_decision_boundary(X_and, y_xor, title="XOR (failed)", ax=axes[2])
    plt.tight_layout()
    plt.savefig("/tmp/week09_demo.png", dpi=100)
    print("\n시각화 저장: /tmp/week09_demo.png")
