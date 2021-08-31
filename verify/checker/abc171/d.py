def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    Q = int(input())
    B = [0] * Q
    C = [0] * Q

    for i in range(Q):
        B[i], C[i] = map(int, input().split())

    assert 1 <= N <= 100
    assert len(A) == N
    assert all(1 <= A_i <= 10**5 for A_i in A)
    assert 1 <= Q <= 100
    assert all(1 <= B_i <= 10**5 for B_i in B)
    assert all(1 <= C_i <= 10**5 for C_i in C)
    assert all(B[i] != C[i] for i in range(Q))


if __name__ == '__main__':
    main()
