def main() -> None:
    N, Q = map(int, input().split())
    S = input()

    assert 1 <= N <= 2*(10**5)
    assert 1 <= Q <= 100
    assert all(c in ('(', ')') for c in S)
    assert len(S) == N

    has_two = False

    for _ in range(Q):
        op, l, r = map(int, input().split())
        has_two |= (op == 2)

        assert op in (1, 2)
        assert 1 <= l < r <= N

    assert has_two


if __name__ == '__main__':
    main()
