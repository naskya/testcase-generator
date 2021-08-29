def main() -> None:
    N, K = map(int, input().split())
    P = list(map(int, input().split()))

    P.sort()

    assert 2 <= N <= 100
    assert 1 <= K <= N - 1
    assert len(P) == N
    assert P == list(range(1, N + 1))


if __name__ == '__main__':
    main()
