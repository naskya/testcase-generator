def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    assert 1 <= N <= 100
    assert len(A) == 2 * N
    assert all(0 <= A_i < 2**30 for A_i in A)


if __name__ == '__main__':
    main()
