def main() -> None:
    X = input()
    assert set(X) == set(map(chr, range(ord('a'), ord('z') + 1)))

    N = int(input())
    assert 2 <= N <= 100

    S = [input() for _ in range(N)]
    assert all(S_i.islower() for S_i in S)
    assert all(1 <= len(S_i) <= 10 for S_i in S)
    assert all(S[i] != S[j] for i in range(N) for j in range(i + 1, N))


if __name__ == '__main__':
    main()
