def main() -> None:
    N, K = map(int, input().split())
    k_str = [''] * K

    for i in range(K):
        c, k_str[i] = input().split()
        assert c in ('L', 'R')

    k = list(map(int, k_str))

    assert 1 <= N <= 1000
    assert 1 <= K <= 100
    assert all(1 <= k_i <= N for k_i in k)
    assert len(set(k)) == K


if __name__ == '__main__':
    main()
