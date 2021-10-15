def main() -> None:
    N, A, B = map(int, input().split())
    D = list(map(int, input().split()))

    assert 1 <= N <= 200
    assert abs(A) <= 3.6 * (10**6)
    assert abs(B) <= 3.6 * (10**6)
    assert all(1 <= D_i <= 1800 for D_i in D)


if __name__ == '__main__':
    main()
