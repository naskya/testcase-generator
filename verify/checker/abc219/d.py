def main() -> None:
    N = int(input())
    X, Y = map(int, input().split())
    assert 1 <= N <= 100
    assert 1 <= X <= 300
    assert 1 <= Y <= 300

    for _ in range(N):
        A, B = map(int, input().split())
        assert 1 <= A <= 300
        assert 1 <= B <= 300


if __name__ == '__main__':
    main()
