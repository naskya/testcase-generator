def main() -> None:
    N = int(input())
    S = []
    T = []

    for _ in range(N):
        S.append(input())
    for _ in range(N):
        T.append(input())

    assert 1 <= N <= 100
    assert all(len(S_i) == N for S_i in S)
    assert all(len(T_i) == N for T_i in S)
    assert all(S_ij in ('.', '#') for S_i in S for S_ij in S_i)
    assert all(T_ij in ('.', '#') for T_i in T for T_ij in T_i)
    assert any(S_ij == '#' for S_i in S for S_ij in S_i)
    assert any(T_ij == '#' for T_i in T for T_ij in T_i)


if __name__ == '__main__':
    main()
