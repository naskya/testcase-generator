def main() -> None:
    N = int(input())
    a = list(map(int, input().split()))

    assert 3 <= N <= 100
    assert len(a) == N
    assert all(0 <= a_i <= 10**9 for a_i in a)


if __name__ == '__main__':
    main()
