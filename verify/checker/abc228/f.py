def main() -> None:
    H, W, h1, w1, h2, w2 = map(int, input().split())

    assert 2 <= H <= 100
    assert 2 <= W <= 100
    assert 1 <= h1 <= H
    assert 1 <= h2 <= H
    assert 1 <= w1 <= W
    assert 1 <= w2 <= W

    for _ in range(H):
        A_i = list(map(int, input().split()))

        assert len(A_i) == W
        assert all(1 <= A_ij <= 10**9 for A_ij in A_i)


if __name__ == '__main__':
    main()
