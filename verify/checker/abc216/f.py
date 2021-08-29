def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(A) == N
    assert len(B) == N
    assert all(1 <= A_i <= 5000 for A_i in A)
    assert all(1 <= B_i <= 5000 for B_i in B)


if __name__ == '__main__':
    main()
