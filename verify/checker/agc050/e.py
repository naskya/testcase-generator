def main() -> None:
    g1, r1, g2, r2, g3, r3 = map(int, input().split())

    assert 1 <= g1 <= 10**12
    assert 1 <= r1 <= 10**12
    assert 1 <= g2 <= 10**12
    assert 1 <= r2 <= 10**12
    assert 1 <= g3 <= 10**12
    assert 1 <= r3 <= 10**12


if __name__ == '__main__':
    main()
