def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    for _ in range(N):
        A, B = map(int, input().split())

        assert -10**18 <= A <= 10**18
        assert -10**18 <= B <= 10**18


if __name__ == '__main__':
    main()
