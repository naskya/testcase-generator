def main() -> None:
    N, K = map(int, input().split())
    c = input()

    assert 2 <= N <= 100
    assert 1 <= K <= (N + 1) / 2
    assert len(c) == N - 1
    assert all(c_i in ('A', 'B', '?') for c_i in c)


if __name__ == '__main__':
    main()
