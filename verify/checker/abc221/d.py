def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    for _ in range(N):
        A, B = map(int, input().split())
        assert 1 <= A <= 10**9
        assert 1 <= B <= 10**9


if __name__ == '__main__':
    main()
