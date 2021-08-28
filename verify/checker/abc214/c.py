def main() -> None:
    N = int(input())
    S = list(map(int, input().split()))
    T = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(S) == N
    assert len(T) == N
    assert all(1 <= S_i <= 10**9 for S_i in S)
    assert all(1 <= T_i <= 10**9 for T_i in T)


if __name__ == '__main__':
    main()
