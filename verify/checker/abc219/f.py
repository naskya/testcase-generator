def main() -> None:
    S = input()
    K = int(input())

    assert all(S_i in ('L', 'R', 'U', 'D') for S_i in S)
    assert 1 <= len(S) <= 100
    assert 1 <= K <= 10**12


if __name__ == '__main__':
    main()
