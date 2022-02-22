def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    for _ in range(N):
        A_i, B_i = map(int, input().split())
        assert 1 <= A_i <= 1000
        assert 1 <= B_i <= 1000


if __name__ == '__main__':
    main()
