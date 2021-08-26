def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))

    assert 1 <= N <= 2*(10**5)
    assert all(1 <= A_i <= N for A_i in A)


if __name__ == '__main__':
    main()
