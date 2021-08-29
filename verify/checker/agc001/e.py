def main() -> None:
    N = int(input())
    assert 2 <= N <= 100

    for _ in range(N):
        A, B = map(int, input().split())

        assert 1 <= A <= 2000
        assert 1 <= B <= 2000


if __name__ == '__main__':
    main()
