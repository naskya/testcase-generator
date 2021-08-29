def main() -> None:
    N = int(input())
    L = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(L) == 2 * N
    assert all(1 <= L_i <= 100 for L_i in L)


if __name__ == '__main__':
    main()
