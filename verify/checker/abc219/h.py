def main() -> None:
    N = int(input())
    assert 1 <= N <= 300

    for _ in range(N):
        X_i, A_i = map(int, input().split())
        assert -10**9 <= X_i <= 10**9
        assert 1 <= A_i <= 10**9


if __name__ == '__main__':
    main()
