def main() -> None:
    T = int(input())
    assert T == 1

    N = int(input())
    assert 1 <= N <= 100

    for _ in range(N):
        L, R = map(int, input().split())

        assert 1 <= L <= 10**9
        assert 1 <= R <= 10**9
        assert L <= R


if __name__ == '__main__':
    main()
