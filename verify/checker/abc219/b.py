def main() -> None:
    for _ in range(3):
        S_i = input()
        assert 1 <= len(S_i) <= 10
        assert S_i.islower()

    T = input()
    assert 1 <= len(T) <= 1000
    assert all(T_i in ('1', '2', '3') for T_i in T)


if __name__ == '__main__':
    main()
