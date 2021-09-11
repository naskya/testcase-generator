def main() -> None:
    N, R = map(int, input().split())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert 1 <= R <= N - 1
    assert len(A) == N - 1
    assert all(1 <= A_i <= 10**9 for A_i in A)


if __name__ == '__main__':
    main()
