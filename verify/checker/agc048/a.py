def main() -> None:
    T = int(input())
    assert T == 1

    S = input()
    assert S.islower()
    assert 1 <= len(S) <= 100


if __name__ == '__main__':
    main()
