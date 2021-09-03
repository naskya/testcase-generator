def main() -> None:
    H, W = map(int, input().split())
    assert 2 <= H <= 100
    assert 2 <= W <= 100

    for _ in range(H):
        S = input()
        assert len(S) == W
        assert all(S_ij in ('R', 'B', '.') for S_ij in S)


if __name__ == '__main__':
    main()
