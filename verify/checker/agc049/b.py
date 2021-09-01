def main() -> None:
    N = int(input())
    S = input()
    T = input()

    assert 1 <= N <= 100
    assert len(S) == N
    assert len(T) == N
    assert all(S_i in ('0', '1') for S_i in S)
    assert all(T_i in ('0', '1') for T_i in T)


if __name__ == '__main__':
    main()
