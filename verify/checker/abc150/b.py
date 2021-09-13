def main() -> None:
    N = int(input())
    S = input()

    assert 3 <= N <= 50
    assert len(S) == N
    assert S.isupper()


if __name__ == '__main__':
    main()
