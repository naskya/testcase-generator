def main() -> None:
    N, K = map(int, input().split())
    assert 1 <= K <= N <= 100

    for _ in range(N):
        P_i = tuple(map(int, input().split()))
        assert len(P_i) == 3
        assert all(0 <= P_ij <= 300 for P_ij in P_i)


if __name__ == '__main__':
    main()
