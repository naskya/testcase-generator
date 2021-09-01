def main() -> None:
    N, K, T = map(int, input().split())

    assert 1 <= N <= 50
    assert 1 <= K <= 50
    assert 1 <= T <= 10**7

    for _ in range(N):
        B = list(map(int, input().split()))

        assert len(B) == K
        assert all(1 <= B_ij <= 10**9 for B_ij in B)


if __name__ == '__main__':
    main()
