
if __name__ == "__main__":
    import sys
    sys.stdout.write(sys.version)
    if sys.version_info[0] != "3":
        sys.stdout.write("\nkindly use python 3.x to run the program\n")
        sys.exit(1)

    from maincli import main
    main()

# -- END --