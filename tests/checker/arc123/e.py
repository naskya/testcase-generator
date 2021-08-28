def main() -> None:
    T = int(input())
    N, Ax, Bx, Ay, By = map(int, input().split())
    assert T == 1
    assert 1 <= N <= 10**9
    assert 1 <= Ax <= 10**6
    assert 1 <= Bx <= 10**6
    assert 1 <= Ay <= 10**6
    assert 1 <= By <= 10**6


if __name__ == '__main__':
    main()
