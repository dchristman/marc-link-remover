from pymarc import MARCReader
from pymarc import MARCWriter
from pathlib import Path

def main():
    mrc_input = get_input()
    mrc_output = get_output()
    search_string = raw_input("Enter string to identify matches: ")
    remove_links(search_string, mrc_input, mrc_output)
    #write_mrc(output, mrc_output)

def get_input():
    while True:
        input_path = raw_input("Enter filename for input Marc data (type 'exit' to quit): ")
        if Path(input_path).is_file():
            return input_path
        elif input_path == "exit":
            exit()
        else:
            print "File not found."

def get_output():
    input_path = raw_input("Enter filename for output Marc data (type 'exit' to quit): ")
    if Path(input_path).is_file():
        while True:
            prompt = raw_input("File already exists. Overwrite? Y/n: ")
            if prompt =='y' or prompt == 'Y' or prompt == '':
                break
            elif prompt == 'n' or prompt == 'N':
                return get_output()
            else:
                print "Invalid entry"
    elif input_path == 'exit':
        exit()
    return input_path

def remove_links(search, input, output):
    records_total = 0
    links_total = 0
    links_removed = 0
    errors = 0
    out = open(output, 'wb')
    with open(input) as fh:
        reader = MARCReader(fh)
        for record in reader:
            records_total += 1
            for field in record.get_fields('856'):
                links_total += 1
                if field.value().find(search) != -1:
                    record.remove_field(field)
                    links_removed += 1
            try:
                out.write(record.as_marc())
            except:
                errors += 1
    print "Total records: " + str(records_total)
    print "Total links: " + str(links_total)
    print "Links removed: " + str(links_removed)
    print "Records skipped and not written: " + str(errors)
    out.close()

#def write_mrc(reader, output_path):




main()
