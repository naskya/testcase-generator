def main() -> None:
    N, M, X = map(int, input().split())

    assert 1 <= N <= 12
    assert 1 <= M <= 12
    assert 1 <= X <= 10**5

    for _ in range(N):
        buf = list(map(int, input().split()))
        C = buf[0]
        A = buf[1:]

        assert 1 <= C <= 10**5
        assert len(A) == M
        assert all(0 <= A_i <= 10**5 for A_i in A)


if __name__ == '__main__':
    main()
