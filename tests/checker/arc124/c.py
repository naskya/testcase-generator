def main() -> None:
    N = int(input())
    assert 1 <= N <= 50

    for _ in range(N):
        a, b = map(int, input().split())
        assert 1 <= a <= 10**9
        assert 1 <= b <= 10**9


if __name__ == '__main__':
    main()
