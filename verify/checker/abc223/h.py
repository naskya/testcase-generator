def main() -> None:
    N, Q = map(int, input().split())
    assert 1 <= N <= 100
    assert 1 <= Q <= 50

    A = list(map(int, input().split()))
    assert len(A) == N
    assert all(1 <= A_i < 2**60 for A_i in A)

    for _ in range(Q):
        L, R, X = map(int, input().split())
        assert 1 <= L <= R <= N
        assert 1 <= X < 2**60


if __name__ == '__main__':
    main()
