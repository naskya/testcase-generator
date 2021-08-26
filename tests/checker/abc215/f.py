def main() -> None:
    N = int(input())

    assert 2 <= N <= 2*(10**5)

    x = [0] * N
    y = [0] * N

    for i in range(N):
        x[i], y[i] = map(int, input().split())

    assert all(1 <= x_i <= 10**9 for x_i in x)
    assert all(1 <= y_i <= 10**9 for y_i in y)
    assert all(x[i] != x[j] or y[i] != y[j] for i in range(N) for j in range(i + 1, N))


if __name__ == '__main__':
    main()
