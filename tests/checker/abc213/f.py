def main() -> None:
    N = int(input())
    S = input()

    assert 1 <= N <= 100
    assert len(S) == N
    assert S.islower()


if __name__ == '__main__':
    main()
