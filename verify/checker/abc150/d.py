def main() -> None:
    N, M = map(int, input().split())
    a = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert 1 <= M <= 10**9
    assert len(a) == N
    assert all(a_i % 2 == 0 and 2 <= a_i <= 10**9 for a_i in a)


if __name__ == '__main__':
    main()
