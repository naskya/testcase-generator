def main() -> None:
    N, M = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    c = [list(map(int, input().split())) for _ in range(N)]

    assert 1 <= N <= 20
    assert 1 <= M <= 1000
    assert len(A) == N
    assert len(B) == M
    assert all(1 <= A_i <= 10**5 for A_i in A)
    assert all(1 <= B_i <= 10**5 for B_i in B)
    assert all(len(c[i]) == M for i in range(N))
    assert all(c[i][j] in (0, 1) for i in range(N) for j in range(M))
    assert all(any(c[i][j] == 1 for i in range(N)) for j in range(M))


if __name__ == '__main__':
    main()
