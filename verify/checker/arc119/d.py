def main() -> None:
    H, W = map(int, input().split())

    assert 1 <= H <= 100
    assert 1 <= W <= 100

    for _ in range(H):
        s = input()

        assert len(s) == W
        assert all(s_ij in ('R', 'B') for s_ij in s)


if __name__ == '__main__':
    main()
