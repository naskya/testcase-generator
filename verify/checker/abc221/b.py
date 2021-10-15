def main() -> None:
    S = input()
    T = input()

    assert 2 <= len(S) == len(T) <= 100
    assert S.islower()
    assert T.islower()


if __name__ == '__main__':
    main()
