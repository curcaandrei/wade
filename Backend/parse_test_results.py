import xml.etree.ElementTree as ET
import os

def parse_xml_report(file):
    tree = ET.parse(file)
    root = tree.getroot()
    for testcase in root.iter('testcase'):
        name = testcase.get('name')
        classname = testcase.get('classname')
        status = "Passed"
        for child in testcase:
            if child.tag == 'failure':
                status = "Failed"
            elif child.tag == 'error':
                status = "Error"
        print(f"{classname}.{name} - {status}")

def main():
    test_reports_dir = 'test-reports'  # Adjust path if necessary
    for service_dir in os.listdir(test_reports_dir):
        service_path = os.path.join(test_reports_dir, service_dir)
        if os.path.isdir(service_path):
            print(f"Service: {service_dir}")
            for file in os.listdir(service_path):
                if file.endswith('.xml'):
                    parse_xml_report(os.path.join(service_path, file))

if __name__ == "__main__":
    main()
