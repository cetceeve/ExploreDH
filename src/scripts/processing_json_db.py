import sys_io_json as io

if __name__ == "__main__":
    # read from cache if files are present and no reparse was forced by user
    if io.hasFiles(io.source["cache"], ["dictPerson", "dictOrga", "dictLocation", "dictArticle", "dictKeyword"]):
        print("reading from cache")
        dictPerson = io.read(io.source["cache"], "dictPerson")
        dictOrga = io.read(io.source["cache"], "dictOrga")
        dictLocation = io.read(io.source["cache"], "dictLocation")
        dictArticle = io.read(io.source["cache"], "dictArticle")
        dictKeyword = io.read(io.source["cache"], "dictKeyword")

        print("creating database")
        db = {
            "people": dictPerson,
            "orgas": dictOrga,
            "locations": dictLocation,
            "articles": dictArticle,
            "keywords": dictKeyword
        }

        print("writing to \"{}\"".format(io.source["output"]["path"].format("database")))
        io.write(io.source["output"], db, "database")
    else:
        print("Error: required data not in \"{}\"!".format(io.source["cache"]["dir"]))
