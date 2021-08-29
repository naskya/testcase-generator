def main() -> None:
    N, X = map(int, input().split())

    assert 2 <= N <= 10**12
    assert 1 <= X <= N - 1


if __name__ == '__main__':
    main()
