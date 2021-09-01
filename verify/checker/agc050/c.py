def main() -> None:
    s = input()

    assert 1 <= len(s) <= 100
    assert all(s_i in ('B', 'S', '?') for s_i in s)


if __name__ == '__main__':
    main()
