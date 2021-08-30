def main() -> None:
    N = int(input())
    assert 2 <= N <= 100

    for _ in range(N):
        A, B = map(int, input().split())
        assert 1 <= A <= B <= 10**9


if __name__ == '__main__':
    main()
