def main() -> None:
    N = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(a) == len(b) == N
    assert all(0 <= a_i <= 2**30 for a_i in a)
    assert all(0 <= b_i <= 2**30 for b_i in b)


if __name__ == '__main__':
    main()
