def main() -> None:
    K = int(input())
    assert 2 <= K <= 10

    A, B = input().split()
    assert A[0] != '0'
    assert B[0] != '0'
    assert all(ord(A_i) - ord('0') < K for A_i in A)
    assert all(ord(B_i) - ord('0') < K for B_i in B)
    assert 1 <= int(A, K) <= 10**5
    assert 1 <= int(B, K) <= 10**5


if __name__ == '__main__':
    main()
