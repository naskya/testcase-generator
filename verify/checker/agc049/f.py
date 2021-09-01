def main() -> None:
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    C = list(map(int, input().split()))

    assert 1 <= N <= 100
    assert len(A) == len(B) == len(C) == N
    assert all(0 <= A_i <= 2*(10**5) for A_i in A)
    assert all(0 <= B_i <= 2*(10**5) for B_i in B)
    assert all(1 <= C_i <= 5 for C_i in C)


if __name__ == '__main__':
    main()
