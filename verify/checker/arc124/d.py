def main() -> None:
    N, M = map(int, input().split())
    p = list(map(int, input().split()))
    p.sort()

    assert 1 <= N <= 100
    assert 1 <= M <= 100
    assert p == list(range(1, N + M + 1))


if __name__ == '__main__':
    main()
