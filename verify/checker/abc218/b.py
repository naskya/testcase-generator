def main() -> None:
    P = list(map(int, input().split()))
    P.sort()

    assert len(P) == 26
    assert P == list(range(1, 26 + 1))


if __name__ == '__main__':
    main()
