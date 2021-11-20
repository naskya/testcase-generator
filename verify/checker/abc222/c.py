def main() -> None:
    N, M = map(int, input().split())

    assert 1 <= N <= 50
    assert 1 <= M <= 100

    for _ in range(2 * N):
        A = input()

        assert len(A) == M
        assert all(A_ij in ('G', 'C', 'P') for A_ij in A)


if __name__ == '__main__':
    main()
