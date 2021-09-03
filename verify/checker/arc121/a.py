def main() -> None:
    N = int(input())
    assert 3 <= N <= 100

    for _ in range(N):
        x, y = map(int, input().split())
        assert -10**9 <= x <= 10**9
        assert -10**9 <= y <= 10**9


if __name__ == '__main__':
    main()
