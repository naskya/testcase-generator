def main() -> None:
    N = int(input())
    S = input()

    assert 1 <= N <= 7
    assert len(S) == 7
    assert all(S_i in ('o', 'x') for S_i in S)


if __name__ == '__main__':
    main()
