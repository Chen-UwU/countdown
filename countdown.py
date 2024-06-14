import time
from internal import (
    get_config,
    generate_wallpaper,
    countdown,
    logger,
    change_wallpaper,
    check_time,
    open_info,
    open_info2
)


def main() -> None:
    try:
        check_time()
        open_info()
        while True:
            config = get_config()
            if config.now_state == "首考":
                time_diff = countdown(config.shoukao_date)
            else:
                time_diff = countdown(config.gaokao_date)
            image_path = generate_wallpaper(time_diff)
            change_wallpaper(image_path)
            logger.info(f"执行成功:{time_diff}")
            time.sleep(config.update_time)
    except KeyboardInterrupt:
        logger.warning("keyboard exit")
    except Exception as e:
        logger.error(f"发生崩溃，崩溃原因：{e}")
        open_info2()
        raise e


if __name__ == "__main__":
    main()
