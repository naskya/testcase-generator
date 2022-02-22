def main() -> None:
    N, M = map(int, input().split())
    assert 2 <= N <= 2*(10**5)
    assert 1 <= M <= 100

    for _ in range(M):
        A_i, B_i = map(int, input().split())
        assert 1 <= A_i <= N
        assert 1 <= B_i <= N
        assert A_i != B_i


if __name__ == '__main__':
    main()
