def main() -> None:
    H, W, N = map(int, input().split())
    cards = [(0, 0)] * N

    for i in range(N):
        cards[i] = tuple(map(int, input().split()))

    assert 1 <= H <= 10**9
    assert 1 <= W <= 10**9
    assert 1 <= N <= min(H * W, 100)
    assert len(set(cards)) == N
    assert all(1 <= cards[i][0] <= H for i in range(N))
    assert all(1 <= cards[i][1] <= W for i in range(N))


if __name__ == '__main__':
    main()
