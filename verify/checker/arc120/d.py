def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(A) == 2 * N
    assert all(1 <= A_i <= 10**9 for A_i in A)


if __name__ == '__main__':
    main()
