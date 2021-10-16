def main() -> None:
    A, B, C = map(int, input().split())

    assert 1 <= A <= B <= 1000
    assert 1 <= C <= 1000


if __name__ == '__main__':
    main()
