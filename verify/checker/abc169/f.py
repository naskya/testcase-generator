def main() -> None:
    N, S = map(int, input().split())
    A = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert 1 <= S <= 3000
    assert len(A) == N
    assert all(1 <= A_i <= 3000 for A_i in A)


if __name__ == '__main__':
    main()
