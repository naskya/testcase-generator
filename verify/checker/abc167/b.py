def main() -> None:
    A, B, C, K = map(int, input().split())

    assert 0 <= A
    assert 0 <= B
    assert 0 <= C
    assert 1 <= K <= A + B + C <= 2*(10**9)


if __name__ == '__main__':
    main()
