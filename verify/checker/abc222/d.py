def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    assert 1 <= N <= 3000
    assert len(A) == len(B) == N
    assert A == sorted(A)
    assert B == sorted(B)
    assert all(A[i] <= B[i] for i in range(N))


if __name__ == '__main__':
    main()
