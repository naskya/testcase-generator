def main() -> None:
    N, X = map(int, input().split())

    assert 1 <= N <= 100
    assert 1 <= X <= 10**6

    for _ in range(N):
        A_i, C_i = map(int, input().split())

        assert 1 <= A_i <= 10**6
        assert 1 <= C_i <= 10**6


if __name__ == '__main__':
    main()
