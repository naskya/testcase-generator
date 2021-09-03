def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    assert 2 <= N <= 100
    assert len(A) == len(B) == N
    assert all(0 <= A_i <= 10**9 for A_i in A)
    assert all(0 <= B_i <= 10**9 for B_i in B)


if __name__ == '__main__':
    main()
