def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(A) == N
    assert len(B) == N
    assert len(C) == N
    assert all(1 <= A_i <= 10**9 for A_i in A)
    assert all(1 <= B_i <= 10**9 for B_i in B)
    assert all(1 <= C_i <= 10**9 for C_i in C)


if __name__ == '__main__':
    main()
