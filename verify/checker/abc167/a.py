def main() -> None:
    S = input()
    T = input()

    assert S.islower()
    assert T.islower()
    assert 1 <= len(S) <= 10
    assert len(T) == len(S) + 1


if __name__ == '__main__':
    main()
