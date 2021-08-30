def main() -> None:
    A_str, B_str = input().split()

    assert 0 <= int(A_str) <= 10**15
    assert 0 <= float(B_str) < 10
    assert B_str[-3] == '.'
    assert all(b.isnumeric() for b in B_str.split('.'))


if __name__ == '__main__':
    main()
