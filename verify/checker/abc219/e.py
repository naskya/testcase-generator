def main() -> None:
    one_found = False

    for _ in range(4):
        A_i = list(map(int, input().split()))
        assert len(A_i) == 4
        assert all(A_ij in (0, 1) for A_ij in A_i)
        one_found |= any(A_ij == 1 for A_ij in A_i)

    assert one_found


if __name__ == '__main__':
    main()
