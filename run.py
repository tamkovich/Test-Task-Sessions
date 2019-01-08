from driver_config import FlaurologicalDriver


URL = "https://flaurological.org/meetings/past-meetings/2018-program-schedule.aspx"
driver = FlaurologicalDriver()


def main():
    driver.run(URL)
    driver.quit()


if __name__ == '__main__':
    main()
