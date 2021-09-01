def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    for i in range(N):
        S = input()
        assert len(S) == N
        assert all(S_i in ('0', '1') for S_i in S)
        assert S[i] == '0'


if __name__ == '__main__':
    main()
