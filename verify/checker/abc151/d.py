def main() -> None:
    H, W = map(int, input().split())
    assert 1 <= H <= 20
    assert 1 <= W <= 20
    assert 2 <= H * W

    dots = 0
    for _ in range(H):
        S = input()
        dots += S.count('.')
        assert len(S) == W
        assert all(S_i in ('.', '#') for S_i in S)

    assert 2 <= dots


if __name__ == '__main__':
    main()
