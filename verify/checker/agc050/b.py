def main() -> None:
    N = int(input())
    assert 3 <= N <= 100

    for _ in range(N):
        a = int(input())
        assert -100 <= a <= 100


if __name__ == '__main__':
    main()
