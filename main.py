from Api import Api

if __name__ == '__main__':
    api = Api('all_matches.json')
    allMatches = api.getAllMatches()
    print("Done!")

