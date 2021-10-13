from Api import Api


def main():
    api = Api('all_matches.json')
    allMatches = api.getAllMatches()
    print(f"Done! Received {len(allMatches)} entries in total.")


if __name__ == '__main__':
    main()
