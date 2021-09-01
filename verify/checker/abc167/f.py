def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    sum_of_lengths = 0

    for _ in range(N):
        S = input()
        sum_of_lengths += len(S)
        assert len(S) != 0
        assert all(S_i in ('(', ')') for S_i in S)

    assert sum_of_lengths <= 1000


if __name__ == '__main__':
    main()
