def main() -> None:
    K, N = map(int, input().split())
    x = list(map(int, input().split()))

    assert 2 <= K <= 10
    assert 1 <= N <= 1000
    assert len(x) == K
    assert 0 <= x[0]
    assert x[-1] <= 1000
    assert all(x[i] < x[i + 1] for i in range(K - 1))


if __name__ == '__main__':
    main()
