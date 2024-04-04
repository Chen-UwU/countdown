import time
from internal import (
    get_config,
    generate_wallpaper,
    countdown,
    logger,
    change_wallpaper,
    check_time,
)


def main() -> None:
    try:
        while True:
            config = get_config()
            check_time()
            if config.now_state == "首考":
                time_diff = countdown(config.shoukao_date)
            else:
                time_diff = countdown(config.gaokao_date)
            image_path = generate_wallpaper(time_diff)
            change_wallpaper(image_path)
            logger.info("执行成功:" + str(time_diff) + "\n")
            time.sleep(config.update_time)
    except KeyboardInterrupt:
        logger.info("keyboard exit")


if __name__ == "__main__":
    main()
