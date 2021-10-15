def main() -> None:
    N = input()

    assert 1 <= int(N) <= 10**9
    assert len(N) - N.count('0') >= 2


if __name__ == '__main__':
    main()
