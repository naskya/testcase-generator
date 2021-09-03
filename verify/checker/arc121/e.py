def main() -> None:
    N = int(input())
    p = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(p) == N - 1
    assert all(1 <= p[i] <= i + 1 for i in range(N - 1))


if __name__ == '__main__':
    main()
