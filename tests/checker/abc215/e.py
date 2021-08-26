def main() -> None:
    N = int(input())
    S = input()

    assert 1 <= N <= 100
    assert len(S) == N
    assert all(c in 'ABCDEFGHIJ' for c in S)


if __name__ == '__main__':
    main()
