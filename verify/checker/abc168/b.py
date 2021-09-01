def main() -> None:
    K = int(input())
    S = input()

    assert 1 <= K <= 100
    assert 1 <= len(S) <= 100
    assert S.islower()


if __name__ == '__main__':
    main()
