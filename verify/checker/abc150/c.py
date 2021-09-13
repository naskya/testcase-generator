def main() -> None:
    N = int(input())
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))

    P.sort()
    Q.sort()

    assert 2 <= N <= 8
    assert len(P) == len(Q) == N
    assert P == Q == list(range(1, N + 1))


if __name__ == '__main__':
    main()
