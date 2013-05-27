if True:
 import argparse

 def main():
     parser = argparse.ArgumentParser(
         description='Concatenate files.')
     parser.add_argument(
         'FILE', nargs='*',
         help='Path(s) to files')

     args = parser.parse_args()

main()
