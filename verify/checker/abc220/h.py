def main() -> None:
    N, M = map(int, input().split())
    AB = set(tuple(map(int, input().split())) for _ in range(M))

    assert 2 <= N <= 40
    assert 1 <= M <= N * (N - 1) / 2
    assert len(AB) == M
    assert all(1 <= a < b <= N for a, b in AB)


if __name__ == '__main__':
    main()
