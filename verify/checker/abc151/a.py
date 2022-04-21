def main() -> None:
    C = input()
    assert len(C) == 1
    assert C.islower()
    assert C != 'z'


if __name__ == '__main__':
    main()
