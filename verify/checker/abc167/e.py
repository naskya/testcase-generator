def main() -> None:
    N, M, K = map(int, input().split())

    assert 1 <= N <= 2*(10**5)
    assert 1 <= M <= 2*(10**5)
    assert 0 <= K <= N - 1


if __name__ == '__main__':
    main()
