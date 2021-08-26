def main() -> None:
    S = input()

    assert 1 <= len(S) <= 15

    for c in S:
        assert (c in (',', '!')) or c.isalpha()


if __name__ == '__main__':
    main()
