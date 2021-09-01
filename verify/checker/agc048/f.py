def main() -> None:
    S = input()

    assert 1 <= len(S) <= 300
    assert all(S_i in ('0', '1') for S_i in S)


if __name__ == '__main__':
    main()
