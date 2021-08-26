def main() -> None:
    N, M = map(int, input().split())
    S = list(map(int, input().split()))
    T = list(map(int, input().split()))

    assert 1 <= N <= 2*(10**5)
    assert 1 <= M <= 2*(10**5)
    assert len(S) == N
    assert len(T) == M
    assert all(S_i in (0, 1) for S_i in S)
    assert all(T_i in (0, 1) for T_i in T)


if __name__ == '__main__':
    main()
