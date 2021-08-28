def main() -> None:
    N, M, K = map(int, input().split())

    assert 1 <= N <= 100
    assert 1 <= M <= 100
    assert 1 <= K <= min(M, 10)

    for _ in range(N):
        RX, RY = map(int, input().split())
        assert 0 <= RX <= 10**9
        assert 0 <= RY <= 10**9

    for _ in range(M):
        BX, BY = map(int, input().split())
        assert 0 <= BX <= 10**9
        assert 0 <= BY <= 10**9


if __name__ == '__main__':
    main()
