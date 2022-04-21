def main() -> None:
    N = int(input())
    assert 2 <= N <= 50

    points = set()
    for _ in range(N):
        x, y = map(int, input().split())
        assert 0 <= x <= 1000
        assert 0 <= y <= 1000
        assert (x, y) not in points
        points.add((x, y))


if __name__ == '__main__':
    main()
