def main() -> None:
    N, M = map(int, input().split())
    A = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert 1 <= M <= 100
    assert len(A) == N
    assert all(1 <= A_i <= 10**5 for A_i in A)


if __name__ == '__main__':
    main()
