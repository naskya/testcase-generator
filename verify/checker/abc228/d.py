def main() -> None:
    Q = int(input())
    assert 1 <= Q <= 100

    two_found = False

    for _ in range(Q):
        t, x = map(int, input().split())
        two_found |= (t == 2)

        assert t == 1 or t == 2
        assert 0 <= x <= 10**18

    assert two_found


if __name__ == '__main__':
    main()
