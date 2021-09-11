def main() -> None:
    N = int(input())
    points = [tuple(map(int, input().split())) for _ in range(N)]

    assert 4 <= N <= 100
    assert all(len(point) == 2 for point in points)
    assert all(points[i] != points[j] for i in range(N) for j in range(i + 1, N))
    assert all(0 <= point[0] <= 10**9 and 0 <= point[1] <= 10**9 for point in points)


if __name__ == '__main__':
    main()
