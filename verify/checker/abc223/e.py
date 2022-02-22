def main() -> None:
    X, Y, A, B, C = map(int, input().split())
    assert 1 <= X <= 10**9
    assert 1 <= Y <= 10**9
    assert 1 <= A <= 10**18
    assert 1 <= B <= 10**18
    assert 1 <= C <= 10**18


if __name__ == '__main__':
    main()
