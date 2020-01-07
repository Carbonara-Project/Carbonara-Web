import json

def parse_report_file(report_file):
  """
  Decoder that given an encoded report_file returns a dict of the report
  
  :param report_file: file containing the encoded report
  """
  report = ''
  for c in report_file.chunks():
    report += c.decode()
  return json.loads(report)