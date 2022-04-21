def main() -> None:
    N, M = map(int, input().split())
    assert 1 <= N <= 100000
    assert 0 <= M <= 100

    for _ in range(M):
        p, S = input().split()
        p = int(p)
        assert 1 <= p <= N
        assert S in ('AC', 'WA')


if __name__ == '__main__':
    main()
