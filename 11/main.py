import cjson


def main():
    json_str = '{"old_year": 2023, "new_year": "2024"}'

    res = cjson.loads(json_str)
    # res = json.loads(json_str)
    print(res)
    print(type(res))
    print(type(res["old_year"]), type(res["new_year"]))
    print(res)


if __name__ == "__main__":
    main()
