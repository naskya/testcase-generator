def main() -> None:
    N = int(input())
    assert 4 <= N <= 1000

    XY = set()

    for _ in range(N):
        x, y, c = map(int, input().split())
        XY.add((x, y))

        assert -10**9 <= x <= 10**9
        assert -10**9 <= y <= 10**9
        assert 1 <= c <= 10**9

    assert len(XY) == N


if __name__ == '__main__':
    main()
