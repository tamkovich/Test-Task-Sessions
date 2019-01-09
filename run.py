from data_ import FlaurologicalDataStructure


URL = "https://flaurological.org/meetings/past-meetings/2018-program-schedule.aspx"


def main():
    dataset = FlaurologicalDataStructure(URL)


if __name__ == '__main__':
    main()
