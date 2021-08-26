def main() -> None:
    N = int(input())
    c = list(map(int, input().split()))

    assert 1 <= N <= 5*(10**4)
    assert all(1 <= c_i <= 10**9 for c_i in c)


if __name__ == '__main__':
    main()