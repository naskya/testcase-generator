def main() -> None:
    N, D = map(int, input().split())

    assert 2 <= N <= 10**6
    assert 1 <= D <= 2 * (10**6)


if __name__ == '__main__':
    main()
