import sys
from time import time
from gmpy2 import mpz, isqrt  # 使用gmpy2高性能库
from tqdm import tqdm

sys.set_int_max_str_digits(100000000)

def sqrt_fast(n, one):
    """利用gmpy2的isqrt函数优化平方根计算"""
    return isqrt(n * one)

def pi_chudnovsky_extreme(digits):
    """极端优化的Chudnovsky算法实现"""
    one = mpz(10)**digits
    k = mpz(1)
    a_k = one
    a_sum = one
    b_sum = mpz(0)
    C = mpz(640320)
    C3_OVER_24 = C**3 // 24
    DIGITS_PER_TERM = 14.181647462  # 精确项数计算: log10(151931373056000/(C3_OVER_24)))
    total_terms = int(digits / DIGITS_PER_TERM + 1)
    
    # 预计算常数优化循环
    factor_cache = []
    for k_pre in range(1, total_terms+1):
        numerator = -(6*k_pre - 5)*(2*k_pre - 1)*(6*k_pre - 1)
        denominator = k_pre**3 * C3_OVER_24
        factor_cache.append((numerator, denominator))
    
    # 主循环优化：减少重复计算
    with tqdm(total=total_terms, desc="π计算进度", unit="term") as pbar:
        for k in range(1, total_terms+1):
            numerator, denominator = factor_cache[k-1]
            a_k = a_k * numerator // denominator
            a_sum += a_k
            b_sum += k * a_k
            if a_k == 0:
                break
            pbar.update(1)

    sqrt_term = 10005 * one
    sqrt_10005 = sqrt_fast(sqrt_term, one)
    pi = (426880 * sqrt_10005 * one) // (13591409*a_sum + 545140134*b_sum)
    return pi

if __name__ == "__main__":
    digits = int(input("请输入要计算的圆周率位数："))
    start = time()
    
    # 计算圆周率
    pi = pi_chudnovsky_extreme(digits)
    
    # 格式化输出优化
    pi_str = f"{pi}"
    formatted = f"3.{pi_str[1:]}" if len(pi_str) > 1 else "3.14"  # 处理特殊情况
    
    # 高效写入文件
    print("\n保存文件中...")
    with open("π.txt", "w") as f:
        f.write(formatted)
    
    print(f"\n计算完成，总耗时：{time() - start:.3f}秒")
    print(f"前50位验证：{formatted[:52]}")