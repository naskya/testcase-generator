def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert len(A) == N
    assert all(1 <= A_i <= 10**9 for A_i in A)


if __name__ == '__main__':
    main()
