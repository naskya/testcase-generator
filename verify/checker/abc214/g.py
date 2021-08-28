def main() -> None:
    N = int(input())
    p = list(map(int, input().split()))
    q = list(map(int, input().split()))

    p.sort()
    q.sort()

    assert 1 <= N <= 100
    assert p == list(range(1, N + 1))
    assert q == list(range(1, N + 1))


if __name__ == '__main__':
    main()
