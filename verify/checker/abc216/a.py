def main() -> None:
    X_Y = input()

    assert X_Y[:-2].isnumeric()
    assert X_Y[-2] == '.'
    assert X_Y[-1].isnumeric()
    assert 1 <= int(X_Y[:-2]) <= 15
    assert 0 <= int(X_Y[-1]) <= 9


if __name__ == '__main__':
    main()
