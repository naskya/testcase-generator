def main() -> None:
    T = int(input())
    assert T == 1

    N = int(input())
    a = list(map(int, input().split()))
    a.sort()

    assert 2 <= N <= 100
    assert len(a) == N
    assert a == list(range(1, N + 1))


if __name__ == '__main__':
    main()
