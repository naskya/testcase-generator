def main() -> None:
    N, K = map(int, input().split())
    p = list(map(int, input().split()))

    assert 1 <= K <= N <= 1000
    assert len(p) == N
    assert all(1 <= p_i <= 1000 for p_i in p)


if __name__ == '__main__':
    main()
