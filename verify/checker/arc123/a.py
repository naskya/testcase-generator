def main() -> None:
    A_1, A_2, A_3 = map(int, input().split())
    assert 1 <= A_1 <= 10**15
    assert 1 <= A_2 <= 10**15
    assert 1 <= A_3 <= 10**15


if __name__ == '__main__':
    main()
