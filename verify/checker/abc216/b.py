def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    for _ in range(N):
        S, T = input().split()
        assert S.islower()
        assert T.islower()
        assert 1 <= len(S) <= 10
        assert 1 <= len(T) <= 10


if __name__ == '__main__':
    main()
