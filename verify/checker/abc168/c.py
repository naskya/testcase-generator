def main() -> None:
    A, B, H, M = map(int, input().split())

    assert 1 <= A <= 1000
    assert 1 <= B <= 1000
    assert 0 <= H <= 11
    assert 0 <= M <= 59


if __name__ == '__main__':
    main()
