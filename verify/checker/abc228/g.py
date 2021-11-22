def main() -> None:
    H, W, N = map(int, input().split())

    assert 2 <= H <= 10
    assert 2 <= W <= 10
    assert 1 <= N <= 300

    for _ in range(H):
        c_i = list(map(int, input().split()))

        assert len(c_i) == W
        assert all(1 <= c_ij <= 9 for c_ij in c_i)


if __name__ == '__main__':
    main()
