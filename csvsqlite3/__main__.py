import csvsqlite3
import sys
if __name__ == "__main__":
    colnum = int(sys.argv[2])
    lines = int(sys.argv[3])
    csvsqlite3.print_column(sys.argv[1], colnum,num=lines)
