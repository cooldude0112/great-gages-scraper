import json

from jsonschema.validators import validate


def do_validation(file_name):
    print("File Validation started ....")
    for index, object in enumerate(json.loads(open(file_name, "rb").read())):
        try:
            print("processing ...", index)
            validate(
                instance=object,
                schema=json.loads(open('ScrapeVendorProduct.schema.json', "rb").read())
            )
        except Exception as e:
            print(e)
            print(json.dumps(object))
            exit(-1)

    print("File Validated ....")


if __name__ == '__main__':
    input_file = r"K:\My Drive\ics\Futek\04-04-2023\2023-04-04-v1.json"
    do_validation(input_file)
