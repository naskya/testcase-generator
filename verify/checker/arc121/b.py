def main() -> None:
    N = int(input())
    assert 1 <= N <= 100

    for _ in range(2 * N):
        a_str, c = input().split()
        assert 1 <= int(a_str) <= 10**15
        assert c in ('R', 'G', 'B')


if __name__ == '__main__':
    main()
