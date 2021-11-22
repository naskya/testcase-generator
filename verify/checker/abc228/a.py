def main() -> None:
    S, T, X = map(int, input().split())

    assert 0 <= S <= 23
    assert 0 <= T <= 23
    assert 0 <= X <= 23
    assert S != T


if __name__ == '__main__':
    main()
