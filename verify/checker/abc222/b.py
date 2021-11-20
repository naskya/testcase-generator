def main() -> None:
    N, P = map(int, input().split())
    a = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert 1 <= P <= 100
    assert len(a) == N
    assert all(0 <= a_i <= 100 for a_i in a)


if __name__ == '__main__':
    main()
