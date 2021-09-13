def main() -> None:
    N = int(input())
    C = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(C) == N
    assert all(1 <= C_i <= 10**9 for C_i in C)


if __name__ == '__main__':
    main()
