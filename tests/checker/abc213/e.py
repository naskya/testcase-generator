def main() -> None:
    H, W = map(int, input().split())
    S = []

    for _ in range(H):
        S.append(input())

    assert 2 <= H <= 100
    assert 2 <= W <= 100
    assert all(len(S_i) == W for S_i in S)
    assert all(S[i][j] in ('.', '#') for i in range(H) for j in range(W))
    assert S[0][0] == '.'
    assert S[H - 1][W - 1] == '.'


if __name__ == '__main__':
    main()
